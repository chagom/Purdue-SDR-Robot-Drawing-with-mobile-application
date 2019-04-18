from roboid import *
import numpy as np
import json
import math
import time

class HamsterPrinter:
	def __init__(self, way_points):
		wait_until_ready()
		self.hamster = Hamster()
		self.tgt_acc = -16300
		self.acc_set = [self.tgt_acc]*30
		self._prev_err = 0
                self.k_p = 0.03
                self.k_d = 0.02
		self.v = 50
		self.r = 35/2
		self.way_points = way_points

	def steering_control(self):
		self.acc_set.append(self.hamster.acceleration_z())
		self.acc_set.pop(0)

                #print(self.hamster.acceleration_z())
		err = np.mean(self.acc_set) - (self.tgt_acc)
		self._prev_err = err
		return self.k_p * err + self.k_d * (err - self._prev_err)

	def turn(self, angle):
		turn_time = self.r * math.radians(angle) / self.v

		if angle > 0:
			self.hamster.turn_right(turn_time)
		else:
			self.hamster.turn_left(turn_time)

	def move_forward(self, dst):
		move_time = dst / self.v

		start_time = time.time()
		while True:
			#compansation = self.steering_control()
                        compansation = 3.51
			print(compansation)
			self.hamster.wheels(self.v, self.v + compansation)
			elapsed_time = time.time() - start_time
			if elapsed_time >= move_time:
				break
			wait(10)

	def get_angle(self, src_pos, tgt_pos):
		return 180

	def get_dst(self, src_pos, tgt_pos):
		return math.sqrt((tgt_pos[0] - src_pos[0])**2 + (tgt_pos[1] - src_pos[1])**2)

	def run(self):
		for i in range(len(self.way_points)-1):
			src_pos = way_points[i]
			tgt_pos = way_points[i + 1]

			dst = self.get_dst(src_pos, tgt_pos)
			angle = self.get_angle(src_pos, tgt_pos)

		#	self.turn(angle)
			self.move_forward(dst)

			wait(100)

if __name__ == "__main__":
	way_points = [
		(100, 0),
		(100, 100),
		#(100, 300),
		#(200, 300),
	]
	robots = HamsterPrinter(way_points)
	#robots.turn(90)
        robots.run()
