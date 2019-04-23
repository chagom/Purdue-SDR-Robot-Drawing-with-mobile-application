import math
from roboid import *


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


if __name__ == "__main__":
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
