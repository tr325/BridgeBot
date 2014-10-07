from DeckUtils import Hand
from DeckUtils import Deck
from DeckUtils import BidHistory
from DeckUtils import Bid
import unittest


class TestBidHistory(unittest.TestCase):

	def setUp(self):
		self.bh = BidHistory()
		self.bh.pastBids = [[Bid(0,0), Bid(0,0)], [Bid(0,0)], 
							[Bid(1,1)], [Bid(0,0)]]
		self.bh.bidPosition = 1
		self.bh.numBids = 5
	
	def test_isBiddingFinished(self):
		self.assertFalse(self.bh.isBiddingFinished())
		self.bh.pastBids[self.bh.bidPosition].append(Bid(0,0))
		self.bh.bidPosition += 1
		self.assertTrue(self.bh.isBiddingFinished())
	
	def test_addBid(self):
		self.bh.addBid(Bid(0,0))
		self.assertEqual(self.bh.pastBids[1][1], Bid(0,0))
				

class TestHand(unittest.TestCase):

	def setUp(self):
		self.h = Hand()
		self.card = "9"
		self.suit = 2
		self.clubs = ["A", "J", "5", "4", "2"]
		self.diamonds = ["K", "Q","J", "7"]
		self.spades = ["10", "5"]
		self.hearts = ["6", "8"]
		self.cards = {1: self.clubs, 2: self.diamonds,
					  3: self.hearts, 4: self.spades}
		self.h.cards = self.cards
	
	def test_addCard(self):
		self.h.addCard(self.suit, self.card)
		self.assertTrue(self.card in self.h.cards[self.suit])
				
	def test_getCardPoints(self):
		self.assertEqual(self.h.getCardPoints(self.card), 0)
	
	def test_getSuitPoints(self):
		self.assertEqual(self.h.getSuitPoints(self.suit), 6)
		
	def test_getSuitLength(self):
		self.assertEqual(self.h.getSuitLength(self.suit), 4)
	
	def test_getTotalPoints(self):
		self.assertEqual(self.h.getTotalPoints(), 11)
		
	def test_findBestSuit(self):
		self.assertEqual(self.h.findBestSuit(), (1,5))
		
	def test_findSecondSuit(self):
		self.assertEqual(self.h.findSecondSuit(), (2,4))


class TestDeck(unittest.TestCase):
	
	def setUp(self):
		self.d = Deck()
	
	def test_dealHand_size(self):
		self.d.dealHand(self.d.north)
		total_num_cards = 0
		for i in range(1,5):
			total_num_cards += len(self.d.north.cards[i])
		self.assertEqual(total_num_cards, 13)		

	def test_dealHand_valid_cards(self):
		self.d.dealHand(self.d.north)
		card_names = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5",
					  "4", "3", "2"]
		for i in range(1,5):
			for c in self.d.north.cards[i]:
				self.assertTrue(c in card_names)
	
	def test_deal(self):
		self.d.deal()
		total_cards_remaining = 0
		for i in range(1,5):
			total_cards_remaining += len(self.d.deck[i])
		self.assertEqual(total_cards_remaining, 0)

if __name__ == '__main__':
	unittest.main()
