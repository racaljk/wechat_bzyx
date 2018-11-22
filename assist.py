# -*- coding: utf-8 -*-
import os
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image


def get_touch_point():
    mobile_info = os.popen('cd adb && adb shell wm size')
    resolution = re.findall(r'Physical size: (\d+?)x(\d+)', mobile_info.read())
    if len(resolution) == 0:
        raise Exception("can not read mobile resolution")
    return [int(resolution[0][0]) // 2, int(resolution[0][1]) // 2]


def get_screenshot():
    os.system('cd adb && adb shell screencap -p /sdcard/bzyx_assist.png && adb pull /sdcard/bzyx_assist.png ..')


def create_board(image_distance):
    global update_interval
    if image_distance < 790:
        press_time = image_distance * 1.6
        update_interval = 2.5
    elif 790 <= image_distance <= 1700:
        press_time = image_distance * 1.9
        update_interval = 4
    elif image_distance > 1700:
        press_time = image_distance * 2.00
        update_interval = 6

    press_time = int(press_time)
    cmd = 'adb shell input swipe ' + point[0] + ' ' + point[1] + ' ' + point[0] + ' ' + point[1] + ' ' + str(press_time)
    print(cmd)
    os.system('cd adb && ' + cmd)


def on_click(event):
    global should_update
    global coordinate_arr
    global click_count

    #print('touch at ', (event.xdata, event.ydata))
    coordinate_arr.append([(event.xdata, event.ydata)])

    click_count += 1
    if click_count == 2:
        click_count = 0  # reset to wait next double-clicking
        cor1 = coordinate_arr.pop()
        cor2 = coordinate_arr.pop()

        distance = (cor1[0][0] - cor2[0][0]) ** 2 + (cor1[0][1] - cor2[0][1]) ** 2
        distance = distance ** 0.5
        print('image distance is', distance)
        create_board(distance)
        should_update = True


def update_fig(*args):
    global should_update
    global update_interval
    if should_update:
        time.sleep(update_interval)  # it is necessary since game box needs time to place
        get_screenshot()
        im.set_array(np.array(Image.open('bzyx_assist.png')))
        should_update = False
    return im,


should_update = True
click_count = 0
coordinate_arr = []
point = [str(x) for x in get_touch_point()]
update_interval = 2  # default to 2s

fig = plt.figure()
get_screenshot()
img = np.array(Image.open('bzyx_assist.png'))
im = plt.imshow(img, animated=True)

fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, update_fig, interval=50, blit=True)
plt.show()
