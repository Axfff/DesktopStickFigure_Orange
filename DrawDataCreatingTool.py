from Classes import drawImg
import tkinter as tk
from tkinter.messagebox import askyesnocancel
from tkinter.filedialog import *
import threading
import ctypes
from PIL import ImageTk
import sys
from pygame.time import Clock
import editKeyPointsFile
from os import rename, remove, path


ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = tk.Tk()
root.title('Key points file editor')
# character = Classes.CharacterWithoutWindow()

changeKeyPoints = []

keyPointsDic = {'p_c': [255, 315],
                'p_kn1': [250, 410], 'p_kn2': [280, 405],
                'p_an1': [235, 491], 'p_an2': [289, 491],
                'p_f1': [235, 491], 'p_f2': [289, 491],
                'p_w': [255, 275],
                'p_n': [265, 230],
                'p_el1': [230, 281], 'p_el2': [270, 289],
                'p_h1': [229, 335], 'p_h2': [286, 320],
                'a_h': [1, -8]
                }
initialFilePath = 'unsaved.json'
KPFile = editKeyPointsFile.KeyPointsFile(initialFilePath)
root.title(f'Key points file editor - {initialFilePath}')


def transformKPDic(KPDic):
    outputList = []
    for k in KPDic:
        outputList.append(KPDic[k])
    return outputList


def button(text=None, command=None, width=None, height=None):
    if width is None:
        width = 8
    if height is None:
        height = 3
    return tk.Button(master=root, width=width, height=height, text=text, command=command)


def get_command_for_buttons(text, changeKeyPointsList, ScaleXSetting=None, ScaleYSetting=None):
    global text_L_selection, changeKeyPoints, original_value_x, original_value_y

    changeKeyPoints = changeKeyPointsList

    # update selection label
    text_L_selection.set(text)

    # update scales
    if not ScaleXSetting:
        ScaleXSetting = {'from': 0, 'to': 500, 'resolution': 1}
    if not ScaleYSetting:
        ScaleYSetting = {'from': 0, 'to': 500, 'resolution': 1}
    for option in ScaleXSetting:
        Scale_x[option] = ScaleXSetting[option]
    for option in ScaleYSetting:
        Scale_y[option] = ScaleYSetting[option]
    value_x_, value_y_ = keyPointsDic[changeKeyPointsList[0]]
    value_x.set(value_x_)
    value_y.set(value_y_)
    original_value_x = value_x_
    original_value_y = value_y_


def getValue_and_updateImage():
    # take out keyPointsPos data from keyPointsDic
    global keyPointsDic
    keyPoints = list(map(lambda a: tuple(keyPointsDic[a]), keyPointsDic))

    # update viewImage
    global viewImage
    viewImage = ImageTk.PhotoImage(drawImg((500, 500), keyPoints, showCtrlPoints=True))


def updateGUI():
    global root, img_L_viewer
    clock = Clock()
    while True:
        img_L_viewer['image'] = viewImage
        root.update()
        clock.tick(120)


def getValue_X(_):
    global changeKeyPoints, original_value_x

    x = value_x.get()
    dx = original_value_x - x
    original_value_x = x

    for ind, var in enumerate(changeKeyPoints):
        if ind == 0:
            keyPointsDic[var][0] = x

        else:
            keyPointsDic[var][0] -= dx

    KPFile.addFrame(frameNum=pageNumStr.get(), keyPoints=transformKPDic(keyPointsDic))
    # print(pageNumStr.get())
    getValue_and_updateImage()


def getValue_Y(_):
    global changeKeyPoints, original_value_y

    y = value_y.get()
    dy = original_value_y - y
    # print(original_value_y, y, dy)
    original_value_y = y

    for ind, var in enumerate(changeKeyPoints):
        if ind == 0:
            keyPointsDic[var][1] = y

        else:
            keyPointsDic[var][1] -= dy

    KPFile.addFrame(frameNum=pageNumStr.get(), keyPoints=transformKPDic(keyPointsDic))
    # print(pageNumStr.get())
    getValue_and_updateImage()


def openFile():
    global KPFile, root
    filePath = askopenfilename()
    KPFile = editKeyPointsFile.KeyPointsFile(filePath)
    getFrameDataFromFile()
    root.title(f'Key points file editor - {filePath}')


def createFile():
    global KPFile, root
    filePath = asksaveasfilename(defaultextension='.json')
    KPFile = editKeyPointsFile.KeyPointsFile(filePath)
    root.title(f'Key points file editor - {filePath}')


def saveFile():
    global KPFile
    KPFile.write()
    if KPFile.filePath == initialFilePath:
        savePath = asksaveasfilename(defaultextension='.json')
        if path.exists(savePath):
            remove(savePath)

        rename(initialFilePath, savePath)

        KPFile = editKeyPointsFile.KeyPointsFile(savePath)


def getFrameDataFromFile():
    global keyPointsDic, changeKeyPoints, original_value_x, original_value_y
    Framedata = KPFile.readFrame(pageNumStr.get())
    if Framedata is not None:
        for i, k in enumerate(keyPointsDic):
            keyPointsDic[k] = Framedata[i]
    else:
        pass

    value_x_, value_y_ = keyPointsDic[changeKeyPoints[0]]
    value_x.set(value_x_)
    value_y.set(value_y_)
    original_value_x = value_x_
    original_value_y = value_y_

    getValue_and_updateImage()


def changeFrameNum(delta):
    pageNum = int(pageNumStr.get()) + delta
    if pageNum >= 0:
        pageNumStr.set(str(pageNum))
    else:
        pageNumStr.set(str(0))

    getFrameDataFromFile()


