import Conventions
import BBot
from DeckUtils import Hand
from DeckUtils import Bid
import unittest


class test_Convention(unittest.TestCase):
	
	def setUp(self):
		self.hand = Hand()
		self.conv = Conventions.Convention(self.hand)
		self.partner_hand_info = BBot.PartnersHandInfo()
		self.hand.cards[1] = ["10", "9", "7"]
		self.hand.cards[2] = ["A", "6", "5", "3"]
		self.hand.cards[3] = ["Q", "J", "8", "3", "2"]
		self.hand.cards[4] = ["Q"]
		self.partner_hand_info.info["fitSuit"] = 1
		self.partner_hand_info.info["bestSuitLength"] = 6
		self.partner_hand_info.info["bestSuit"] = 1
		self.partner_hand_info.info["secondSuit"] = 2
		self.partner_hand_info.info["thirdSuit"] = 0
	
	def test_nextBidLevel(self):
		self.assertEqual(self.conv.nextBidLevel(Bid(1,1),1), 2)
		self.assertEqual(self.conv.nextBidLevel(Bid(1,1),2), 1)
	
	def test_hasFoundFit_fitSuit(self):
		self.assertTrue(self.conv.hasFoundFit(self.partner_hand_info))
		
	def test_hasFoundFit_six_and_three(self):	
		self.partner_hand_info.info["fitSuit"] = 0
		self.assertTrue(self.conv.hasFoundFit(self.partner_hand_info))
		
	def test_hasFoundFit_four_and_four(self):
		self.partner_hand_info.info["fitSuit"] = 0
		self.partner_hand_info.info["bestSuitLength"] = 4
		self.assertTrue(self.conv.hasFoundFit(self.partner_hand_info))
		
	def test_hasFoundFit_no_fit(self):
		self.partner_hand_info.info["fitSuit"] = 0
		self.partner_hand_info.info["bestSuitLength"] = 4
		self.partner_hand_info.info["secondSuit"] = 4
		self.assertFalse(self.conv.hasFoundFit(self.partner_hand_info))
	
	def test_bidBailOut(self):
		self.partner_hand_info.info["bestSuit"] = 4
		self.partner_hand_info.info["secondSuit"] = 0
		bailout_bid = self.conv.bidBailOut(Bid(0,0), 
										   self.partner_hand_info)
		self.assertTrue(bailout_bid, Bid(4,1))
		self.partner_hand_info.info["bestSuitLength"] = 4
		self.partner_hand_info.info["secondSuit"] = 1
		bailout_bid = self.conv.bidBailOut(Bid(0,0), 
										   self.partner_hand_info)
		self.assertTrue(bailout_bid, Bid(1,1))		
		self.partner_hand_info.info["secondSuit"] = 0
		bailout_bid = self.conv.bidBailOut(Bid(0,0), 
										   self.partner_hand_info)
		self.assertTrue(bailout_bid, Bid(5,1))


