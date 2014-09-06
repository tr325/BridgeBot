from DeckUtils import *
from Conventions import *		
	
class PartnersHandInfo(object):
	# Contains information known about a BidBot partner's hand
	# Store information in a dict with keys taken from a smallish list of useful info
	
	def __init__(self):
		self.info = {}
	
	
class Table(object):
	# Contains bidding history information and player positions
	bidLevel = (0,0)
			
	def __init__(self):
		self.deck = Deck()
		self.bidHist = BidHistory()
		self.deck.deal()
		self.north = BidBot(self.deck.north)
		self.east = BidBot(self.deck.east)
		self.south = BidBot(self.deck.south)
		self.west = BidBot(self.deck.west)
		self.players = [self.north, self.east, self.south, self.west]	
		self.partners = [self.south, self.west, self.north, self.east]
	
	def bidding(self):
		i = 0
		while (True):
			pNum = (i % 4) # ensures correct looping of players
			i += 1
			currentBid = self.players[pNum].bid()
			if (currentBid != (0,0) and (self.players[pNum].isOpener)):
				self.partners[pNum].isOpener = False
			self.partners[pNum].addPartnersBid(currentBid, self.players[pNum].isOpener)
			self.bidLevel = currentBid
			print self.players[pNum].hand.cards
			print "Bidding currentBid is: ", currentBid, ", and isOpener = ", self.players[pNum].isOpener
			print ""
			self.bidHist.addBid(currentBid)
			if self.bidHist.isBiddingFinished():
				print self.bidHist.pastBids
				break

class BidBot(object):
	# Carries out the bidding for a hand.
	
	########  Should contain: #######
	# List of convention objects (populated in __init__)
	# knowledge of P's hand in PartnersHandInfo object
	# knowledge of opener/responder (in __init__)
	
	def __init__(self, hand):
		self.hand = hand
		self.psHand = PartnersHandInfo()
		self.isOpener = True
		self.weak2s = Weak2s(self.hand)
		self.strong2C = Strong2C(self.hand)
		self.conventions = []
		self.conventions.append(self.weak2s)
		self.conventions.append(self.strong2C)
				
	def bid(self):
		for conv in self.conventions:
			convBid = conv.getBid( (0,0), self.isOpener )
			if convBid != (0,0):
				return convBid
		return (0,0)
	
	def addPartnersBid(self, pBid, isPOpener):
		if isPOpener and pBid != (0,0):
			self.isOpener = False
			

t = Table()
t.bidding()













