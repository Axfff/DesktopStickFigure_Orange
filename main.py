import tkinter as tk
import time
from PIL import Image, ImageTk
import ctypes
import pygame
import win32api, win32con
import Classes


ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配

clock = pygame.time.Clock()

WINDOWsIZE = (170, 170)
BORNpOSITION = (-300, -WINDOWsIZE[1]+50)
# SCREENsIZE = (root.winfo_screenwidth(), root.winfo_screenheight())
SCREENsIZE = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))


orange = Classes.Character()
orange.setImage(r'run_imgs/001.png')
orange.moveAbsolutely(*BORNpOSITION)


v0_y = 0
v_x = 15
a = 100
t0 = time.time()
while orange.getPosition()[1] < SCREENsIZE[1]-WINDOWsIZE[1]:
    t = time.time() - t0
    dy = int(v0_y + a * t)
    dx = v_x
    if orange.getPosition()[1] + dy >= SCREENsIZE[1] - WINDOWsIZE[1]:
        y_pos = SCREENsIZE[1] - WINDOWsIZE[1]
        actual_dy = (SCREENsIZE[1] - WINDOWsIZE[1]) - orange.getPosition()[1]
        dx = int(v_x * (actual_dy / dy))
        orange.moveRelatively(dx, actual_dy)
        break
    orange.moveRelatively(v_x, dy)
    clock.tick(60)


orange.run()

