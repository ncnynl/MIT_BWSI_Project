from flask import Flask
from flask_ask import Ask, statement, question
import numpy as np

from camera import save_camera_config
from camera import take_picture

import os
import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
from collections import Counter
import tensorflow as tf
import logging
logging.getLogger("tensorflow").setLevel(logging.FATAL)
print("Imports complete", flush = True)
import time
app = Flask(__name__)
ask = Ask(app, '/')

#camera set up (change port for different camera)
save_camera_config(port=2, exposure=0.5)

#for template matching
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
ntemplates = [file for file in os.scandir("./masks/nums")]


#for matching output of classifier --> actual suit
suits = ["dclubs", "ddiamonds", "dhearts", "dspades","uclubs","udiamonds", "uhearts", "uspades"]
suits_true = ["clubs", "diamonds", "hearts", "spades"]
tmp = {}
for i, suit in enumerate(suits):
	tmp[suit] = i
	tmp[i] = suit
suits= tmp


#load detectors
card_detector = dlib.simple_object_detector("./detector.svm")
suit_detector = dlib.simple_object_detector("./suit_detector.svm")

#load suit classifier
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=64)]
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns, hidden_units=[1024, 512, 256] , n_classes = 8,model_dir = "./weights")


bin_n = 16 # Number of bins (for HOG)
def hog(img):
	"""
	Computes the HOG [histogram of oriented gradients] for an image

	Parameters
	----------
	img: np.ndarray
		input image (greyscale)- shape should be (H, W)

	Returns
	-------
	Vector of shape (64, ) that describes the image using gradients

	"""
	gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
	gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
	mag, ang = cv2.cartToPolar(gx, gy)

	# quantizing binvalues in (0...16)
	bins = np.int32(bin_n*ang/(2*np.pi))

	# Divide to 4 sub-squares
	bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
	mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
	hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
	hist = np.hstack(hists)
	return hist

def process_card(approx, img):
	"""
	Takes the section of an image detected to be a card and warps it to 400x500 px

	Parameters
	----------
	approx: np.ndarray
		[x, y] of corners of the card in the image
	img: np.ndarray
		original image

	Returns
	-------
	The cutout of the card, warped to fit 400x500px
	"""
	h = np.array([ [0,0],[399,0],[399,499],[0,499] ],np.float32)
	transform = cv2.getPerspectiveTransform(approx, h)
	warp = cv2.warpPerspective(img,transform,(400,500))
	return warp

def toBW(img):
	"""
	Converts an image to single channel black and white

	Parameters
	----------
	img: np.ndarray
		image to turn black and white

	Returns
	-------
	A copy of the original image that's been converted to black and white
	"""
	bw = np.asarray(img).copy()
	bw[bw<128]= 0.0
	bw[bw>=128] = 255.0
	return bw

def process_card_to_suit(approx, card):
	"""
	Takes the section of an image detected to be a suit object and warps it to 20x25 px

	Parameters
	----------
	approx: np.ndarray
		[x, y] of corners of the suit object in the image
	img: np.ndarray
		original image

	Returns
	-------
	The cutout of the suit object, warped to fit 20x25px
	"""
	h = np.array([[0,0],[19,0],[19,24],[0,24]],np.float32)
	transform = cv2.getPerspectiveTransform(approx, h)
	warp = cv2.warpPerspective(card,transform,(20,25))
	return warp


@app.route("/")
def home():
	return "Hello!"

@ask.launch
def start():
	"""
	Runs when the skill is activated
	"""
	return question("What would you like to do?")

@ask.intent("IdentifyIntent")
def identify():
	img = take_picture()
	combined = get_cards(img)
	print(combined, flush = True)
	if len(combined)==0:
		return statement("I don't see a card")
	if len(combined) == 1:
		return statement("You have a {} of {}".format(*(combined[0])))
	msg = say_cards(combined)
	print(msg, flush = True)
	return statement(msg)

