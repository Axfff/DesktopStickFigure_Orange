import tkinter as tk
# import time
import ctypes
from PIL import Image, ImageTk, ImageDraw
import aggdraw


# import pygame


def draw_line(draw, xy, fill, width):
    draw.line(xy, fill, width)
    r = int(width / 2)
    for pos in xy:
        # print(f'draw circle at {pos}')
        draw.ellipse([(pos[0] - r, pos[1] - r), (pos[0] + r, pos[1] + r)], fill=fill)


def draw_curve(img, startPos, ctrlPos, endPos, fill, width):
    canvas = aggdraw.Draw(img)
    # print(startPos, ctrlPos, endPos)

    pen = aggdraw.Pen(fill, width)
    path = aggdraw.Path()
    path.moveto(*startPos)
    path.curveto(*ctrlPos, *ctrlPos, *endPos)
    canvas.path(path, path.coords(), pen)
    canvas.flush()

    draw = ImageDraw.Draw(img)
    r = int(width / 2)
    draw.ellipse([(startPos[0] - r, startPos[1] - r), (startPos[0] + r, startPos[1] + r)], fill=fill)
    draw.ellipse([(endPos[0] - r, endPos[1] - r), (endPos[0] + r, endPos[1] + r)], fill=fill)


headImg_facingLeft = Image.open(r'run_imgs/head/facingLeft.png')
headImg_facingRight = Image.open(r'run_imgs/head/facingRight.png')
def drawImg(canvasSize, keyPoints, fillColor=(255, 112, 0, 255), width=16, showCtrlPoints=False):
    # check and init data
    if len(keyPoints) != 14:
        raise ValueError(f'keyPoints takes exactly 14 values({len(keyPoints)} given)')
    # for pos in keyPoints[:-1]:
    #     if pos[0] > canvasSize[0] or pos[1] > canvasSize[1]:
    #         raise ValueError('input pos bigger than canvas size')
    #     elif pos[0] < 0 or pos[1] < 0:
    #         raise ValueError('input pos smaller than zero')
    p_c, p_kn1, p_kn2, p_an1, p_an2, p_f1, p_f2, p_w, p_n, p_el1, p_el2, p_h1, p_h2, a_n = keyPoints

    # init img
    img = Image.new('RGBA', canvasSize, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # head
    if a_n[0] == 0:
        headImg = headImg_facingLeft
    elif a_n[0] == 1:
        headImg = headImg_facingRight
    else:
        raise ValueError('a_n[0] input is not defined')
    headImg = headImg.rotate(a_n[1])
    headPos = (p_n[0]-int(headImg.size[0]/2), p_n[1]-int(headImg.size[1]/2))
    img.paste(headImg, headPos)
    # leg 1
    draw_line(draw, [p_c, p_kn1, p_an1, p_f1], fillColor, width)
    # leg 2
    draw_line(draw, [p_c, p_kn2, p_an2, p_f2], fillColor, width)
    # arm 1
    draw_curve(img, p_n, p_el1, p_h1, fillColor, width)
    # arm 2
    draw_curve(img, p_n, p_el2, p_h2, fillColor, width)
    # body
    draw_curve(img, p_n, p_w, p_c, fillColor, width)

    # showCtrlPoints
    if showCtrlPoints:
        r = 2
        showCtrlPointsColor = (255, 255, 255)
        for pos in keyPoints[:-1]:
            draw.ellipse([(pos[0] - r, pos[1] - r), (pos[0] + r, pos[1] + r)], fill=showCtrlPointsColor)
        # draw.line(keyPoints[:-1], fill=showCtrlPointsColor, width=5)

    return img


class Character:

    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-transparentcolor', '#f0f0f0')
        self.root.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
        self.root.wm_attributes("-topmost", True)  # 永远处于顶层
        self.root.overrideredirect(True)  # 还可以调用如下方法去除窗口边框
        self.root.resizable(width=False, height=False)  # 窗口不可缩放

        self.img = None
        self.commandList = []

    def setImage(self, imgPath):
        self.img = ImageTk.PhotoImage(Image.open(imgPath))
        # print(self.img.width(), self.img.height())
        self.root.geometry(f'{self.img.width()}x{self.img.height()}')
        tk.Label(master=self.root, bg='#f0f0f0', image=self.img).pack()
        self.root.update()

    def moveAbsolutely(self, x_pos='fix', y_pos='fix'):
        if x_pos == 'fix':
            x_pos = self.root.winfo_x()
        if y_pos == 'fix':
            y_pos = self.root.winfo_y()
        self.root.geometry(f'+{x_pos}+{y_pos}')
        self.root.update()

    def moveRelatively(self, dx, dy):
        x_pos = self.root.winfo_x() + dx
        y_pos = self.root.winfo_y() + dy
        self.moveAbsolutely(x_pos, y_pos)
        self.root.update()

    def getPosition(self):
        return self.root.winfo_x(), self.root.winfo_y()

    def update(self):
        self.root.update()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    orange = Character()
    # orange.setImage(r'run_imgs/001.png')

    kPoints = [(85, 100),
               (100, 130), (85, 135),
               (105, 165), (72, 165),
               (110, 165), (77, 165),
               (83, 79),
               (95, 60),
               (100, 85), (60, 80),
               (120, 110), (55, 110),
               (0, 0)
               ]
    drawImg((500, 500), kPoints).show()
    # # a.update()
    # orange.moveAbsolutely(300, 400)
    # # a.update()
    # time.sleep(1)
    # orange.moveAbsolutely(400, 500)
    # # a.update()
    # time.sleep(1)
    # for i in range(40):
    #     if i <= 10:
    #         orange.moveRelatively(i * 10, -10 * i)
    #     if i > 30:
    #         orange.moveRelatively(i * 1, 1 * i)
    #     pygame.time.Clock().tick(30)
    # time.sleep(1)
    # orange.setImage(r'run_imgs/001s.png')
    # # a.update()
    # orange.moveAbsolutely(100, 100)
    # # a.update()
    # time.sleep(1)
    # orange.run()
