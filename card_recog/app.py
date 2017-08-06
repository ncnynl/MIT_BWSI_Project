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
app = Flask(__name__)
ask = Ask(app, '/')

save_camera_config(port=0, exposure=0.5)
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
ntemplates = [file for file in os.scandir("./masks/nums")]

suits = ["dclubs", "ddiamonds", "dhearts", "dspades","uclubs","udiamonds", "uhearts", "uspades"]
suits_true = ["clubs", "diamonds", "hearts", "spades"]
tmp = {}
for i, suit in enumerate(suits):
	tmp[suit] = i
	tmp[i] = suit
suits= tmp

card_detector = dlib.simple_object_detector("./detector.svm")
suit_detector = dlib.simple_object_detector("./suit_detector.svm")

#load suit classifier

feature_columns = [tf.contrib.layers.real_valued_column("", dimension=64)]
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns, hidden_units=[1024, 512, 256] , n_classes = 8,model_dir = "./weights")
bin_n = 16 # Number of bins
def hog(img):
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
def process_card(approx, card):
	h = np.array([ [0,0],[399,0],[399,499],[0,499] ],np.float32)
	transform = cv2.getPerspectiveTransform(approx, h)
	warp = cv2.warpPerspective(card,transform,(400,500))
	return warp
def toBW(img):
	bw = np.asarray(img).copy()
	bw[bw<128]= 0.0
	bw[bw>=128] = 255.0
	return bw
def process_card_to_suit(approx, card):
	h = np.array([[0,0],[19,0],[19,24],[0,24]],np.float32)
	# print(h)
	# print(card)
	transform = cv2.getPerspectiveTransform(approx, h)
	warp = cv2.warpPerspective(card,transform,(20,25))
	# print(warp.shape)
	return warp


@app.route("/")
def home():
	pass

@ask.launch
def start():
	img = take_picture()
	# img = img[:, ::-1, :]
	cards = card_detector(img)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	fig, ax = plt.subplots()
	ax.imshow(img)
	plt.show()
	vals = []
	suits_list = []
	print(len(cards), flush = True)

	for i, card in enumerate(cards): #for each card
		#identify the location of each card
		l, t, r, b = card.left(), card.top(), card.right(), card.bottom()
		print("Shape: {} by {}".format(card.right()-card.left(), abs(card.top()-card.bottom())))
		r+=15
		r = min(r, img.shape[1])
		b+=15
		b = min(b, img.shape[0])
		#extend the card a bit to ensure that the bottom right number is in the crop
		approx = np.array([[l, t], [r, t], [r, b], [l, b]], np.float32)
		bw = process_card(approx, toBW(img))
		color = process_card(approx, img)
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
			print(dist, temp_name)
			print(Counter(results).most_common())
			(top_left, bottom_right), count = Counter(results).most_common(1)[0]
			scores.append((temp_name, count, dists[(top_left, bottom_right)]/count))

		scores.sort(key = lambda x :(x[1], 1/x[2]), reverse = True)
		val_pred = scores[0][0]
		print(scores)
		# fig, ax = plt.subplots()
		# ax.imshow(color)
		# plt.show()
		vals.append(val_pred)
		####################
		# suit recognition #
		####################
		pred_suits = suit_detector(color)
		pred = np.zeros(8, )
		hog_imgs = []
		for j, suit in enumerate(pred_suits):
			l2, t2, r2, b2 = suit.left(), suit.top(), suit.right(), suit.bottom()
			approx2 = np.array([[l2, t2], [r2, t2], [r2, b2], [l2, b2]], np.float32)
			suit_img = process_card_to_suit(approx2, color)
			hog_img = hog(suit_img)
			hog_img = np.reshape(hog_img, (1, 64))
			predicted_suit = classifier.predict_proba(x=hog_img)
			prediction =[p for p in predicted_suit][0]
			# print(prediction)
			pred = pred + prediction
		print(pred)
		#combine upside down and right side up suits
		p1, p2 = np.split(pred, 2)
		true_pred = p1+p2
		suit_pred = suits_true[np.argmax(true_pred)]
		print(suit_pred)
		suits_list.append(suit_pred)

	print(len(vals), flush = True)
	combined = list(zip(vals, suits_list))
	print(combined, flush = True)
	if len(combined)==0:
		return statement("I don't see a card")
	if len(combined) == 1:
		return statement("You have a {} of {}".format(*combined[0]))
	msg = say_cards(vals)
	print(msg, flush = True)
	return statement(msg)

def say_cards(cards):
	out = "You have "
	for i, card in enumerate(cards):
		print(card, flush = True)
		if i < len(cards)-1:
			val, suit = card
			if val in ['Ace', ]
			out+="a {} of {}, ".format(val, suit)
		else:
			out+="and a {} of {}.".format(*card)
	return out
