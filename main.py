import cv2
import numpy as np
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone


with open("quistion.csv", newline="\n") as f:
    csv_reader = csv.reader(f)

    All_data = list(csv_reader)[1:]


class Quize():

    def __init__(self, data):
        self.quition = data[0]
        self.choise1 = data[1]
        self.choise2 = data[2]
        self.choise3 = data[3]
        self.choise4 = data[4]
        self.Answer = int(data[5])

        self.userAns = None

    def choise(self, cursor, bboxes):

        for i, bbox in enumerate(bboxes):
            if bbox[0] < cursor[0] < bbox[2] and bbox[1] < cursor[1] < bbox[3]:
                cv2.rectangle(
                    img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), cv2.FILLED)
                self.userAns = i+1


detector = HandDetector(detectionCon=0.8)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

correctAns = 0
totalQution = len(All_data)

currentQuition = 0
delly = 0

AllQution = []
for q in All_data:
    AllQution.append(Quize(q))


while True:
    # print(currentQuition)
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if (currentQuition < totalQution):
        data = AllQution[currentQuition]

        hands, img = detector.findHands(img, draw=True)

        img, bbox4 = cvzone.putTextRect(img, f'quiz {currentQuition}', (500, 50), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0))

        img, bbox = cvzone.putTextRect(img, data.quition, (300, 150), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        img, bbox1 = cvzone.putTextRect(img, data.choise1, (350, 300), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        img, bbox2 = cvzone.putTextRect(img, data.choise2, (700, 300), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        img, bbox3 = cvzone.putTextRect(img, data.choise3, (350, 500), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        img, bbox4 = cvzone.putTextRect(img, data.choise4, (700, 500), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        if hands:
            lmList = hands[0]["lmList"]
            cursor = lmList[8]

            length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img, color=(255, 0, 255),
                                                      scale=10)
            if (length < 40 and delly == 0):

                data.choise(cursor, [bbox1, bbox2, bbox3, bbox4])

                if data.userAns is not None:
                    delly += 1

                    # time.sleep(0.8)
                    # print(data.userAns, data.Answer)
                    # print("ok")
                    if (data.userAns == data.Answer):

                        correctAns += 1

                    currentQuition += 1
            if (delly != 0):
                delly += 1
                if (delly > 10):
                    delly = 0

    else:
        img, bbox = cvzone.putTextRect(img, f'your soccer is  {str(round(correctAns/totalQution, 1)*100) }%', (300, 100), border=2, colorB=(
            0, 0, 0), colorT=(0, 0, 255), colorR=(0, 255, 0), offset=30)

        #     pass
    cv2.rectangle(img, (100, 600), (1100, 650), (255, 255, 255), 3)
    # print(currentQuition*1000/totalQution)

    cv2.rectangle(img, (100, 600), (int(100+currentQuition*1000/totalQution), 650),
                  (0, 255, 0), cv2.FILLED)

    cv2.imshow("img", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindows()
        break
    if key == ord("a"):
        currentQuition = 0
        correctAns = 0
        for q in All_data:
            AllQution.append(Quize(q))
