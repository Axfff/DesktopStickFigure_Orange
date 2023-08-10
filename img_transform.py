from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os


def transform(imgPath, size, targetPath):
    img = Image.open(imgPath).convert('RGBA')
    img = img.resize(size, resample=Image.NEAREST)
    # photo = photo.filter
    # photo = ImageEnhance.Contrast(photo).enhance(1.3)
    # print(photo.mode)
    img.save(targetPath)


def transform_for_folder():
    SUPPORTEDfORMAT = ['jpg', 'png']
    for imgName in os.listdir(path=r'imgs'):
        if imgName.split('.')[-1] in SUPPORTEDfORMAT:
            imgPath = os.path.join(r'imgs', imgName)
            targetPath = os.path.join(r'run_imgs', imgName)
            transform(imgPath, (170, 170), targetPath)


def fillColor(imgPath, color=(255, 112, 0, 255)):
    img = Image.open(imgPath).convert('RGBA')
    img_array = img.load()
    for h in range(img.height):
        for w in range(img.width):
            if img_array[w, h][3] != 0 and img_array[w, h] != color:
                img_array[w, h] = color
    img.save(imgPath+'.png')


if __name__ == '__main__':
    fillColor(r'headLeftSquare.png')


