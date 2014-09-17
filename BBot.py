from Conventions import *		
	
class PartnersHandInfo(object):
	# Contains information known about a BidBot partner's hand
	# Store information in a dict with keys taken from a smallish list of useful info
	# Use a dict so it's iterable
	
	def __init__(self):
		self.info = {}
		self.info["numBids"] = 0
		self.info["maxPoints"] = 0
		self.info["minPoints"] = 0
		self.info["bestSuit"] = 0
		self.info["bestSuitLength"] = 0
		self.info["secondSuit"] = 0
		self.info["thirdSuit"] = 0
		self.info["singletonSuit"] = 0
	
	
class Table(object):
	# Contains bidding history information and player positions
	bidLevel = Bid(0,0)
			
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
			currentBid = self.players[pNum].bid(self.bidLevel)
			
			if currentBid.level != 0:
				self.bidLevel = currentBid
				self.partners[pNum].addPartnersBid(currentBid, self.players[pNum].isOpener)
			#print self.players[pNum].hand.cards
			#print currentBid
			#print ""
			self.bidHist.addBid(currentBid)
			if self.bidHist.isBiddingFinished():
				for i in range(0,4):
					print self.players[i].hand.cards
				self.bidHist.printBidding()
				
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
		self.normalBidding = NormalBidding(self.hand)
		self.conventions = []
		self.conventions.append(self.normalBidding)
		#self.conventions.append(self.weak2s)
		#self.conventions.append(self.strong2C)
				
	def bid(self, bidLevel):
		for conv in self.conventions:
			convBid = conv.getBid(bidLevel, self.isOpener, self.psHand )
			if convBid.level != 0:
				return convBid
		return Bid(0,0)
	
	def addPartnersBid(self, pBid, isPOpener):
		if isPOpener and pBid.level != 0:
			self.isOpener = False
		for conv in self.conventions:
			# evaluates bids from possible list of conventions, updating pshandinfo
			if (not conv.interpretPsBid(pBid, isPOpener, self.psHand) ):
				# removes conventions if bidding has ruled them out (ie. if opening bid is 1s, the Weak2s convention returns False)
				self.conventions.remove(conv)
			

t = Table()
t.bidding()













