# from PIL import Image
# import aggdraw
#
# img = Image.new("RGB", (200, 200), "gray")
# canvas = aggdraw.Draw(img)
#
# pen = aggdraw.Pen((255, 0, 0), 4)
# path = aggdraw.Path()
# path.moveto(10, 10)
# path.curveto(50, 10, 100, 100, 100, 100)
# canvas.path(path, path.coords(), pen)
# canvas.flush()
#
# # img.save("curve.png", "PNG")
# img.show()

# import tkinter as tk
# from tkinter import filedialog
#
# root = tk.Tk()
# root.withdraw()
#
# file_path = filedialog.askopenfilename()
# # file_path = filedialog.askdirectory()
#
# print(file_path)

import tkinter as tk
from tkinter.filedialog import *
from PIL import Image


def selectFile():
    global img
    filepath = askopenfilename()  # 选择打开什么文件，返回文件名
    filename.set(filepath)  # 设置变量filename的值
    img = Image.open(filename.get())  # 打开图片


def outputFile():
    outputFilePath = askdirectory()  # 选择目录，返回目录名
    outputpath.set(outputFilePath)  # 设置变量outputpath的值


def fileSave():
    filenewpath = asksaveasfilename(defaultextension='.png')  # 设置保存文件，并返回文件名，指定文件名后缀为.png
    filenewname.set(filenewpath)  # 设置变量filenewname的值
    img.save(str(filenewname.get()))  # 设置保存图片


root = tk.Tk()
filename = tk.StringVar()
outputpath = tk.StringVar()
filenewname = tk.StringVar()

# 构建“选择文件”这一行的标签、输入框以及启动按钮，同时我们希望当用户选择图片之后能够显示原图的基本信息
tk.Label(root, text='选择文件').grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=filename).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text='打开文件', command=selectFile).grid(row=1, column=2, padx=5, pady=5)

# 构建“选择目录”这一行的标签、输入框以及启动按钮
tk.Label(root, text='选择目录').grid(row=2, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=outputpath).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text='点击选择', command=outputFile).grid(row=2, column=2, padx=5, pady=5)

# 构建“保存文件”这一行的标签、输入框以及启动按钮
tk.Label(root, text='保存文件').grid(row=3, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=filenewname).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text='点击保存', command=fileSave).grid(row=3, column=2, padx=5, pady=5)

root.mainloop()
