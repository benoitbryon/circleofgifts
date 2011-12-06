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
    >>> 
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
    random_copy() will always be the same.
    
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


class CircularDealer(object):
    """Dealer instance distribute roles to players.

    Each player is preceded by another player, and followed by another, so
    that the whole players form a ring.
    """
    def __init__(self, players=[], distribution_history=[]):
        self.distribution_history = distribution_history
        self.players = players
        default_sort_callback = random_copy
        self.sort_players_callback = default_sort_callback
        self.sort_teams_callback = default_sort_callback

    def __call__(self):
        """Does the distribution."""
        # Work on copies
        players = copy.deepcopy(self.players)
        
        # Initialize the distribution
        distribution = []

        # Sort teams
        players = self.sort_teams_callback(players)
        
        # Sort players in each team
        for i, team in enumerate(players):
            players[i] = self.sort_players_callback(team)
        
        # Find the first team with 2 players.
        # Else, implementation fails (could pass in the future...)
        markers = None
        for i, team in enumerate(players):
            if len(team) == 2:
                markers = team
                del players[i]
                break
        if not markers:
            raise NotImplementedError('As for now, cannot proceed if there ' \
                                      'is not at least 2 teams of 2 members.')
        
        # Assert that there is at least one other team with 2 players,
        # else, implementation fails (could be implemented in the future...)
        implemented = any([len(team) == 2 for team in players])
        if not implemented:
            raise NotImplementedError('As for now, cannot proceed if there ' \
                                      'is not at least 2 teams of 2 members.')
        
        # Create 2 lists which exclude markers
        left = []
        right = []
        for team in players:
            left.extend(team[0:1])
            right.extend(team[1:2])
        
        # Shuffle left and right lists
        left = self.sort_players_callback(left)
        right = self.sort_players_callback(right)
        
        # Concatenate firt marker, left, second marker then right
        for item in markers[0:1], left, markers[1:2], right:
            distribution.extend(item)

        # Remember history
        self.distribution_history.append(distribution)

        return distribution
