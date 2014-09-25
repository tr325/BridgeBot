from DeckUtils import *

class Convention(object):
	# Abstract parent class for all Convention objects
		
	def __init__(self, hand):
		self.hand = hand
		self.myBids = []
	
	def getBid(self, bidLevel, isOpener, psHand):
		# needs psHand to know what's going on! 
		# also it's own bidding history? keep record in self.myBids
		if isOpener:
			bid = self.getOpenersBid(bidLevel, psHand)
		else:
			bid = self.getRespondersBid(bidLevel, psHand)
		if bid.level != 0:
			self.myBids.append(bid)
		return bid
	
	def nextBidLevel(self, bidLevel, suit):
		if bidLevel.suit < suit:
			return bidLevel.level
		else:
			return bidLevel.level + 1
			
class LosingTrickCount(Convention):
	
	pLosingCount = 0
	
	def interpretPsBid(self, bidLevel, isPOpener, psHand):
		if self.hasFoundFit(bidLevel, psHand) and bidLevel.suit == psHand.info["fitSuit"]:
			if isPOpener:
				# assumes 9 losers in this hand
				self.pLosingCount = 18 - psBid.level - 9
			else: 
				# assumes 7 losers in this hand
				self.pLosingCount = 18 - psBid.level - 7
			return True
		else:
			return True
	
	def hasFoundFit(self, psBid, psHand):
		if psHand.info["fitSuit"] != 0:
			return True
		elif len(self.myBids) != 0 and psBid.suit == self.myBids[len(self.myBids) - 1]:
			psHand.info["fitSuit"] == psBid.suit
			return True
		else:
			return False
	
	def countLosingTricks(self):
		count = 0
		hCards = ["A", "K", "Q"]
		for sInd in self.hand.cards:
			x = min(3, len(self.hand.cards[sInd]))
			print "x = ", x
			hC = hCards[0:x]
			print "hC = ", hC
			for c in self.hand.cards[sInd]:
				if c in hC:
					x = x - 1
			count += x
			print "count = ", count
		print "LTCount = ", count
		return count
		
	def getBid(self, bidLevel, isPOpener, psHand):
		if self.hasFoundFit(bidLevel, psHand):
			myLTs = self.countLosingTricks()
			if self.pLosingCount == 0:
				if isPOpener:
					self.pLosingCount = 7
				else:
					self.pLosingCount = 9
			maxBidLevel = 18 - myLTs - self.pLosingCount
			if maxBidLevel >= self.nextBidLevel(bidLevel, psHand.info["fitSuit"]):
				self.myBids.append(Bid(psHand.info["fitSuit"], maxBidLevel))
				return Bid(psHand.info["fitSuit"], maxBidLevel)
			else:
				self.myBids.append(Bid(0,0))
				return Bid(0,0)
		else:
			self.myBids.append(Bid(0,0))
			return Bid(0,0)
				
		
