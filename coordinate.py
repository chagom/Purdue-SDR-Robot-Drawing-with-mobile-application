import json
import numpy as np
from matplotlib import pyplot as plt
from math import sin, cos

file = 'simple.json'

class Robot(object):
	def __init__(self):
		self.pos_x = 0.0
		self.pos_y = 0.0
		self.angle = 0.0
		self.plot = False
		self._delta = 0.01


	def step(self):
		self.deltax()
		self.deltay()
		self.deltaa()

	def move(self, seconds):
		for i in range(int(seconds/self._delta)):
			self.step()
			if i % 3 == 0 and self.plot:
				self.plot_xya()

	def print_xya(self):
		print("x= " + str(self.pos_x) + " " + "y= " + str(self.pos_y))
		print("a= " + str(self.angle))

	def plot_robot(self):
		plt.arrow(self.pos_x, self.pos_y, 0.001 * cos(self.angle), 0.001 * sin(self.angle), head_width=self.length, head_length= self.length, fc='k', ec='k')

	def plot_xya(self):
		plt.scatter(self.pos_x, self.pos_y, c='r', edgecolors='r')


def bezierPathParser(input):
	parsed = input.replace(' ', '')
	parsed = parsed.split('\n')
	
	## MovedTo, QuadTo (2 components)

with open(file) as json_file:
	data = json.load(json_file)
	for item in data['information']:
		bezierPathParser(item['path'])