class test_NormalBidding(unittest.TestCase):
	"""Class testing the methods in the NormalBidding convention.
	
	NOTE: NormalBidding should return Bid(0,0) if a fit is found at any
	point.  These situations should be handled by LosingTrickCount"""
	
	def setUp(self):
		self.responders_hand_info = BBot.PartnersHandInfo()
		self.openers_hand_info = BBot.PartnersHandInfo()
		self.opening_hand = Hand()
		self.opening_hand.cards[1] = ["A", "K"]
		self.opening_hand.cards[2] = ["K", "Q", "10", "8"]
		self.opening_hand.cards[3] = ["K", "9", "5", "4"]
		self.opening_hand.cards[4] = ["10", "6", "2"]
		self.responding_hand = Hand()
		self.responding_hand.cards[1] = ["10", "9"]
		self.responding_hand.cards[2] = ["A", "7", "6", "5", "3"]
		self.responding_hand.cards[3] = ["Q", "J", "8", "3", "2"]
		self.responding_hand.cards[4] = ["Q"]
		self.normal_opener = Conventions.NormalBidding(
									self.opening_hand)
		self.normal_responder = Conventions.NormalBidding(
									self.responding_hand)
	
	def test_interpretPsBid_openers_first_bid(self):
		self.normal_responder.interpretPsBid(Bid(2,1), True, 
											 self.openers_hand_info)
		self.assertEqual(self.openers_hand_info.info["bestSuit"], 2)
		self.assertEqual(
					self.openers_hand_info.info["bestSuitLength"], 4)
		self.assertEqual(self.openers_hand_info.info["maxPoints"], 15)
		self.assertEqual(self.openers_hand_info.info["minPoints"], 13)
		
	def test_interpretPsBid_opener_passes(self):
		self.normal_responder.interpretPsBid(Bid(0,0), True,
											 self.openers_hand_info)
		self.assertEqual(self.openers_hand_info.info["maxPoints"], 12)
	
	def test_interpretPsBid_responder_first_bid_normal_points(self):
		self.normal_opener.interpretPsBid(Bid(2,1), False,
										  self.responders_hand_info)
		self.assertEqual(self.responders_hand_info.info["bestSuit"], 2)
		self.assertEqual(
				   self.responders_hand_info.info["bestSuitLength"], 4)
		self.assertEqual(self.responders_hand_info.info["maxPoints"], 
						 11)
		self.assertEqual(self.responders_hand_info.info["minPoints"], 
						 7)
	
	def test_interpretPsBid_responder_passes(self):
		self.normal_opener.interpretPsBid(Bid(0,0), False, 
										  self.responders_hand_info)
		self.assertEqual(self.responders_hand_info.info["maxPoints"], 
						 6)
						 
	def test_interpretPsBd_responder_nt_points(self):
		self.normal_opener.interpretPsBid(Bid(5,1), False,
										  self.responders_hand_info)
		self.assertEqual(self.responders_hand_info.info["minPoints"], 
						 12)
						 		
	def test_interpretPsBid_opener_restate(self):
		self.openers_hand_info.info["numBids"] = 1
		self.openers_hand_info.info["bestSuit"] = 2
		self.openers_hand_info.info["bestSuitLength"] = 4
		self.normal_responder.interpretPsBid(Bid(2,2), True, 
											 self.openers_hand_info)
		self.assertEqual(self.openers_hand_info.info["bestSuitLength"],
				         6)
	
	def test_interpretPsBid_opener_second_suit(self):
		self.openers_hand_info.info["numBids"] = 1
		self.openers_hand_info.info["bestSuit"] = 2
		self.openers_hand_info.info["bestSuitLength"] = 4
		self.normal_responder.interpretPsBid(Bid(1,2), True,
											 self.openers_hand_info)
		self.assertEqual(self.openers_hand_info.info["secondSuit"], 1)
		
	def test_interpretPsBid_responder_restate(self):
		self.responders_hand_info.info["numBids"] = 1
		self.responders_hand_info.info["bestSuit"] = 3
		self.responders_hand_info.info["bestSuitLength"] = 4
		self.normal_opener.interpretPsBid(Bid(3,2), False, 
										  self.responders_hand_info)
		self.assertEqual(
				   self.responders_hand_info.info["bestSuitLength"], 6)

	def test_interpretPsBid_responder_nt_points_second_bid(self):
		self.responders_hand_info.info["numBids"] = 1
		self.responders_hand_info.info["minPoints"] = 12
		self.normal_opener.interpretPsBid(Bid(3,2), False,
										  self.responders_hand_info)
		self.assertEqual(
				   self.responders_hand_info.info["bestSuitLength"], 4)
		self.assertEqual(self.responders_hand_info.info["bestSuit"], 3)
		self.assertEqual(self.responders_hand_info.info["minPoints"],
						 12)
		
	def test_getOpenersBid_first_bid(self):
		first_opener = self.normal_opener.getBid(Bid(0,0), Bid(0,0), 
									True, self.responders_hand_info)
		self.assertEqual(first_opener, Bid(2,1))
		
	def test_getOpenersBid_second_bid_second_suit(self):
		self.normal_opener.mySuitsBid.append(2)
		self.responders_hand_info.info["bestSuit"] = 4
		self.responders_hand_info.info["bestSuitLength"] = 4
		second_opener = self.normal_opener.getBid(Bid(4,1), Bid(4,1),
									True, self.responders_hand_info)
		self.assertEqual(second_opener, Bid(3,2))
		
	def test_getOpenersBid_second_bid_restate_suit(self):
		self.normal_opener.mySuitsBid.append(2)
		self.responders_hand_info.info["bestSuit"] = 4
		self.responders_hand_info.info["bestSuitLength"] = 4
		self.opening_hand.cards[2] = ["K", "Q", "10", "8", "6", "2"]
		self.opening_hand.cards[4] = ["10"]
		second_opener_restate = self.normal_opener.getBid(Bid(4,1), 
							Bid(4,1), True, self.responders_hand_info)
		self.assertEqual(second_opener_restate, Bid(2,2))
		
	def test_getOpenersBid_previously_found_fit(self):
		self.responders_hand_info.info["fitSuit"] = 2
		opener_found_fit = self.normal_opener.getBid(Bid(2,2), 
							Bid(2,2), True, self.responders_hand_info)
		self.assertEqual(opener_found_fit, Bid(0,0))
		
	def test_getOpenersBid_find_fit(self):
		self.normal_opener.mySuitsBid.append(2)
		self.responders_hand_info.info["fitSuit"] = 0
		self.responders_hand_info.info["bestSuit"] = 2
		self.responders_hand_info.info["bestSuitLength"] = 4
		opener_find_fit = self.normal_opener.getBid(Bid(2,2), 
							Bid(2,2), True, self.responders_hand_info)
		self.assertEqual(opener_find_fit, Bid(0,0))
		
	def test_getOpenersBid_not_enough_points(self):
		opener_no_points = self.normal_responder.getBid(Bid(0,0), 
								Bid(0,0), True, self.openers_hand_info)
		self.assertEqual(opener_no_points, Bid(0,0))
	
	def test_getRespondersBid_first_bid_normal_points_no_fit(self):
		self.openers_hand_info.info["bestSuit"] = 1
		first_response = self.normal_responder.getBid(Bid(1,1), 
							   Bid(1,1), False, self.openers_hand_info)
		self.assertEqual(first_response, Bid(2,1))
	
	def test_getRespondersBid_first_bid_normal_points_first_fit(self):
		self.openers_hand_info.info["bestSuit"] = 2
		self.openers_hand_info.info["bestSuitLength"] = 4
		first_fit_response = self.normal_responder.getBid(Bid(2,1),
							   Bid(2,1), False, self.openers_hand_info)
		self.assertEqual(first_fit_response, Bid(0,0))
	
	def test_getRespondersBid_first_bid_nt_points(self):
		self.openers_hand_info.info["bestSuit"] = 2
		self.responding_hand.cards[1] = ["A", "9"]
		first_nt_response = self.normal_responder.getBid(Bid(2,1),
							   Bid(2,1), False, self.openers_hand_info)
		self.assertEqual(first_nt_response, Bid(5,1))
		
	def test_getRespondersBid_second_bid_nt_points_no_fit(self):
		self.openers_hand_info.info["bestSuit"] = 4
		self.openers_hand_info.info["secondSuit"] = 1
		self.responding_hand.cards[1] = ["A", "9"]
		self.normal_responder.myBids.append(Bid(5,1))
		second_nt_response_no_fit = self.normal_responder.getBid(
					Bid(1,2), Bid(1,2), False, self.openers_hand_info)
		self.assertEqual(second_nt_response_no_fit, Bid(2,2))
		
	def test_getRespondersBid_second_nt_points_with_fit(self):
		#  this will be handled by GameForcing convention
		self.openers_hand_info.info["bestSuit"] = 2
		self.openers_hand_info.info["secondSuit"] = 1
		self.openers_hand_info.info["bestSuitLength"] = 4
		self.responding_hand.cards[1] = ["A", "9"]
		self.normal_responder.myBids.append(Bid(5,1))
		second_nt_response_with_fit = self.normal_responder.getBid(
					Bid(1,2), Bid(1,2), False, self.openers_hand_info)
		self.assertEqual(second_nt_response_with_fit, Bid(0,0))
	
	def test_getRespondersBid_second_bid_sixtimer(self):
		self.openers_hand_info.info["bestSuit"] = 1
		self.openers_hand_info.info["secondSuit"] = 4
		self.responding_hand.cards[1] = ["9"]
		self.responding_hand.cards[2] = ["A", "10" ,"7", "6", "5", "3"]
		self.normal_responder.myBids.append(Bid(2,1))
		self.normal_responder.mySuitsBid.append(2)
		second_response_sixtimer = self.normal_responder.getBid(
					Bid(4,1), Bid(4,1), False, self.openers_hand_info)
		self.assertEqual(second_response_sixtimer, Bid(2,2))
	
	def test_getRespondersBid_second_bid_find_fit(self):
		self.openers_hand_info.info["bestSuit"] = 1
		self.openers_hand_info.info["bestSuitLength"] = 4
		self.openers_hand_info.info["secondSuit"] = 3
		self.normal_responder.myBids.append(Bid(2,1))
		self.normal_responder.mySuitsBid.append(2)
		second_response_find_fit= self.normal_responder.getBid(
					Bid(3,2), Bid(3,2), False, self.openers_hand_info)
		self.assertEqual(second_response_find_fit, Bid(0,0))
									   