class NormalBidding(Convention):
	
	minOpenPts = 13
	maxOpenPts = 15
	minRespPts = 7
	maxRespPts = 11
	ntRespPts = 12
	
	def interpretPsBid(self, psBid, isPOpener, psHand):
		if psHand.info["numBids"] == 0:
			return self.interpretFirstBid(psBid, isPOpener, psHand)
		elif psHand.info["numBids"] == 1:
			return self.interpretSecondBid(psBid, isPOpener, psHand)
		else:
			return self.interpretFurtherBids()
		
	def interpretFirstBid(self, psBid, isPOpener, psHand):	
		if isPOpener:
			if psBid.level == 0:
				psHand.info["maxPoints"] = 12
				return True
			elif psBid.level == 1 and psBid.suit != 5:
				psHand.info["maxPoints"] = self.maxOpenPts
				psHand.info["minPoints"] = self.minOpenPts
				psHand.info["bestSuit"] = psBid.suit
				psHand.info["bestSuitLength"] = 4
				#print "Partner opened Normal Bidding"
				return True
			else:
				return False
		elif (not isPOpener):
			if psBid.level == 0:
				psHand.info["maxPoints"] = self.minRespPts - 1			
			elif psBid.suit != 5:
				psHand.info["maxPoints"] = self.maxRespPts
				psHand.info["minPoints"] = self.minRespPts
				psHand.info["bestSuit"] = psBid.suit
				psHand.info["bestSuitLength"] = 4
				#print "Partner responded Normal Bidding"
				return True
			if psBid.suit == 5:
				psHand.info["minPoints"] = self.ntRespPts
				if psHand.info["maxPoints"] == 0:
					psHand.info["maxPoints"] = 20	#placeholder
				#print "Partner responded NT Normal Bidding"
				return True
		
	def getOpenersBid(self, bidLevel, psHand):
		if len(self.myBids) == 0:
			return self.getFirstOBid()
		elif len(self.myBids) == 1:
			return self.getSecondOBid(bidLevel, psHand)
		else:
			return Bid(0,0)
		
	def getSecondOBid(self, bidLevel, psHand):
		if psHand.info["bestSuit"] != 0:
			if self.hand.findBestSuit()[1] >= 6:
				return Bid(self.myBids[0].suit, self.nextBidLevel(bidLevel, self.myBids[0].suit))
			elif self.hand.findSecondSuit()[0] != 0:
				return Bid(self.hand.findSecondSuit()[0], self.nextBidLevel(bidLevel, self.hand.findSecondSuit()[0]))
			elif self.hand.getSuitLength(psHand.info["bestSuit"]) == 3:
				return Bid(0,0)
			else:
				return Bid(5, self.nextBidLevel(bidLevel, 5))
		else:
			return Bid(0,0)
				
	def	getFirstOBid(self):
		if self.hand.getTotalPoints() >= self.minOpenPts and self.hand.getTotalPoints() <= self.maxOpenPts:
			return Bid(self.hand.findBestSuit()[0], 1)
		else:
			return Bid(0,0)
	
	def getRespondersBid(self, bidLevel, psHand):
		if len(self.myBids) == 0:
			return self.getFirstRBid(bidLevel, psHand)
		elif len(self.myBids) == 1:
			return self.getSecondRBid(bidLevel, psHand)
		else:
			return Bid(0,0)
			
	def getFirstRBid(self, bidLevel, psHand):
		if self.hand.getTotalPoints() >= self.minRespPts and self.hand.getTotalPoints() <= self.maxRespPts:
			if self.hand.findBestSuit()[0] == psHand.info["bestSuit"]:
				psHand.info["fitSuit"] = self.hand.findBestSuit()[0]
			return Bid(self.hand.findBestSuit()[0], self.nextBidLevel(bidLevel, self.hand.findBestSuit()[0]))
		elif self.hand.getTotalPoints() >= self.ntRespPts:
			return Bid(5, self.nextBidLevel(bidLevel, 5))
		else:
			return Bid(0,0)
	
	def getSecondRBid(self, bidLevel, psHand):
		return Bid(0,0)
		
	def interpretFurtherBids(self):
		return Bid(0,0)


#########  These are old! Update from normalBidding convention for a template of how the bidding will work!  ############### 
	 
class Weak2s(Convention):
	
	minOpenPts = 7
	maxOpenPts = 11
	openLength = 6
	
	def getBid(self, currentBid, isOpener, psHand):
		if isOpener:
			return self.getOpeningBid(currentBid)
		else: 
			return (0,0)
	
	def getOpeningBid(self, currentBid):
		if self.hand.findLength()[1] < self.openLength:
			return (0,0)
		elif currentBid[1] >= 2:
			return (0,0)
		elif self.hand.findLength()[0] <= currentBid[0]:
			return (0,0)
		elif (self.hand.getTotalPoints() < self.minOpenPts) or (self.hand.getTotalPoints() > self.maxOpenPts):
			return (0,0)
		else:
			return (self.hand.findLength()[0], 2)
		
class Strong2C(Convention):
	
	minOpenPts = 20
	
	def getBid(self, currentBid, isOpener):
		if isOpener and (self.hand.getTotalPoints() >= self.minOpenPts):
			return (1, 2)
		else:
			return (0,0)
				
				
