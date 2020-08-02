import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image = cv2.imread('plate.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny_edge = cv2.Canny(gray,150, 150)

contours, new  = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]

# Initialize license Plate contour and x,y coordinates
contour_with_license_plate = None
license_plate = None
x = None
y = None
w = None
h = None

# Find the contour with 4 potential corners and creat ROI around it
for contour in contours:
        # Find Perimeter of contour and it should be a closed contour
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if len(approx) == 4: #see whether it is a Rect
            contour_with_license_plate = approx
            x, y, w, h = cv2.boundingRect(contour)
            license_plate = gray[y:y + h, x:x + w]
            cv2.imshow("de",license_plate)
            break

# Removing Noise from the detected image, before sending to Tesseract
#license_plate = cv2.bilateralFilter(license_plate, 11, 14, 15)

#(thresh, license_plate) = cv2.threshold(license_plate, 170, 190, cv2.THRESH_BINARY)

#Text Recognition
text = pytesseract.image_to_string(license_plate)
#Draw License Plate and write the Text
image = cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 3)
image = cv2.putText(image, text, (x-52,y-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

print("License Plate :", text)

cv2.imshow("License Plate Detection",image)
cv2.waitKey(0)