class test_LosingTrickCount(unittest.TestCase):
	
	def setUp(self):
		self.responders_hand_info = BBot.PartnersHandInfo()
		self.openers_hand_info = BBot.PartnersHandInfo()
		self.opening_hand = Hand()
		self.opening_hand.cards[1] = ["A", "K"]
		self.opening_hand.cards[2] = ["K", "Q", "10", "8"]
		self.opening_hand.cards[3] = ["K", "9", "5", "4"]
		self.opening_hand.cards[4] = ["10", "6", "2"]
		self.responding_hand = Hand()
		self.responding_hand.cards[1] = ["10", "9"]
		self.responding_hand.cards[2] = ["A", "7", "6", "5", "3"]
		self.responding_hand.cards[3] = ["Q", "J", "8", "3", "2"]
		self.responding_hand.cards[4] = ["Q"]
		self.losing_trick_opener = Conventions.LosingTrickCount(
									self.opening_hand)
		self.losing_trick_responder = Conventions.LosingTrickCount(
									self.responding_hand)
	
	def test_countLosingTricks(self):
		losing_trick_count = self.losing_trick_opener.countLosingTricks()
		self.assertEqual(losing_trick_count, 6)
	
	def test_interpretPsBid(self):
		self.openers_hand_info.info["fitSuit"] = 2
		self.responders_hand_info.info["fitSuit"] = 2
		self.losing_trick_responder.interpretPsBid(Bid(2,3), True,
												self.openers_hand_info)
		self.assertEqual(self.losing_trick_responder.pLosingCount, 6)
		self.losing_trick_opener.interpretPsBid(Bid(2,3), False,
											self.responders_hand_info)
		self.assertEqual(self.losing_trick_opener.pLosingCount, 8)
						
	def test_getBid_opener_first_LTC_bid_with_space(self):
		self.responders_hand_info.info["fitSuit"] = 2
		bid = self.losing_trick_opener.getBid(Bid(0,0), True, 
											 self.responders_hand_info)
		self.assertEqual(bid, Bid(2,3))
		
	def test_getBid_opener_first_LTC_bid_no_space(self):
		self.responders_hand_info.info["fitSuit"] = 2
		bid = self.losing_trick_opener.getBid(Bid(4,3), True, 
											 self.responders_hand_info)
		self.assertEqual(bid, Bid(0,0))
	
	def test_getBid_responder_first_LTC_bid_with_space(self):
		self.openers_hand_info.info["fitSuit"] = 2
		bid = self.losing_trick_responder.getBid(Bid(0,0), False, 
												self.openers_hand_info)
		self.assertEqual(bid, Bid(2,4))
	
	def test_getBid_responder_first_LTC_bid_no_space(self):
		self.openers_hand_info.info["fitSuit"] = 2
		bid = self.losing_trick_responder.getBid(Bid(3,4), False, 
												self.openers_hand_info)
		self.assertEqual(bid, Bid(0,0))
	
	def test_getBid_opener_second_LTC_bid_with_space(self):
		self.responders_hand_info.info["fitSuit"] = 2
		self.losing_trick_opener.pLosingCount = 8
		bid = self.losing_trick_opener.getBid(Bid(0,0), True,
											self.responders_hand_info)
		self.assertEqual(bid, Bid(2,4))
	
	def test_getBid_opener_second_LTC_bid_no_space(self):
		self.responders_hand_info.info["fitSuit"] = 2
		self.losing_trick_opener.pLosingCount = 8
		bid = self.losing_trick_opener.getBid(Bid(3,4), True,
											self.responders_hand_info)
		self.assertEqual(bid, Bid(0,0))
		
	def test_getBid_responder_second_LTC_bid_with_space(self):
		self.openers_hand_info.info["fitSuit"] = 2
		self.losing_trick_responder.pLosingCount = 7
		bid = self.losing_trick_responder.getBid(Bid(0,0), False,
											self.openers_hand_info)
		self.assertEqual(bid, Bid(2,4))
	
	def test_getBid_responder_second_LTC_bid_no_space(self):
		self.openers_hand_info.info["fitSuit"] = 2
		self.losing_trick_responder.pLosingCount = 7
		bid = self.losing_trick_responder.getBid(Bid(3,4), False,
											self.openers_hand_info)
		self.assertEqual(bid, Bid(0,0))
	
				 
	   
if __name__ == '__main__':
	unittest.main()
