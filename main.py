import time
import cv2
import numpy as np
import glob
from skimage import io
import pandas as pd
import csv


def onClick(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x = %d, y = %d" % (x, y))


def roll(file):
    img = cv2.imread(file)
    roll1 = img[238:462, 112:316]
    roll2 = img[238:462, 346:550]
    roll3 = img[238:462, 580:785]
    roll4 = img[238:462, 815:1020]
    roll5 = img[238:462, 1048:1255]
    roll6 = img[238:462, 1284:1490]
    roll7 = img[518:742, 230:435]
    roll8 = img[518:742, 463:668]
    roll9 = img[518:742, 697:903]
    roll10 = img[518:742, 932:1137]
    roll11 = img[518:742, 1165:1370]
    return roll1, roll2, roll3, roll4, roll5, roll6, roll7, roll8, roll9, roll10, roll11


def mse(img1, img2):
    result = np.sum((img1.astype("float") - img2.astype("float"))**2)
    result /= float(img1.shape[0] * img1.shape[1])

    return result


def count_countours(img):
    image = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)

    a = cv2.resize(image[112:132, 57:129], (360, 100))
    b = cv2.cvtColor(cv2.resize(img[138:147, 33:105], (350, 50)), cv2.COLOR_BGR2GRAY)
    b = cv2.Canny(b, 50, 100)

    lower = np.array([22, 100, 180], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")
    mask = cv2.inRange(a, lower, upper)

    contours1, hierarchy1 = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours2, hierarchy2 = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(a, contours1, -1, (255, 0, 0), 3)
    cv2.drawContours(b, contours2, -1, (255, 0, 0), 3)

    count = 0
    for contour in contours1:
        area = cv2.contourArea(contour)
        if 2000 < area < 3000:
            m = cv2.moments(contour)
            y = int(m["m01"] / m["m00"])
            if a.shape[0]*3/7 < y < a.shape[0]*4/7:
                count += 1

    # cv2.imshow("Star", a)
    # cv2.waitKey(0)
    # cv2.imshow("Title", b)
    # cv2.waitKey(0)

    return ("CE", count, a, b) if len(contours2) > 80 else ("Servant", count, a, b)


servants = pd.read_csv("servant_data/Servants.csv")
ser_img = []
for directory in servants['Directory']:
    img = io.imread(directory)
    ser_img.append(cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))

with open("gacha_data/gachas.csv", 'w') as f:
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    writer.writerow(["CardType","Rarity","ServantName","Class","Avail","Time"])
    f.close()
completed = set()
while True:
    screenshots = set(glob.glob("gacha_data/*.png")) - completed
    for shot in sorted(screenshots):
        with open("gacha_data/gachas.csv", 'a') as ap:
            imgs = roll(shot)
            for img in imgs:
                img = cv2.resize(img, (138, 150))
                card = list(count_countours(img))

                if card[0] == "Servant":
                    mse_num = []
                    for image in ser_img:
                        mse_num.append(mse(image, img))
                    diff = np.min(mse_num)
                    info = servants.iloc[mse_num.index(diff)]
                    if diff < 19500 and info[1] == card[1]:
                        card = card[:2]
                        card.extend([info[0], info[2], info[3], diff, shot[22:-4]])
                    else:
                        print("Failure: " + str(info) + str(card[:2]))
                        cv2.imshow("Star", card[2])
                        cv2.imshow("Type", card[3])
                        cv2.waitKey(0)
                        mse_num.sort()
                        print(mse_num)
                else:
                    card = card[:2]
                    card.extend(["", "", "", "", shot[22:-4]])

                writer = csv.writer(ap, delimiter=',', lineterminator='\n')
                writer.writerow(card)
            completed.add(shot)
            ap.close()
    time.sleep(3)
