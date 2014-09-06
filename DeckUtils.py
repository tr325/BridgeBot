from random import randint

class BidHistory(object):
	# Contains history of all bidding so far at the Table
	pastBids = [[], [], [], []]
	bidPosition = 0
	numBids = 0
	
	def __init__(self):
		pass
	
	def isBiddingFinished(self):
		# REALLY FIX THIS LATER
		# returns True when three passes in a row occur
		if self.numBids >= 4:
			for i in range(0,3):
				#TRUST IT IT WORKS 
				if self.pastBids[self.bidPosition -1 - i][len(self.pastBids[self.bidPosition -1- i]) - 1] != (0, 0):
					break
			else:
				return True
			return False
		else:
			return False

	def addBid(self, newBid):
		# adds the new bid onto the bid history
		self.pastBids[self.bidPosition].append(newBid)
		self.bidPosition = (self.bidPosition + 1) % 4
		self.numBids += 1

		
class Deck(object):
	
	# Maybe not even how to do it... create a Hand() class, and input (from keyboard initially) a hand to bid
	# simplifies to jsut bidding. next create a Deck() class, and a D.shuffle() and D.deal() methods	
	
	spades = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
	hearts = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
	diamonds = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
	clubs = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
	deck = {4: spades, 3: hearts, 2: diamonds, 1: clubs}
	
	def __init__(self):
		self.north = Hand()
		self.east = Hand()
		self.west = Hand()
		self.south = Hand()

	def dealHand(self, hand):
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
		self.dealHand(self.north)
		self.dealHand(self.south)
		self.dealHand(self.east)
		self.dealHand(self.west)
		
		
class Hand(object):
	
	def __init__(self):
		self.spades = []
		self.hearts = []
		self.diamonds = []
		self.clubs = []
		self.cards = {1: self.clubs, 2: self.diamonds, 3: self.hearts, 4: self.spades}
	
	def addCard(self, suit, card):
		self.cards[suit].append(card)
	
	def getTotalPoints(self):
		points = 0
		for s in self.cards:
			for c in self.cards[s]:
				points += self.getCardPoints(c)
		return points
	
	def findLength(self):
		# Returns longest suit and number in that suit. If two suits have same length, returns stronger of the two
		maxLength = 0
		longSuit = 0
		for sInd in self.cards:
			if len(self.cards[sInd]) > maxLength:
				maxLength = len(self.cards[sInd])
				longSuit = sInd
			if len(self.cards[sInd]) == maxLength:
				if (longSuit != 0) and (self.getSuitPoints(sInd) >= self.getSuitPoints(longSuit)):
					# chooses stronger suit (by points) of two of the same length
					# if two suits have same length AND same points it chooses the higher suit (ie. favours majors)
					maxLength = len(self.cards[sInd])
					longSuit = sInd
		return (longSuit, maxLength)
		
	def getSuitLength(self, sInd):
		return len(self.cards[sInd])
	
	def getSuitPoints(self, sInd):
		suit = self.cards[sInd]
		points = 0
		for c in suit:
			points += self.getCardPoints(c)
		return points
			
	def getCardPoints(self, card):
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

