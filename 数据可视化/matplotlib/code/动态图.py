# -*- coding: utf-8 -*-
'''
@File    : 动态图.py
@Time    : 2020/12/14 15:07
@Author  : huiyun gao
@desc    :
'''

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def draw_animation():
    def update_points(num):
        '''
        更新数据点
        '''
        point_ani.set_data(x[num], y[num])
        return point_ani,

    x = list(range(1, 100))
    y = [2 / (i**2) for i in x]

    fig = plt.figure(tight_layout=True)
    plt.plot(x, y)
    point_ani, = plt.plot(x[0], y[0], "ro")
    #plt.grid(ls="--")
    # 开始制作动画
    ani = animation.FuncAnimation(fig, update_points, np.arange(0, 100), interval=100, blit=True)

    ani.save("./img/test_animation.gif", writer='pillow')
    plt.show()


if __name__ == '__main__':
    draw_animation()
