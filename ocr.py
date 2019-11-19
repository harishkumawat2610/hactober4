from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
from datetime import datetime

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done")
args = vars(ap.parse_args())
# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)


filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

text = pytesseract.image_to_string(Image.open(os.getcwd()+"/"+filename))
os.remove(filename)
print(text)
dates_list=[]
dates=["[\d]{1,2}/[\d]{1,2}/[\d]{4}",
       "[\d]{1,2}-[\d]{1,2}-[\d]{2}",
       "[\d]{1,2} [ADFJMNOS]\w* [\d]{4}",
       "([\d]{1,2}\s(JAN|NOV|OCT|DEC)\s[\d]{4})",
       "[\d]{1,2} [ADFJMNOS]\w* [\d]{4}",
       "([\d]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})",
       "(\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})",
       "[\d]{1,2}/[\d]{1,2}/[\d]{2}",
       "([\d]{1,2}\s(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT|NOV|OCT|DEC)\s[\d]{4})",
       "[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Nov|Oct|Dec]\s[\d]{1,2}(,|')\s[\d]{4}",
       "[JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER]\s[\d]{1,2}(,|')\s[\d]{4}"

    ]
for i in range(0,len(dates)):
    print(i)
    match = re.findall(dates[i], text)
    dates_list.append(match)
print(dates_list)

# show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)
