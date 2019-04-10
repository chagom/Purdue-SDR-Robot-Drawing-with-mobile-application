from roboid import *
import math
import numpy
import collections

hamster = Hamster()
wait_until_ready()

def drive(posnr, wdia, vL, vR, t, Cangle):
    vdiff = vR-vL
    newposn = [0,0,0]
    newposn[2] = posnr[2] -vdiff*t/wdia

    if(vdiff == 0):
        newposn[0] = vL*t*math.cos(posnr[2]) + posnr[0]
        newposn[1] = vR*t*math.sin(posnr[2]) + posnr[1]
    else:
        if vR > vL:
            alpha = math.atan(t*(vR-vL)/wdia)
        elif vR<vL:
            alpha = math.atan(t*(vL-vR)/wdia)
        newposn[0] = posnr[0] + t*(vL + vR)/2*math.cos(Cangle - alpha)
        newposn[1] = posnr[1] + t*(vL + vR)/2*math.sin(Cangle - alpha)

    return newposn

trajectory = collections.deque([[1.0,0.0,math.degrees(0.0)],[1.0,100.0, math.degrees(0.0)]])

dt = 1
Tsim = 100
d = 4

k_rho = 0.05
k_alpha = 0.8
k_beta = -0.008

j= 1
for j in range(0,len(trajectory)-1):
    temp = trajectory.popleft()
    C_Robot_Pos = temp[0:2]
    C_Robot_Angr = math.radians(temp[2])
    C_Robot_Angd = temp[2]

for i in range(0, Tsim, dt):
    delta_x = trajectory[0][0] - C_Robot_Pos[0]
    delta_y = trajectory[0][1] - C_Robot_Pos[1]
    rho = math.sqrt(delta_x**2 + delta_y**2)
    alpha = -C_Robot_Angr + math.atan2(delta_y, delta_x)

    if math.degrees(alpha) > 180:
        temp_alpha = math.degrees(alpha) - 360
        alpha = math.radians(temp_alpha)
    elif math.degrees(alpha)<-180:
        temp_alpha = math.degrees(alpha) + 360
        alpha = math.radians(temp_alpha)

    beta = -C_Robot_Angr-alpha

    v = k_rho*rho
    w = k_alpha*alpha+k_beta*beta
    vL = v+ d/2*w
    vR = v - d/2*w
    print(vL, vR)
    hamster.wheels(vL,vR)

    j = j + 1

    posr = C_Robot_Pos + [C_Robot_Angr]
    posr = drive(posr, d, vL, vR, dt, posr[2])
    C_Robot_Pos = [posr[0], posr[1]]
    C_Robot_Angr = posr[2]

    wait(500)
