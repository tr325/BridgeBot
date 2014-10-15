from DeckUtils import Deck
from DeckUtils import Hand
from DeckUtils import Bid
from DeckUtils import BidHistory


class Convention(object):
	"""Abstract parent class for all Convention objects."""
	
	def __init__(self, hand):
		"""Initialise a Convention Object."""
		self.hand = hand
		self.mySuitsBid = []
		self.myBids = []
	
	def getBid(self, psBid, bidLevel, isOpener, psHand):
		"""Return the next bid from this hand."""		
		# needs psHand information 
		# record suits this hand has bid previously in self.mySuitsBid[]
		# record all bids in self.myBids[]
		if isOpener:
			bid = self.getOpenersBid(psBid, bidLevel, psHand)
		else:
			bid = self.getRespondersBid(psBid, bidLevel, psHand)
		if bid.level != 0:
			self.myBids.append(bid)
			if bid.suit != 5:
				self.mySuitsBid.append(bid.suit)
		return bid
	
	def nextBidLevel(self, bidLevel, suit):
		"""Return the next legal level at which a suit can be bid."""
		if bidLevel.level == 0:
			return 1
		elif bidLevel.suit < suit:
			return bidLevel.level
		else:
			return bidLevel.level + 1
	
	def hasFoundFit(self, psHand):
		"""Return True if a fit has been found, else return False."""
		#print "checking for fit"
		if psHand.info["fitSuit"] != 0:
			return True
		pBL = psHand.info["bestSuitLength"]
		if self.hand.getSuitLength(psHand.info["bestSuit"]) + pBL >= 8:
			psHand.info["fitSuit"] = psHand.info["bestSuit"]
			return True
		elif self.hand.getSuitLength(psHand.info["secondSuit"]) >= 4:
			psHand.info["fitSuit"] = psHand.info["secondSuit"]
			return True
		elif self.hand.getSuitLength(psHand.info["thirdSuit"]) >= 4:
			psHand.info["fitSuit"] = psHand.info["thirdSuit"]
			return True
		else:
			return False
	
	def bidBailOut(self, bidLevel, psHand):
		"""Return a bailing bid when no fit has been found."""
		pBest = psHand.info["bestSuit"]
		pSecond = psHand.info["secondSuit"]
		if self.hand.getSuitLength(pBest) == 3:
			return Bid(pbest, self.nextBidLevel(bidLevel, pBest))
		elif self.hand.getSuitLength(pSecond) == 3:
			return Bid(pSecond, self.nextBidLevel(bidLevel, pSecond))
		elif (psHand.info["bestSuitLength"] == 6 and
				self.hand.getSuitLength(pBest) == 1):
			return Bid(pBest, self.nextBidLevel(bidLevel, pBest))
		else:
			return Bid(5, self.nextBidLevel(bidLevel, 5))

class LosingTrickCount(Convention):
	"""Convention class for Losing Trick Count."""	
	pLosingCount = 0
	pHasBidLTC = False
	
	def interpretPsBid(self, bidLevel, isPOpener, psHand):
		"""Interpret partner's losing trick count bid."""
		fitFound = self.hasFoundFit(psHand)
		if (fitFound and bidLevel.suit == psHand.info["fitSuit"] and 
		        (not self.pHasBidLTC)):
		   	if (not self.pHasBidLTC) and self.pLosingCount != 0:
		   		self.pHasBidLTC = True
			if isPOpener:
				# partner assumes 9 losers in this hand
				self.pLosingCount = 18 - bidLevel.level - 9
			else: 
				# partner assumes 7 losers in this hand
				self.pLosingCount = 18 - bidLevel.level - 7
			
			return True
		else:
			return True
	
	def countLosingTricks(self):
		"""Carry out the standard losing trick count."""
		count = 0
		hCards = ["A", "K", "Q"]
		for sInd in self.hand.cards:
			x = min(3, len(self.hand.cards[sInd]))
			hC = hCards[0:x]
			for c in self.hand.cards[sInd]:
				if c in hC:
					x = x - 1
			count += x
		return count
		
	def getBid(self, bidLevel, isOpener, psHand):
		"""Return the next bid for this hand.
		
		Overrides the parent class method.
		"""
		if self.hasFoundFit(psHand):
			myLTs = self.countLosingTricks()
			if self.pLosingCount == 0:
				if isOpener:
					#print "Assume p has 9 losers"
					self.pLosingCount = 9
				else:
					#print "Assume p has 7 losers"
					self.pLosingCount = 7
			maxBidLevel = 18 - myLTs - self.pLosingCount
			#print "I have ", myLTs, "losing tricks, and p has ", self.pLosingCount
			#print "Bid up to ", maxBidLevel
			#print "Next bid level is ", self.nextBidLevel(bidLevel, psHand.info["fitSuit"])
			if maxBidLevel >= self.nextBidLevel(bidLevel, 
			                                    psHand.info["fitSuit"]):
				self.myBids.append(Bid(psHand.info["fitSuit"], maxBidLevel))
				return Bid(psHand.info["fitSuit"], maxBidLevel)
			else:
				self.myBids.append(Bid(0,0))
				return Bid(0,0)
		else:
			self.myBids.append(Bid(0,0))
			return Bid(0,0)
				
		
