from random import randint
from collections import namedtuple

# makes a data structure for bid tuples.
Bid = namedtuple('Bid', 'suit level')

class BidHistory(object):
	"""Class to contain table bidding history and related methods."""
	# Contains history of all bidding so far at the Table
	pastBids = [[], [], [], []]
	bidPosition = 0
	numBids = 0
	
	def __init__(self):
		"""Create a BidHistory object"""
		pass
	
	def isBiddingFinished(self):
		"""Determine when bidding has finished."""
		if self.numBids >= 4:
			for i in range(0,3):
				bidInd = self.bidPosition - 1 - i
				if self.pastBids[bidInd][len(self.pastBids[bidInd]) - 1] != (0, 0):
					break
			else:
				return True
			return False
		else:
			return False

	def addBid(self, newBid):
		"""Add a bid onto the bid history."""
		self.pastBids[self.bidPosition].append(newBid)
		self.bidPosition = (self.bidPosition + 1) % 4
		self.numBids += 1
		
	def printBidding(self):
		"""Print the bidding history in a readable form."""
		suitText = ["C  ", "D  ", "H  ", "S  ", "NT "]
		while True:
			for p in self.pastBids:
				if len(p) != 0:
					bid = p.pop(0)
					if bid.level == 0:
						print "PASS",
					else:
						text = str(bid.level) + str(suitText[bid.suit - 1])
						print text,						
				else:
					return
			print ""
			

		
class Deck(object):
	"""Class containing a deck of cards, and methods to deal hands."""	
	
	def __init__(self):
		"""Initialise the deck (with four Hand objects)."""
		self.north = Hand()
		self.east = Hand()
		self.west = Hand()
		self.south = Hand()
		self.spades = ["A", "K", "Q", "J", "10", "9", "8", "7", "6",
					   "5", "4", "3", "2"]
		self.hearts = ["A", "K", "Q", "J", "10", "9", "8", "7", "6",
					   "5", "4", "3", "2"]
		self.diamonds =["A", "K", "Q", "J", "10", "9", "8", "7", "6",
					    "5", "4", "3", "2"]
		self.clubs = ["A", "K", "Q", "J", "10", "9", "8", "7", "6",
					  "5", "4", "3", "2"]
		self.deck = {4: self.spades, 3: self.hearts, 2: self.diamonds,
					 1: self.clubs}

	def dealHand(self, hand):
		"""Deal a hand from the (remaining) cards in the deck."""
		for j in range(1,14):
			suitInd = randint(1,4)
			suit = self.deck[suitInd]
			while len(suit) == 0:
				suitInd = randint(1,4)
				suit = self.deck[suitInd]
			if len(suit) > 1:
				cardInd = randint(0,len(suit) - 1)
			else:
				cardInd = 0
			card = self.deck[suitInd].pop(cardInd)
			hand.addCard(suitInd, card)

	def deal(self):
		"""Deal four hands from the deck."""
		self.dealHand(self.north)
		self.dealHand(self.south)
		self.dealHand(self.east)
		self.dealHand(self.west)
		
		
		
class Hand(object):
	"""Object for a single hand of cards, with methods for analysis of that
	hand (ie. points counting, length, etc).
	"""
	def __init__(self):
		"""Initialise the Hand object"""
		self.spades = []
		self.hearts = []
		self.diamonds = []
		self.clubs = []
		self.cards = {1: self.clubs, 2: self.diamonds, 
		              3: self.hearts, 4: self.spades}
	
	def addCard(self, suit, card):
		"""Add a card to a suit when dealing."""
		self.cards[suit].append(card)
	
	def getTotalPoints(self):
		"""Return the total number of points in the hand."""
		points = 0
		for s in self.cards:
			for c in self.cards[s]:
				points += self.getCardPoints(c)
		return points
	
	def findBestSuit(self):
		"""Return the longest suit and number of cards in that suit."""
		# If two suits have same length, returns stronger of the two
		maxLength = 0
		longSuit = 0
		for sInd in self.cards:
			if len(self.cards[sInd]) > maxLength:
				maxLength = len(self.cards[sInd])
				longSuit = sInd
			if len(self.cards[sInd]) == maxLength:
				if ((longSuit != 0) and 
				    (self.getSuitPoints(sInd) >= self.getSuitPoints(longSuit))):
					# chooses stronger suit (by points) of two of the same 
					# length. If two suits have same length AND same points it 
					# chooses the higher suit (ie. favours majors)
					maxLength = len(self.cards[sInd])
					longSuit = sInd
		return longSuit, maxLength
		
	def findSecondSuit(self):
		"""Return the second best (biddable) suit and its length.
		
		If no second biddable suit exists, returns (0,4)
		"""
		bestSuit = self.findBestSuit()[0]
		secondSuit = 0
		length = 4
		for sInd in self.cards:
			if sInd != bestSuit:
				if len(self.cards[sInd]) > length:
					length = len(self.cards[sInd])
					secondSuit = sInd
				if len(self.cards[sInd]) == length:
					if ((secondSuit != 0) and 
				  (self.getSuitPoints(sInd) >= self.getSuitPoints(secondSuit))):
						# chooses stronger suit (by points) of two of the same 
						# length. If two suits have same length AND same points 
						# it chooses the higher suit (ie. favours majors).
						secondSuit = sInd
					elif secondSuit == 0:
						secondSuit = sInd
						
		return secondSuit, length
	
	def getSuitLength(self, sInd):
		"""Return the number of cards in a suit."""
		if sInd == 0:
			return 0  	# safeguard against checking suits p hasn't bid
		else:
			return len(self.cards[sInd])
	
	def getSuitPoints(self, sInd):
		"""Return the number of points in a suit."""
		suit = self.cards[sInd]
		points = 0
		for c in suit:
			points += self.getCardPoints(c)
		return points
			
	def getCardPoints(self, card):
		"""Get the number of points for a single card."""
		points = 0
		if card == "A":
			points = 4
		if card == "K":
			points = 3
		if card == "Q":
			points = 2
		if card == "J":
			points = 1
		return points

