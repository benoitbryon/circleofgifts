try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import copy
import random


def random_copy(iterable, random_callback=random.random):
    """Shuffle iterable and return a randomized copy.

    >>> random_copy([])
    []
    >>> random_copy([1])
    [1]
    >>> l = range(1000)
    >>> randomized = random_copy(l)
    >>> randomized is not l
    True
    >>> all([item in l for item in randomized])
    True
    >>> len(randomized) == len(l)
    True
    >>> same = True
    >>> for i in range(10):  # Let's assume that there are poor chances the
    ...                      # same random list of 1000 elements being
    ...                      # generated 10 times.
    ...     m = random_copy(l)
    ...     if m != l:
    ...         same = False
    ...         break
    >>> same
    False

    The optional argument random_callback is a 0-argument callable returning a
    random float in [0.0, 1.0); by default, this is the function
    random.random().

    If the random_callback always return the same value, the result of
    random_copy() will always be the same. Might be useful for tests.

    >>> def fake_random(): return 0.1
    >>> same = True
    >>> m = random_copy(l, fake_random)
    >>> for i in range(10):  # Let's assume that there are poor chances the
    ...                      # same random list of 1000 elements being
    ...                      # generated 10 times.
    ...     n = random_copy(l, fake_random)
    ...     if m != n:
    ...         same = False
    ...         break
    >>> same
    True
    """
    result = copy.deepcopy(iterable)
    random.shuffle(result, random_callback)
    return result


def permutations(items, sort_callback=None):
    """Generator of sorted permutations for items.

    >>> list(permutations([]))
    []
    >>> list(permutations([1]))
    [[1]]
    >>> list(permutations([1, 2]))
    [[1, 2], [2, 1]]
    >>> list(permutations([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    """
    import itertools
    if items:
        for item in itertools.permutations(items, len(items)):
            yield list(item)


def unique_circular_permutations(items, sort_callback=copy.deepcopy):
    """Generator of permutations, whithout circular duplicates.

    First item in results is predictable: always the first in ``items``.
    It serves as a pivot and is kept as is. Other items are sorted using
    ``sort_callback``.

    >>> list(unique_circular_permutations([]))
    []
    >>> list(unique_circular_permutations([1]))
    [[1]]
    >>> list(unique_circular_permutations([1, 2]))
    [[1, 2]]
    >>> list(unique_circular_permutations([1, 2, 3], sort_callback=sorted))
    [[1, 2, 3], [1, 3, 2]]
    >>> list(unique_circular_permutations([1, 2, 3, 4], sort_callback=sorted))
    [[1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4], [1, 3, 4, 2], [1, 4, 2, 3], [1, 4, 3, 2]]

    """
    if not items:
        pass
    else:
        items = copy.deepcopy(items)
        pivot = items.pop(0)
        if not items:
            yield [pivot]
        else:
            for permutation in permutations(items, sort_callback=sort_callback):
                yield [pivot] + permutation


