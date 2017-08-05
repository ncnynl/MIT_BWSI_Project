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
app = Flask(__name__)
ask = Ask(app, '/')

save_camera_config(port=0, exposure=0.5)
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
ntemplates = [file for file in os.scandir("./masks/nums")]

values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
tmp = {}
for i, value in enumerate(values):
	tmp[value] = i
	tmp[i] = value
values = tmp
card_detector = dlib.simple_object_detector("./detector.svm")

def process_card(approx, card):
	h = np.array([ [0,0],[399,0],[399,499],[0,499] ],np.float32)
	transform = cv2.getPerspectiveTransform(approx, h)
	warp = cv2.warpPerspective(card,transform,(400,500))
	return warp
def toBW(img):
	bw = np.asarray(img).copy()
	# bw_mean= np.mean(np.asarray(img), axis = 2)
	# bw[bw_mean<128]= np.array([0, 0, 0])
	# bw[bw_mean>=128] = np.array([255, 255, 255])
	# print(bw[bw_mean<128])
	bw[bw<128]= 0.0
	bw[bw>=128] = 255.0

	# return np.mean(bw, axis = 2, dtype = "uint8")
	return bw



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
	print(len(cards))
	for i, card in enumerate(cards):
		l, t, r, b = card.left(), card.top(), card.right(), card.bottom()
		print("Shape: {} by {}".format(card.right()-card.left(), abs(card.top()-card.bottom())))
		r+=15
		r = min(r, img.shape[1])
		b+=15
		b = min(b, img.shape[0])
		approx = np.array([[l, t], [r, t], [r, b], [l, b]], np.float32)
		print(l, r, t, b)
		bw = process_card(approx, toBW(img))
		color = process_card(approx, img)
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
				# print(bw.shape)
				res = cv2.matchTemplate(bw,template,method)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				

				# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
				if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
					top_left = min_loc
				else:
					top_left = max_loc
				l = top_left[0]
				r = top_left[0]+w
				t = top_left[1]
				b = top_left[1]+h
				section = bw[t:b, l:r]
				# fig, ax = plt.subplots()
				# ax.imshow(section)
				# plt.show()

				

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
			# res_mean = np.mean(np.array(reses), axis = 0)
			(top_left, bottom_right), count = Counter(results).most_common(1)[0]

			scores.append((temp_name, count, dists[(top_left, bottom_right)]/count))

		scores.sort(key = lambda x :(x[1], 1/x[2]), reverse = True)
		val_pred = scores[0][0]
		print(scores)
		fig, ax = plt.subplots()
		ax.imshow(color)
		plt.show()
		vals.append(val_pred)

	print(vals)
	if len(vals)==0:
		return statement("I don't see a card")
	if len(vals) == 1:
		return statement("You have a {}".format(vals[0]))
	return statement(say_cards(vals))

def say_cards(vals):
	out = "You have "
	for i, val in enumerate(vals):
		if i < len(vals)-1:
			out+="a {}, ".format(val)
		else:
			out+="and a {}".format(val)
	return out
