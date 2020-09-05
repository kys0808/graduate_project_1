from PIL import Image
import glob
import xml.etree.ElementTree as elemTree
import xml
import random
import numpy as np
import cv2
import os
imgFiles = glob.glob("*.jpg")

def changeLabel(xmlPath, newXmlPath, imgPath, boxes):
    tree = elemTree.parse(xmlPath)

    # path 변경
    path = tree.find('./path')
    path.text = imgPath[0]

    # bounding box 변경
    objects = tree.findall('./object')
    for i, object_ in enumerate(objects):
        bndbox = object_.find('./bndbox')
        bndbox.find('./xmin').text = str(boxes[i][0])
        bndbox.find('./ymin').text = str(boxes[i][1])
        bndbox.find('./xmax').text = str(boxes[i][2])
        bndbox.find('./ymax').text = str(boxes[i][3])
    tree.write(newXmlPath, encoding='utf8')
def getSizeFromXML(object):
    tree = elemTree.parse(object)
    w, h = tree.find('./width'), tree.find('./height')
    return w, h

class RandomHorizontalFlip(object):
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, img, bboxes):
        img_center = np.array(img.shape[:2])[::-1]/2
        img_center = img_center.astype(int)
        img_center = np.hstack((img_center, img_center))
        if random.random() < self.p:
            img = img[:, ::-1, :]
            bboxes[:, [0, 2]] += 2*(img_center[[0, 2]] - bboxes[:, [0, 2]])
            box_w = abs(bboxes[:, 0] - bboxes[:, 2])
            bboxes[:, 0] -= box_w
            bboxes[:, 2] += box_w
        return img, bboxes

labelPath = "../xml/"
classes = "bollard.txt"

def getRectFromXML(label):
    tree = elemTree.parse(label)
    objects = tree.findall('./object')
    good = list()
    for i, object_ in enumerate(objects):
        bndbox = object_.find('./bndbox')
        x_min = bndbox.find('./xmin').text
        y_min = bndbox.find('./ymin').text
        x_max = bndbox.find('./xmax').text
        y_max = bndbox.find('./ymax').text
        boxes = [int(x_min), int(y_min), int(x_max), int(y_max)]
        good.append(np.array(boxes))
    return np.array(good)
for imgFile in imgFiles:
    fileName = imgFile.split('.')[0]
    label = f'{labelPath}{fileName}.xml'
    w, h = getSizeFromXML(label)

    # opencv loads images in bgr. the [:,:,::-1] does bgr -> rgb
    image = cv2.imread(imgFile)[:,:,::-1]
    bboxes = getRectFromXML(label)
    # HorizontalFlip image
    image, bboxes = RandomHorizontalFlip(1)(image.copy(), bboxes.copy())

    # Save image
    image = Image.fromarray(image, 'RGB')
    newImgPath = f'filps/'
    if not os.path.exists(newImgPath):
        os.makedirs(newImgPath)
    image.save(newImgPath + imgFile)

    # Save label
    newXmlPath = f'filps/label/'
    if not os.path.exists(newXmlPath):
        os.makedirs(newXmlPath)
    newXmlPath = newXmlPath + fileName + '.xml'
    changeLabel(label, newXmlPath, newImgPath, bboxes)