def get_cards(img):

	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	cards = card_detector(img)

	# fig, ax = plt.subplots()
	# ax.imshow(img)
	# plt.show()
	vals = []
	suits_list = []
	print("{} cards detected".format(len(cards)), flush = True)
	for i, card in enumerate(cards): #for each card
		#identify the location of each card
		l, t, r, b = card.left(), card.top(), card.right(), card.bottom()
		# print("Shape: {} by {}".format(card.right()-card.left(), abs(card.top()-card.bottom())))
		r+=15
		r = min(r, img.shape[1])
		b+=15
		b = min(b, img.shape[0])
		#extend the card a bit to ensure that the bottom right number is in the crop
		approx = np.array([[l, t], [r, t], [r, b], [l, b]], np.float32)
		bw = process_card(approx, toBW(img))
		color = process_card(approx, img)
		t0 = time.time()
		######################
		# Number recognition #
		######################
		scores = []
		for templ in ntemplates:
			temp_name = templ.name.split("_")[1].split(".")[0]
			template = cv2.imread("./masks/nums/{}".format(templ.name), 0)
			w, h = template.shape[::-1]
			results = []
			reses = []
			dists = {}
			for meth in methods:
				method = eval(meth)
				res = cv2.matchTemplate(color,template,method)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
					top_left = min_loc
				else:
					top_left = max_loc
				l = top_left[0]
				r = top_left[0]+w
				t = top_left[1]
				b = top_left[1]+h
				section = bw[t:b, l:r]
				bottom_right = (top_left[0] + w, top_left[1] + h)
				reses.append(res)
				result = (top_left, bottom_right)
				dist=np.linalg.norm(section-template)
				if result in dists:
					dists[result]+=dist
				else:
					dists[result] = dist
				results.append(result)
			# print(dist, temp_name)
			# print(Counter(results).most_common())
			(top_left, bottom_right), count = Counter(results).most_common(1)[0]
			scores.append((temp_name, count, dists[(top_left, bottom_right)]/count))

		scores.sort(key = lambda x :(x[1], 1/x[2]), reverse = True)
		val_pred = scores[0][0]
		# print(scores)
		fig, ax = plt.subplots()
		ax.imshow(color)
		plt.show()
		vals.append(val_pred)
		t1= time.time()
		print("{} seconds elapsed for number recognition".format(t1-t0), flush = True)
		####################
		# suit recognition #
		####################
		t2 = time.time()
		pred = np.zeros(8, )
		hog_imgs = []
		pred_suits = suit_detector(color)
		for j, suit in enumerate(pred_suits):

			l2, t2, r2, b2 = suit.left(), suit.top(), suit.right(), suit.bottom()
			approx2 = np.array([[l2, t2], [r2, t2], [r2, b2], [l2, b2]], np.float32)
			suit_img = process_card_to_suit(approx2, color)
			hog_img = hog(suit_img)
			hog_img = np.reshape(hog_img, (1, 64))
			t_1 = time.time()
			with tf.device("/gpu:0"):
				c = classifier.predict_proba(x=hog_img)
			with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
				sess.run(c)
			t_2 = time.time()
			print("{} elapsed for probabilities".format(t_2-t_1), flush = True)
			prediction =[p for p in predicted_suit][0]
			pred = pred + prediction
		# print(pred)
		#combine upside down and right side up suits
		p1, p2 = np.split(pred, 2)
		true_pred = p1+p2
		suit_pred = suits_true[np.argmax(true_pred)]
		suits_list.append(suit_pred)
		t3 = time.time()
		print("{} seconds elapsed for suit recognition".format(t3-t2), flush = True)
	combined = list(zip(vals, suits_list))
	return combined

def say_cards(cards_list):
	"""
	Parses a list of cards into speech

	Parameters
	----------
	cards_list: list
		list of (value, suit) pairs, each representing a card

	Returns
	-------
	A string with a (I hope) grammatically correct sentence that lists all cards
	"""
	out = "You have "
	print("Cards: {}".format(cards_list), flush = True)
	for i, card in enumerate(cards_list):
		print(card, flush = True)
		if i < len(cards_list)-1:
			val, suit = card
			print(card, flush = True)
			if val in ['Ace', '8']:
				out+="an {} of {}, ".format(val, suit)  
			else:
				out+="a {} of {}, ".format(val, suit)
			
		else:
			print(card, flush = True)
			val, suit = card
			
			if val in ['Ace', '8']:
				out+="and an {} of {}, ".format(val, suit)  
			else:
				out+="and a {} of {}, ".format(val, suit)
	return out

@ask.intent("RankIntent")
def rank_img():
	img = take_picture()
	combined = get_cards(img)
	print(combined, flush = True)
	msg = rank_hand(combined)
	print(msg, flush = True)
	return statement(msg)

SORT_ORDER = {"2": 0, "3": 1,"4": 2,"5": 3,"6": 4,"7": 5, "8": 6,"9": 7,"10": 8,"Jack": 9,"Queen":10, "King":11, "Ace":12}
def rank_hand(cards):
	"""
	Ranks a standard five card poker hand

	Parameters
	----------
	cards: list
		one card: (value, suit)

	Returns
	-------
	Rank of hand
	"""

	#There's probably a better way to do this
	if len(cards)!=5:
		return "Invalid hand"
	vals, suits = list(zip(*[card for card in cards]))
	print(vals, suits, flush = True)
	if all(x == suits[0] for x in suits): #all suits the same (i.e. a flush)
		if is_straight(vals):
			if sorted(vals, key = lambda x:SORT_ORDER[x], reverse = True)[0] == "Ace":
				return "Royal Flush"
			else:
				return "Straight Flush"
		else:
			return "Flush"
	else:
		if _ofakind(vals, 4):
			return "Four of a kind"
		elif full_house(vals):
			return "Full House"
		elif is_straight(vals):
			return "Straight"
		elif _ofakind(vals, 3):
			return "Three of a kind"
		elif two_pair(vals):
			return "Two pair"
		elif _ofakind(vals, 2):
			return "Pair"
		else:
			return "High Card"

def full_house(vals):
	counter = Counter(vals)
	return counter.most_common()[0][1] == 3 and counter.most_common()[1][1] == 2
def two_pair(vals):
	counter = Counter(vals)
	return counter.most_common()[0][1] == 2 and counter.most_common()[1][1] == 2
def _ofakind(vals, num):
	"""
	Returns True if the hand is a [num] of a kind
	"""
	counter = Counter(vals)
	return counter.most_common(1)[0]==num
def is_straight(vals):
	"""
	Returns True if values form a straight (5 consecutive cards)
	"""
	for i, val in enumerate(sorted(vals, key = lambda x:SORT_ORDER[x])):
		if i == len(vals)-1:
			return True
		if SORT_ORDER[val] != SORT_ORDER[vals[i+1]]-1:
			return False
	return False