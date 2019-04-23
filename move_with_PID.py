import math
<<<<<<< HEAD
from roboid import *
=======
import time

file = 'simple.json'
way_points = []

class HamsterPrinter:
	def __init__(self, way_points):
		wait_until_ready()
		self.hamsters = (Hamster(), Hamster())

   	#left
		self.tgt_acc_l = -17600
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
>>>>>>> d41900c3479e0f5eac6f601d278fb386cb4df907


class HamsterPrinter:
    def __init__(self):
        self.hamster_l = Hamster(port_name='/dev/cu.SLAB_USBtoUART')
        self.hamster_r = Hamster(port_name='/dev/cu.SLAB_USBtoUART70')

        wait_until_ready()

        self.tgt_acc = -16300
        self.acc_set = [self.tgt_acc] * 20
        self._prev_err = 0
        self.k_p = 0.005
        self.k_d = 0.002
        self.v = 50
        self.r = 35 / 2
        self.way_points = None
        self.cur_angle = 0

    def move_forward(self, dist):
        print('forward')
        compensation = -5
        self.hamster_l.wheels(self.v, self.v + 3.51), self.hamster_r.wheels(self.v + compensation,
                                                                            self.v + 3.51 + compensation)
        wait(dist)
        self.hamster_l.stop(), self.hamster_r.stop()
        wait(500)

    def turn_right(self, angle):
        print('turn')
        compensation = -3
        temp = 3.8
        turn_time = angle * 8
        self.hamster_r.wheels(self.v * temp, self.v), self.hamster_l.wheels(-(self.v + compensation),
                                                                            -(self.v + compensation) * temp)
        wait(turn_time)
        self.hamster_l.stop(), self.hamster_r.stop()
        wait(500)

    def get_angle(self, src_pos, tgt_pos):

        heading_alpha = math.degrees(math.atan2(tgt_pos[1] - src_pos[1], tgt_pos[0] - src_pos[0]))
        alpha = -self.cur_angle + heading_alpha
        if alpha >= 180:
            alpha = alpha - 360
        elif alpha <= -180:
            alpha = alpha + 360

        self.cur_angle = heading_alpha
        return alpha

    def get_dst(self, src_pos, tgt_pos):
        return math.sqrt((tgt_pos[0] - src_pos[0]) ** 2 + (tgt_pos[1] - src_pos[1]) ** 2)

    def run(self):
        for i in range(len(self.way_points) - 1):
            src_pos = self.way_points[i]
            tgt_pos = self.way_points[i + 1]

            dst = self.get_dst(src_pos, tgt_pos)
            angle = self.get_angle(src_pos, tgt_pos)
            self.turn_right(angle)
            self.move_forward(dst)
            wait(100)

    def print_rectangle(self, size):
        wait_until_ready()
        self.move_forward(size)
        self.turn_right(90)
        self.move_forward(size)
        self.turn_right(90)
        self.move_forward(size)
        self.turn_right(90)
        self.move_forward(size)



def bezierPathParser(input):
	resultArr = []
	parsed = input.split('\n')

	for item in parsed:
		item = item.replace(' ', '')
		item = item.replace('moveto', '')
		item = item.replace('quadto', '')

		s = item[item.find("(")+1:item.find(")")]
		if(s==-1):
			pass
		else:
			resultArr.append("({})".format(s))

	del resultArr[-1]

	return resultArr


if __name__ == "__main__":
<<<<<<< HEAD
    way_points = [
        (0, 0),
        (1000, 0),
        (1000, 1000),
        (0, 1000),
        (0, 0),
    ]
    hamster = HamsterPrinter()
    hamster.way_points = way_points
    # hamster.print_rectangle(2000)
    hamster.run()
=======
	way_points = []
	'''
	way_points = [
		(100, 0),
		(100, 100),
		#(100, 300),
		#(200, 300),
	]
	'''

	with open(file) as json_file:
		data = json.load(json_file)
		for item in data['information']:
			#way_points.append(bezierPathParser(item['path']))
			way_points = bezierPathParser(item['path'])  ## Last trajectory

	print(way_points)

	'''
	robots = HamsterPrinter(way_points)
	robots.left_turn(180)
        #robots.right_turn(180)
        #robots.run()
	'''
>>>>>>> d41900c3479e0f5eac6f601d278fb386cb4df907