def closeWindow():
    if KPFile is None:
        root.destroy()
        sys.exit()

    result = askyesnocancel('Save before quit', 'Save before quit?')

    if result is None:
        return
    if result:
        KPFile.write()
    root.destroy()
    sys.exit()


# set GUI
menus = tk.Menu(root)
M_file = tk.Menu(master=menus)
menus.add_cascade(label='File', menu=M_file)
M_file.add_command(label='new', command=createFile)
M_file.add_command(label='open', command=openFile)
M_file.add_command(label='save', command=saveFile)
root.config(menu=menus)

B_p_c = button(text='core',
               command=lambda: get_command_for_buttons(
                   'core position',
                   ['p_c', 'p_kn1', 'p_kn2', 'p_an1', 'p_an2', 'p_f1', 'p_f2', 'p_w', 'p_n', 'p_el1',
                    'p_el2', 'p_h1', 'p_h2']))
B_p_kn1 = button(text='knee1', command=lambda: get_command_for_buttons('knee1 position', ['p_kn1', 'p_an1', 'p_f1']))
B_p_kn2 = button(text='knee2', command=lambda: get_command_for_buttons('knee2 position', ['p_kn2', 'p_an2', 'p_f2']))
B_p_an1 = button(text='ankle1', command=lambda: get_command_for_buttons('ankle1 position', ['p_an1', 'p_f1']))
B_p_an2 = button(text='ankle2', command=lambda: get_command_for_buttons('ankle2 position', ['p_an2', 'p_f2']))
B_p_f1 = button(text='foot1', command=lambda: get_command_for_buttons('foot1 position', ['p_f1']))
B_p_f2 = button(text='foot2', command=lambda: get_command_for_buttons('foot2 position', ['p_f2']))
B_p_w = button(text='waist', command=lambda: get_command_for_buttons('waist position', ['p_w']))
B_p_n = button(text='neck', command=lambda: get_command_for_buttons('neck position', ['p_n', 'p_el1', 'p_el2', 'p_h1', 'p_h2']))
B_p_el1 = button(text='elbow1', command=lambda: get_command_for_buttons('elbow1 position', ['p_el1']))
B_p_el2 = button(text='elbow2', command=lambda: get_command_for_buttons('elbow2 position', ['p_el2']))
B_p_h1 = button(text='hand1', command=lambda: get_command_for_buttons('hand1 position', ['p_h1']))
B_p_h2 = button(text='hand2', command=lambda: get_command_for_buttons('hand2 position', ['p_h2']))
B_a_h = button(text='head',
               command=lambda: get_command_for_buttons(
                   'head angle', ['a_h'],
                   ScaleXSetting={'from': 0, 'to': 1, 'resolution': 1},
                   ScaleYSetting={'from': 180, 'to': -180}
               ))

text_L_selection = tk.StringVar()
L_selection = tk.Label(master=root, textvariable=text_L_selection)

_keyPoints = list(map(lambda a: tuple(keyPointsDic[a]), keyPointsDic))
viewImage = ImageTk.PhotoImage(drawImg((500, 500), _keyPoints, showCtrlPoints=True))
img_L_viewer = tk.Label(master=root, bg='gray', image=viewImage)

value_x = tk.IntVar()
Scale_x = tk.Scale(root, from_=0, to=170, length=680, variable=value_x, command=getValue_X, orient=tk.HORIZONTAL)
value_y = tk.IntVar()
Scale_y = tk.Scale(root, from_=0, to=170, length=680, variable=value_y, command=getValue_Y)

# B_save = button(text='save', command=lambda:1)
# B_open = button(text='open', command=lambda:1)
B_lastFrame = button(text='<', width=3, height=1,
                     command=lambda: changeFrameNum(-1))
B_nextFrame = button(text='>', width=3, height=1,
                     command=lambda: changeFrameNum(1))

pageNumStr = tk.StringVar()
pageNumStr.set('0')
E_FrameNum = tk.Entry(master=root, textvariable=pageNumStr, width=7)


L_selection.grid(row=0, column=5)
Scale_x.grid(row=1, column=5)
Scale_y.grid(row=2, column=4, rowspan=6)
B_p_c.grid(row=3, column=2)
B_p_kn1.grid(row=4, column=1)
B_p_kn2.grid(row=4, column=3)
B_p_an1.grid(row=5, column=1)
B_p_an2.grid(row=5, column=3)
B_p_f1.grid(row=6, column=1)
B_p_f2.grid(row=6, column=3)
B_p_w.grid(row=2, column=2)
B_p_n.grid(row=1, column=2)
B_p_el1.grid(row=2, column=1)
B_p_el2.grid(row=2, column=3)
B_p_h1.grid(row=3, column=1)
B_p_h2.grid(row=3, column=3)
B_a_h.grid(row=0, column=2)
img_L_viewer.grid(row=2, column=5, rowspan=6)
B_lastFrame.grid(row=7, column=1)
E_FrameNum.grid(row=7, column=2)
B_nextFrame.grid(row=7, column=3)


# set threads
updateGUIThread = threading.Thread(target=updateGUI)
updateGUIThread.setDaemon(True)
updateGUIThread.start()


# start
get_command_for_buttons(
    'core position',
    ['p_c', 'p_kn1', 'p_kn2', 'p_an1', 'p_an2',
     'p_f1', 'p_f2', 'p_w', 'p_n', 'p_el1', 'p_el2', 'p_h1', 'p_h2']
)
original_value_x, original_value_y = keyPointsDic['p_c']
root.protocol("WM_DELETE_WINDOW", closeWindow)
root.mainloop()
