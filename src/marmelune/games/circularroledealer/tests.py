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
