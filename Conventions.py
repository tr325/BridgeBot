class Convention(object):
	# Abstract parent class for all Convention objects
		
	def __init__(self, hand):
		self.hand = hand
	
	def getBid(self, currentBid, isOpener):
		print "Error: no bid made"

class Weak2s(Convention):
	
	minOpenPts = 7
	maxOpenPts = 11
	openLength = 6
	
	def getBid(self, currentBid, isOpener):
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
				
				