class NormalBidding(Convention):
	""""Convention class for normal bidding (to find fit, etc.)."""
	minOpenPts = 13
	maxOpenPts = 15
	minRespPts = 7
	ntRespPts = 12
	
	def interpretPsBid(self, psBid, isPOpener, psHand):
		"""Interpret partner's normal bidding bid."""
		if psHand.info["numBids"] == 0:
			return self.interpretFirstBid(psBid, isPOpener, psHand)
		else:
			return self.interpretFurtherBids(psBid, psHand)
		
	def interpretFirstBid(self, psBid, isPOpener, psHand):
		"""Interpret partner's normal bid when it is their first bid."""	
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
		else:
			if psBid.level == 0:
				psHand.info["maxPoints"] = self.minRespPts - 1
				return True			
			elif psBid.suit != 5:
				psHand.info["maxPoints"] = self.ntRespPts - 1
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
		
	def interpretFurtherBids(self, psBid, psHand):
		"""Interpret further normal bidding bids."""
		if psBid.suit != 5:
			if psHand.info["bestSuit"] == 0:
				psHand.info["bestSuit"] = psBid.suit
				psHand.info["bestSuitLength"] = 4
				return True
			elif psHand.info["bestSuit"] == psBid.suit:
				if psHand.info["bestSuitLength"] == 4:
					psHand.info["bestSuitLength"] = 6
					return True
				elif psHand.info["bestSuitLength"] == 6:
					psHand.info["bestSuitLength"] = 7
					return True
				else:
					return False
			elif psHand.info["secondSuit"] == 0:
				psHand.info["secondSuit"] = psBid.suit
				return True
			elif psHand.info["thirdSuit"] == 0:
				psHand.info["thirdSuit"] = psBid.suit
				return True
			else:
				return False
		else:
			# Continuation bid - nt
			return True
			
	def getOpenersBid(self, psBid, bidLevel, psHand):
		"""Return an opening hand's normal bidding bid"""
		pts = self.hand.getTotalPoints()
		if ((pts >= self.minOpenPts) and (pts <= self.maxOpenPts) and 
				(not self.hasFoundFit(psHand))):
			#print "number of suits bid = ", len(self.mySuitsBid)
			bestSuit = self.hand.findBestSuit()
			secondSuit = self.hand.findSecondSuit()
			#thirdSuit = self.hand.findThirdSuit()  # Haven't written this yet!
			if len(self.mySuitsBid) == 0:
				return Bid(bestSuit[0], self.nextBidLevel(bidLevel, 
														  bestSuit[0]))
			elif len(self.mySuitsBid) == 1:
				if (self.mySuitsBid[0] == bestSuit[0] and 
						bestSuit[1] < 6):
					return Bid(secondSuit[0], 
							 self.nextBidLevel(bidLevel, secondSuit[0]))
				elif (self.mySuitsBid[0] == bestSuit[0] and 
						bestSuit[1] >= 6):
					return Bid(bestSuit[0], 
							   self.nextBidLevel(bidLevel, bestSuit[0]))
				elif (self.mySuitsBid[0] == secondSuit[0] and 
						secondSuit[1] < 6):
					return Bid(bestSuit[0], 
							   self.nextBidLevel(bidLevel, bestSuit[0]))
				elif (self.mySuitsBid[0] == secondSuit[0] and 
						secondSuit[1] >= 6):
					return Bid(secondSuit[0], self.nextBidLevel(bidLevel, 
																secondSuit[0]))
			elif len(self.mySuitsBid) == 2:
				# two suits have been bid and no fit found
				bailBid = self.bidBailOut(psBid, psHand)
				totalPts = pts + (psHand.info["minPoints"] +
								  psHand.info["maxPoints"])/2.0
				if psBid.suit == bailBid.suit and totalPts > 24.5:
					return bailBid
				elif psBid.suit != bailBid.suit:
					return bailBid
				else:
					return Bid(0,0)				
			else:
				return Bid(0,0)
		else:
			return Bid(0,0)
				
	def getRespondersBid(self, psBid, bidLevel, psHand):
		"""Return a responder's normal bidding bid"""
		pts = self.hand.getTotalPoints()
		bestSuit = self.hand.findBestSuit()
		secondSuit = self.hand.findSecondSuit()
		pBest = psHand.info["bestSuit"]
		pSecond = psHand.info["secondSuit"]  # can be 0 (ie. not set)
		if pts < self.minRespPts:
			return Bid(0,0)
		else:
			if len(self.myBids) == 0:
				if pts >= self.ntRespPts:
					return Bid(5, self.nextBidLevel(bidLevel, 5))
				elif (not self.hasFoundFit(psHand)):
					return Bid(bestSuit[0], 
							   self.nextBidLevel(bidLevel, bestSuit[0]))
				else:
					return Bid(0,0)
			else:
				if (len(self.mySuitsBid) == 0 and 
						(not self.hasFoundFit(psHand))):
					return Bid(bestSuit[0],
							   self.nextBidLevel(bidLevel, bestSuit[0]))
				elif (len(self.mySuitsBid) != 0 and
						(not self.hasFoundFit(psHand)) and
						bestSuit[1] >= 6):
					return Bid(bestSuit[0],
							   self.nextBidLevel(bidLevel, bestSuit[0]))
				elif (len(self.mySuitsBid) != 0 and
						(not self.hasFoundFit(psHand)) and
						bestSuit[1] < 6):
					bailBid = self.bidBailOut(psBid, psHand)
					totalPts = pts + (psHand.info["minPoints"] +
									  psHand.info["maxPoints"])/2.0
					if psBid.suit == bailBid.suit and totalPts > 24.5:
						return bailBid
					elif psBid.suit != bailBid.suit:
						return bailBid
					else:
						return Bid(0,0)
				else:
					return Bid(0,0)
					
			
			 

				
