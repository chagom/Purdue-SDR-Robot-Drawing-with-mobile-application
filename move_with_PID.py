from roboid import *
import numpy as np
import json
import math
import time

class HamsterPrinter:
	def __init__(self, way_points):
		wait_until_ready()
		self.hamsters = (Hamster(), Hamster())

                #left
                self.tgt_acc_l =  -17600
		self.acc_set_l = [self.tgt_acc_l]*30
		self._prev_err_l = 0
                self.k_p_l = 0.03
                self.k_d_l = 0.02
		self.v_l = 50
		self.r_l = 35/2

                #right
                self.tgt_acc_r =  -16300
                self.acc_set_r = [self.tgt_acc_r]*30
                self._prev_err_r = 0
                self.k_p_r = 0.03
                self.k_d_r = 0.02
                self.v_r = 50
                self.r_r = 35/2

                self.way_points = None
                self.angle_mapping = {
                        10 : 0.1,
                        20 : 0.2,
                        30 : 0.3,
                        90 : 1.05,
                        120 : 0.12,
                        }

        def steering_control(self):
		self.acc_set_l.append(self.hamsters[0].acceleration_z())
		self.acc_set_l.pop(0)

                self.acc_set_r.append(self.hamsters[1].acceleration_z())
                self.acc_set_r.pop(0)

                #print(self.hamsters[0].acceleration_z())
		err_l = np.mean(self.acc_set_l) - (self.tgt_acc_l)
		self._prev_err_l = err_l

                err_r = np.mean(self.acc_set_r) - (self.tgt_acc_r)
                self._prev_err_r = err_r

                return self.k_p_l * err_l + self.k_d_l * (err_l - self._prev_err_l), self.k_p_r * err_r + self.k_d_r *(err_r - self._prev_err_r)

	def turn(self, angle):
		#turn_time = self.r * math.radians(angle) / self.v

		if angle > 0:
			self.hamsters[0].move_forward(20)
		else:
			self.hamsters[1].turn_forward(2)

        def left_turn(self, angle):
             turn_time = self.r_r * math.radians(angle) / self.v_r

             start_time = time.time()

             while True:
                 compensation_l, compensation_r = self.steering_control()
                 #compansation = 3.51
                 #print(compansation)
                 self.hamsters[0].wheels(-self.v_l, -self.v_l - compensation_l)
                 self.hamsters[1].wheels(self.v_r, self.v_r + compensation_r)
                 elapsed_time = time.time() - start_time
                 if elapsed_time >= turn_time:
                     break
                 wait(500)

        def right_turn(self, angle):
            turn_time = self.r_l * math.radians(angle) / self.v_l

            start_time = time.time()

            while True:
                compensation_l, compensation_r = self.steering_control()
                #compansation = 3.51
                #print(compansation)
                self.hamsters[0].wheels(self.v_l, self.v_l + compensation_l)
                self.hamsters[1].wheels(-self.v_r, -self.v_r - compensation_r)
                elapsed_time = time.time() - start_time
                if elapsed_time >= turn_time:
                    break
                wait(500)



	def move_forward(self, dst):
		move_time = dst / self.v_l

		start_time = time.time()
		while True:
			compensation_l, compensation_r = self.steering_control()
                        #compansation = 3.51
			#print(compansation)
			self.hamsters[0].wheels(self.v_l, self.v_l + compensation_l)
			self.hamsters[1].wheels(self.v_r, self.v_r + compensation_r)
                        elapsed_time = time.time() - start_time
			if elapsed_time >= move_time:
				break
			wait(500)

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
	robots.left_turn(180)
        #robots.right_turn(180)
        #robots.run()
