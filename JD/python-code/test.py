# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:32:41 2022

@author: 罗佳敏
"""

import os

import cv2
import numpy as np

base_dir = os.path.dirname(os.path.dirname(__file__))
imag_dir = os.path.join(base_dir, 'images', 'slider_imags')


def img2cv(img_data):

    img = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.COLOR_RGB2BGR)

    return img


def img2xy(path_background, path_patch):
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(path_background)  # 背景图片
    tp_img = cv2.imread(path_patch)  # 缺口图片
    # bg_img = img2cv(bg)
    # tp_img = img2cv(fg)

    # 截取图片部分
    # part_tp_img = tp_img[510:605, 155:256]#最小145，最大应该是165

    #cv2.namedWindow('image',0)#O表示显示窗口可以随意手动调节，1
    #cv2.imshow('MORPH_CLOSE', part_tp_img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    #cv2.imwrite("bg_style.png",bg_pic) # 保存背景轮廓提取
    #cv2.imwrite("slide_style.png",tp_pic) # 保存滑块背景提取
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    tl = max_loc  # 左上角点的坐标
    # 返回缺口的左上角X坐标
    # 绘制矩形框
    th, tw = tp_pic.shape[:2]
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(os.path.join(imag_dir, "result_new.png"), bg_img)  # 保存在本地
    return tl


if __name__ == '__main__':

    path_background = os.path.join(imag_dir, 'background.png')
    path_patch = os.path.join(imag_dir, 'patch.png')

    img2xy(path_background, path_patch)