def fibo2(n):
    """Return F_{n-1}, F_n"""
    if (n == 0):  # Base case.
        return 1, 0  # F_{-1}, F_0
    else:  # Recurrency.
        f_k_1, f_k = fibo2(n // 2)  # F_{k-1}, F_k when k = n/2
        f2_k = f_k ** 2  # F_k^2
        if n % 2 == 0:  # n is even
            return (f2_k + f_k_1 ** 2,
                    f_k * f_k_1 * 2 + f2_k)  # F_{2k-1}, F_{2k}
        else:  # n is odd
            return (f_k * f_k_1 * 2 + f2_k,
                    (f_k + f_k_1) ** 2 + f2_k)  # F_{2k}, F_{2k+1}


def fibonacci(n):
    """Return fibonacci level n.

    >>> fibonacci(0)
    0
    >>> fibonacci(1)
    1
    >>> fibonacci(2)
    1
    >>> fibonacci(3)
    2
    >>> fibonacci(4)
    3
    >>> fibonacci(5)
    5
    >>> fibonacci(6)
    8
    >>> fibonacci(7)
    13

    """
    return fibo2(n)[1]


class Dealer(object):
    """Dealer instance distribute roles to players."""
    def __init__(self, players=[], history=[]):
        self.history = history
        self.players = players
        default_sort_callback = random_copy
        self.sort_players_callback = default_sort_callback
        self.sort_teams_callback = default_sort_callback

    @property
    def all_players(self):
        """Return flat list of players, i.e. concatenated teams.

        >>> players = [['albert', 'allan', 'arthur'], ['bob'], ['carl', 'cathy']]
        >>> d = Dealer(players)
        >>> d.all_players
        ['albert', 'allan', 'arthur', 'bob', 'carl', 'cathy']

        """
        try:
            return self._all_players
        except AttributeError:
            self._all_players = []
            for team in self.players:
                for player in team:
                    self._all_players.append(player)
            return self._all_players

    def generate_permutations(self, sort_callback=copy.deepcopy):
        """Generate permutations with all players.

        With respect to the following base rules:

        * teammates cannot hunt each other.
        * there are no circular (from left to right) duplicates.

        With no players, you get an empty deal.

        >>> players = []
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        []

        If there is only one player, he is the result.

        >>> players = [['albert']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        [['albert']]

        If there is only one team, you get an empty deal, since teammates
        cannot hunt each other.

        >>> players = [['albert', 'allan']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        []

        There are other cases without results because of the "can't hunt
        teammate" rule.

        >>> players = [['a1', 'a2'], ['b1']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        []

        If there is two teams of one players, you get one result with the two
        players, order is preserved.

        >>> players = [['albert'], ['bob']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        [['albert', 'bob']]

        Here are results with more complex examples...

        >>> players = [['a1'], ['b1'], ['c1']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations())
        [['a1', 'b1', 'c1'], ['a1', 'c1', 'b1']]

        >>> players = [['a1', 'a2'], ['b1'], ['c1']]
        >>> d = Dealer(players)
        >>> list(d.generate_permutations(sort_callback=sorted))
        [['a1', 'b1', 'a2', 'c1'], ['a1', 'c1', 'a2', 'b1']]

        """
        if self.all_players:
            for result in unique_circular_permutations(self.all_players):
                if not self.has_same_team(result):
                    yield result

    def teammates(self, player):
        """Return list of teammates of player.

        >>> players = [['albert', 'allan', 'arthur'], ['bob'], ['carl', 'cathy']]
        >>> d = Dealer(players)
        >>> d.teammates('albert')
        ['allan', 'arthur']
        >>> d.teammates('allan')
        ['albert', 'arthur']
        >>> d.teammates('arthur')
        ['albert', 'allan']
        >>> d.teammates('bob')
        []
        >>> d.teammates('carl')
        ['cathy']
        >>> d.teammates('cathy')
        ['carl']

        """
        if not hasattr(self, '_teammates'):
            self._teammates = {}
            for team in self.players:
                for p in team:
                    self._teammates[p] = team[:]
                    self._teammates[p].remove(p)
        return self._teammates[player]

    def has_same_team(self, deal):
        """Return ``True`` if there is at least one "teammate hunt" in deal.

        >>> players = [['a1', 'a2', 'a3'], ['b1'], ['c1', 'c2']]
        >>> d = Dealer(players)
        >>> d.has_same_team([])
        False
        >>> d.has_same_team(['a1'])
        False
        >>> d.has_same_team(['a1', 'b1'])
        False
        >>> d.has_same_team(['a1', 'a2', 'b1'])
        True
        >>> d.has_same_team(['a1', 'a3', 'b1'])
        True
        >>> d.has_same_team(['a1', 'b1', 'a2'])
        True
        >>> d.has_same_team(['a1', 'c1', 'c2'])
        True

        """
        if not deal:
            return False
        if len(deal) == 1:
            if not deal[0] in self.all_players:
                raise KeyError(deal[0])
            return False
        items = deal[:]
        items.append(items[0])  # Make deal circular.
        for i in range(0, len(items) - 1):
            if items[i + 1] in self.teammates(items[i]):
                return True
        return False

    def count_same_team(self, deal):
        """Count occurences in deal where player hunts a teammate.

        >>> players = [['albert', 'allan', 'arthur'], ['bob'], ['carl', 'cathy']]
        >>> d = Dealer(players)
        >>> d.count_same_team([])
        0
        >>> d.count_same_team(['albert'])
        0
        >>> d.count_same_team(['albert', 'bob'])
        0
        >>> d.count_same_team(['albert', 'allan', 'bob'])
        1
        >>> d.count_same_team(['allan', 'albert', 'bob'])
        1
        >>> d.count_same_team(['albert', 'allan', 'arthur', 'bob'])
        2
        >>> d.count_same_team(['albert', 'allan', 'carl', 'cathy'])
        2

        Beware of the rotations! The deal is circular, i.e. the last player
        hunts the first one.

        >>> players = [['albert', 'allan', 'arthur'], ['bob'], ['carl', 'cathy']]
        >>> d = Dealer(players)
        >>> d.count_same_team(['albert', 'allan'])
        2
        >>> d.count_same_team(['allan', 'albert'])
        2
        >>> d.count_same_team(['albert', 'allan', 'arthur'])
        3

        Players in deal are supposed to be members of the game, else a KeyError
        is raised.

        >>> players = [['albert', 'allan', 'arthur'], ['bob'], ['carl', 'cathy']]
        >>> d = Dealer(players)
        >>> d.count_same_team(['zoe'])  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: 'zoe'
        >>> d.count_same_team(['albert', 'zoe'])  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: 'zoe'

        """
        if not deal:
            return 0
        if len(deal) == 1:
            if not deal[0] in self.all_players:
                raise KeyError(deal[0])
            return 0
        items = deal[:]
        items.append(items[0])
        count = 0
        for i in range(0, len(items) - 1):
            if items[i + 1] in self.teammates(items[i]):
                count += 1
        return count

    def targets(self, deal):
        """Return a list of tuples (HUNTER, TARGET) representing players.

        >>> deal = ['allan', 'bob', 'cathy']
        >>> d = Dealer()
        >>> d.targets(deal)
        [('allan', 'bob'), ('bob', 'cathy'), ('cathy', 'allan')]

        >>> deal = ['allan']
        >>> d = Dealer()
        >>> d.targets(deal)
        []

        >>> deal = []
        >>> d = Dealer()
        >>> d.targets(deal)
        []

        """
        if not deal or len(deal) == 1:
            return []
        targets = []
        items = deal[:]
        items.append(items[0])
        for i in range(0, len(items) - 1):
            targets.append((items[i], items[i + 1]))
        return targets

    def targets_in_history(self, history_level):
        """Return list of (HUNTER, TARGET) for the given history level.

        >>> history = [['allan', 'bob'], ['cathy', 'drew']]
        >>> d = Dealer(history=history)
        >>> d.targets_in_history(0)
        [('allan', 'bob'), ('bob', 'allan')]
        >>> d.targets_in_history(1)
        [('cathy', 'drew'), ('drew', 'cathy')]
        >>> d._history_targets
        [[('allan', 'bob'), ('bob', 'allan')], [('cathy', 'drew'), ('drew', 'cathy')]]

        Uses a cache to avoid computing targets each time this method is
        called. The cache is built, for all history levels, at the first call.

        >>> history = [['allan', 'bob'], ['cathy', 'drew']]
        >>> d = Dealer(history=history)
        >>> d._history_targets  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        AttributeError: 'Dealer' object has no attribute '_history_targets'
        >>> d.targets_in_history(0)
        [('allan', 'bob'), ('bob', 'allan')]
        >>> d._history_targets
        [[('allan', 'bob'), ('bob', 'allan')], [('cathy', 'drew'), ('drew', 'cathy')]]

        """
        if not hasattr(self, '_history_targets'):
            self._history_targets = []
            for level, history in enumerate(self.history):
                self._history_targets.append(self.targets(self.history[level]))
        return self._history_targets[history_level]

    def count_same_target(self, candidate_targets, reference_targets):
        """Return count of occurrences in candidate that are in reference.

        >>> d = Dealer()
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('cathy',  'drew')]
        >>> d.count_same_target(t1, t2)
        0
        >>> t1 = [('allan', 'cathy')]
        >>> t2 = [('cathy',  'drew'), ('drew', 'allan'), ('allan', 'cathy')]
        >>> d.count_same_target(t1, t2)
        1

        """
        count = 0
        for candidate_target in candidate_targets:
            if candidate_target in reference_targets:
                count += 1
        return count

    def score_same_target(self, items, history_level, coefficient=10):
        """Score when player's target has already been his target."""
        candidate_targets = dict(self.targets(items))
        reference_targets = dict(self.targets_in_history(history_level))
        for player in self.all_players:
            try:
                if candidate_targets[player] == reference_targets[player]:
                    history_threshold = \
                        len(self.all_players) - len(self.teammates(player)) - 1
                    if history_level < history_threshold:
                        return -1  # Blocker!
            except KeyError:
                pass
        return 1

    def count_direct_revenge(self, candidate_targets, reference_targets):
        """Count occurences where hunter in candidate is target in reference.

        >>> d = Dealer()
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('allan',  'bob')]
        >>> d.count_direct_revenge(t1, t2)
        0
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('bob',  'allan')]
        >>> d.count_direct_revenge(t1, t2)
        1

        """
        reverse_candidate_targets = []
        for hunter, target in candidate_targets:
            reverse_candidate_targets.append((target, hunter))
        return self.count_same_target(reverse_candidate_targets,
                                      reference_targets)

    def score_direct_revenge(self, items, history_level, coefficient=7):
        """Score when player's target used to be player's hunter."""
        candidate_targets = self.targets(items)
        reference_targets = self.targets_in_history(history_level)
        count = self.count_direct_revenge(candidate_targets, reference_targets)
        return count * self.coefficient(coefficient, history_level)

    def count_same_target_as_teammate(self, candidate_targets, reference_targets):
        """Count occurences where hunter's target in candidate is teammate's
        target in reference.

        >>> players = [['albert', 'allan'], ['bob', 'bill']]
        >>> d = Dealer(players=players)
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('bob',  'allan')]
        >>> d.count_same_target_as_teammate(t1, t2)
        0
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('albert',  'bob')]
        >>> d.count_same_target_as_teammate(t1, t2)
        1

        """
        count = 0
        for hunter, target in candidate_targets:
            for hunter_teammate in self.teammates(hunter):
                if (hunter_teammate, target) in reference_targets:
                    count += 1
        return count

    def score_same_target_as_teammate(self, items, history_level, coefficient=3):
        """Score when player's target used to be the target of a teammate."""
        candidate_targets = self.targets(items)
        reference_targets = self.targets_in_history(history_level)
        count = self.count_same_target_as_teammate(candidate_targets, reference_targets)
        return count * self.coefficient(coefficient, history_level)

    def count_teammate_revenge(self, candidate_targets, reference_targets):
        """Count occurences where hunter's target in candidate hunts teammate
        in reference.

        >>> players = [['albert', 'allan'], ['bob', 'bill']]
        >>> d = Dealer(players=players)
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('bob',  'allan')]
        >>> d.count_teammate_revenge(t1, t2)
        0
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('bob',  'albert')]
        >>> d.count_teammate_revenge(t1, t2)
        1

        """
        count = 0
        for hunter, target in candidate_targets:
            for hunter_teammate in self.teammates(hunter):
                if (target, hunter_teammate) in reference_targets:
                    count += 1
        return count

    def score_teammate_revenge(self, items, history_level, coefficient=2):
        """Score when player's target used to be the hunter of a teammate."""
        candidate_targets = self.targets(items)
        reference_targets = self.targets_in_history(history_level)
        count = self.count_teammate_revenge(candidate_targets, reference_targets)
        return count * self.coefficient(coefficient, history_level)

    def count_target_teammate(self, candidate_targets, reference_targets):
        """Count occurences where hunter's target in candidate is teammate of
        hunter's target in reference.

        >>> players = [['albert', 'allan'], ['bob', 'bill']]
        >>> d = Dealer(players=players)
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('bob',  'allan')]
        >>> d.count_target_teammate(t1, t2)
        0
        >>> t1 = [('allan', 'bob')]
        >>> t2 = [('allan',  'bill')]
        >>> d.count_target_teammate(t1, t2)
        1

        """
        count = 0
        for hunter, target in candidate_targets:
            for target_teammate in self.teammates(target):
                if (hunter, target_teammate) in reference_targets:
                    count += 1
        return count

    def score_target_teammate(self, items, history_level, coefficient=5):
        """Score when player's target used to be the hunter of a teammate."""
        candidate_targets = self.targets(items)
        reference_targets = self.targets_in_history(history_level)
        count = self.count_target_teammate(candidate_targets, reference_targets)
        return count * self.coefficient(coefficient, history_level)

    def count_team_target_team(self, candidate_targets):
        """Count occurences where hunter's target is in the same team as
        teammate's target.

        >>> players = [['albert', 'allan'], ['bob', 'bill'], ['carl', 'cathy']]
        >>> d = Dealer(players=players)
        >>> targets = [('allan', 'bob'), ('bob', 'albert'), ('albert', 'carl'), ('carl', 'bill'), ('bill', 'cathy'), ('cathy', 'allan')]
        >>> d.count_team_target_team(targets)
        0
        >>> targets = [('allan', 'bob'), ('bob', 'cathy'), ('cathy', 'albert'), ('albert', 'bill'), ('bill', 'carl'), ('carl', 'allan')]
        >>> d.count_team_target_team(targets)
        3

        """
        count = 0
        dict_targets = dict(candidate_targets)
        for hunter, target in candidate_targets:
            for teammate in self.teammates(hunter):
                if dict_targets[teammate] in self.teammates(target):
                    count += 1
                    dict_targets[hunter] = None  # Don't count hunter twice.
        return count

    def score_team_target_team(self, items, coefficient=7):
        """Score when player's target is in same team than a teammate's target."""
        candidate_targets = self.targets(items)
        count = self.count_team_target_team(candidate_targets)
        return count * self.coefficient(coefficient, 0)

    @property
    def history_threshold(self):
        """Return the number of meaningful history levels.

        Threshold is always lower than or equal to history length.

        >>> history = [1, 2]
        >>> players = [['albert', 'allan'], ['bob', 'bill'], ['carl', 'cathy'], ['dilbert'], ['emily', 'erika']]
        >>> d = Dealer(players=players, history=history)
        >>> d.history_threshold
        2

        Else, thereshold is total number of players.

        >>> history = [1, 2, 3, 4, 5, 6]  # Fake history which is not limiting factor.
        >>> players = [['albert', 'allan'], ['bob', 'bill']]
        >>> d = Dealer(players=players, history=history)
        >>> d.history_threshold
        4

        >>> history = [1, 2, 3, 4, 5, 6]  # Fake history which is not limiting factor.
        >>> players = [['albert', 'allan'], ['bob', 'bill'], ['carl', 'cathy']]
        >>> d = Dealer(players=players, history=history)
        >>> d.history_threshold
        6

        """
        threshold = len(self.all_players)
        return min(threshold, len(self.history))

    def coefficient(self, base, history_level=0):
        """Return multiplier depending on base and history level.

        >>> history = [1, 2, 3, 4, 5, 6]  # Fake history which is not limiting factor.
        >>> players = [['albert', 'allan'], ['bob', 'bill']]
        >>> d = Dealer(players=players, history=history)
        >>> d.history_threshold
        4
        >>> d.coefficient(10, 4)  # history_level >= d.history_threshold
        0
        >>> d.coefficient(10, 3) == fibonacci(10)
        True
        >>> d.coefficient(10, 2) == fibonacci(10 + 2)
        True
        >>> d.coefficient(10, 1) == fibonacci(10 + 4)
        True
        >>> d.coefficient(10, 0) == fibonacci(10 + 6)
        True

        """
        if history_level >= self.history_threshold:
            return 0
        history_factor = (self.history_threshold - history_level - 1) * 2
        coefficient = fibonacci(base + history_factor)
        return coefficient

    def deal(self):
        best_result = None
        count_iterations = 0
        for deal in self.generate_permutations():
            count_iterations += 1
            if count_iterations % 100000 == 0:
                print "%d iterations..." % count_iterations
            result = OrderedDict()
            total = 0
            too_much = False
            # Scores without history.
            for operation, coeff in [('score_team_target_team', 5), ]:
                score = getattr(self, operation)(deal, coeff)
                if score == -1:
                    too_much = True
                    break
                total += score
                if best_result and total >= best_result['score']:
                    too_much = True
                    break
                result[operation] = score
            if too_much:
                continue
            # Scores with history.
            history_levels = self.history_threshold
            for i in range(0, history_levels):
                for operation, coeff in [
                        ('score_same_target', 12),  #
                        ('score_direct_revenge', 7),  #
                        ('score_target_teammate', 4),  # 3, 13, 55...
                        ('score_same_target_as_teammate', 3),  # 2, 8, 34...
                        ('score_teammate_revenge', 2),  # 1, 5, 21...
                        ]:
                    score = getattr(self, operation)(deal, i, coeff)
                    if score == -1:
                        too_much = True
                        break
                    total += score
                    if best_result and total >= best_result['score']:
                        too_much = True
                        break
                    result['%s_%d' % (operation, i)] = score
                if too_much:
                    break
            if too_much:
                continue
            result['deal'] = deal
            result['score'] = total
            if total == 0:  # We got an winner!
                print '%d  --> %s' % (count_iterations, result)
                yield result
                break
            if not best_result or (best_result and result['score'] < best_result['score']):
                best_result = result
                print '%d  --> %s' % (count_iterations, result)
                yield result
