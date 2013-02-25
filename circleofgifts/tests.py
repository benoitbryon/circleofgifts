import unittest

from dealer import CircularDealer


class CircularDealerTestCase(unittest.TestCase):
    def test_sorted_deal(self):
        """Test deal which uses sorted() as the sort method for both teams
        and players. This makes the results predicable."""
        players = [['Pierre', 'Paul'], ['Jeanne', 'Julie'],
                   ['Sylvain', 'Sandra']]
        dealer = CircularDealer(players)
        dealer.sort_players_callback = lambda x: sorted(x)
        dealer.sort_teams_callback = lambda x: sorted(x)
        deal = dealer.deal()
        self.assertEqual(deal, ['Jeanne', 'Paul', 'Sandra', 'Julie', 'Pierre',
                                'Sylvain'])

    def test_deal_with_respect_to_history(self):
        # When there is no alternative (sorted result), then the dealer
        # MUST return successfully... and has no choice: it MUST return the
        # same result again and again, whatever the history.
        players = [['Pierre', 'Paul'], ['Jeanne', 'Julie'],
                   ['Sylvain', 'Sandra']]
        dealer = CircularDealer(players)
        dealer.sort_players_callback = lambda x: sorted(x)
        dealer.sort_teams_callback = lambda x: sorted(x)
        deal = dealer.deal_with_respect_to_history()
        self.assertEqual(deal, ['Jeanne', 'Paul', 'Sandra', 'Julie', 'Pierre',
                                'Sylvain'])
        deal = dealer.deal_with_respect_to_history()
        self.assertEqual(deal, ['Jeanne', 'Paul', 'Sandra', 'Julie', 'Pierre',
                                'Sylvain'])

    def test_is_deal_valid(self):
        dealer = CircularDealer([1, 2, 3, 4, 5, 6])
        # No repetition: valid
        self.assertTrue(dealer.is_deal_valid([1, 2, 3, 4, 5, 6], [1, 3, 5, 2, 6, 4]))
        # Exactly the same: invalid
        self.assertFalse(dealer.is_deal_valid([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]))
        # Scheme 6-1 is repeated: invalid
        self.assertFalse(dealer.is_deal_valid([1, 2, 3, 4, 5, 6], [1, 3, 5, 2, 4, 6]))
        # Exactly the opposite: invalid
        self.assertFalse(dealer.is_deal_valid([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1]))
        # Nothing in common: valid
        self.assertTrue(dealer.is_deal_valid([1, 2, 3, 4, 5, 6],
                                             [7, 8, 9]))
