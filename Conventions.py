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
		if bid != (0,0):
			self.myBids.append(bid)
		return bid
	
	def nextBidLevel(self, bidLevel, suit):
		if bidLevel[0] < suit:
			return bidLevel[1]
		else:
			return bidLevel[1] + 1

class NormalBidding(Convention):
	
	minOpenPts = 13
	maxOpenPts = 15
	minRespPts = 7
	maxRespPts = 11
	
	def getOpenersBid(self, bidLevel, psHand):
		if len(self.myBids) == 0:
			return self.getOpeningBid()
		else:
			return (0,0)
	
	def	getOpeningBid(self):
		if self.hand.getTotalPoints() >= self.minOpenPts and self.hand.getTotalPoints() <= self.maxOpenPts:
			return (self.hand.findLength()[0], 1)
		else:
			return (0,0)
	
	def getRespondersBid(self, bidLevel, psHand):
		if len(self.myBids) == 0:
			return self.getRespondingBid(bidLevel)
		else:
			return (0,0)
			
	def getRespondingBid(self, bidLevel):
		if self.hand.getTotalPoints() >= self.minRespPts and self.hand.getTotalPoints() <= self.maxRespPts:
			return (self.hand.findLength()[0], self.nextBidLevel(bidLevel, self.hand.findLength()[0]))
		else:
			return (0,0)


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
				
				
