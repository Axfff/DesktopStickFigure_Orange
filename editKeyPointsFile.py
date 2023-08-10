import json
import os.path

# initialMotion = {'p_c': [255, 315],
#                  'p_kn1': [250, 410], 'p_kn2': [280, 405],
#                  'p_an1': [235, 491], 'p_an2': [289, 491],
#                  'p_f1': [235, 491], 'p_f2': [289, 491],
#                  'p_w': [255, 275],
#                  'p_n': [265, 230],
#                  'p_el1': [230, 281], 'p_el2': [270, 289],
#                  'p_h1': [229, 335], 'p_h2': [286, 320],
#                  'a_h': [1, -8]
#                  }
initialMotion = [[255, 315],
                 [250, 410], [280, 405],
                 [235, 491], [289, 491],
                 [235, 491], [289, 491],
                 [255, 275],
                 [265, 230],
                 [230, 281], [270, 289],
                 [229, 335], [286, 320],
                 [1, -8]]


def writeJson(filePath, dictionary):
    with open(filePath, 'w') as jsonFile:
        json.dump(dictionary, jsonFile)


def readJson(filePath):
    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        return json.load(jsonFile)


class KeyPointsFile:
    def __init__(self, filePath):
        if not filePath:
            # No file path input.
            return

        self.filePath = filePath
        if not os.path.exists(filePath):
            # File path not exist, create.
            self.data = {0: initialMotion}
            self.write()
        self.data = readJson(filePath)

    def addFrame(self, frameNum, keyPoints):
        self.data[frameNum] = keyPoints

    def readFrame(self, frameNum):
        try:
            # self.data[frameNum] is not None
            return self.data[frameNum]
        except:
            return None

    def write(self):
        _dataSorted = sorted(self.data.items(), key=lambda x: x[0])
        self.data = {}
        for k, i in _dataSorted:
            self.data[k] = i

        writeJson(self.filePath, self.data)


if __name__ == '__main__':
    # l = []
    # for k in initialMotion:
    #     l.append(initialMotion[k])
    # print(l)
    import tkinter
    a = KeyPiontsFile()
