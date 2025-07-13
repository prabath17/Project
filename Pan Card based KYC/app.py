import easyocr
import cv2
pan=input("Enter the PAN number: ")

reader = easyocr.Reader(['en'], gpu=False)

img = cv2.imread(r'C:\Users\praba\OneDrive\Documents\workspace\NOTHING\TASK_folder\PRABATH_PAN.jpg')


img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


result = reader.readtext(img_gray, detail=0)



for i,texts in enumerate(result):
    if texts == 'Permanent Account Number Card':
        ref_pan=result[i+1]
    elif texts=='Name':
        name=result[i+1]
    elif texts=='Date of Birth':
        DOB=result[i+2]
    
if(pan==ref_pan):
    print("Your PAN CARD has been verified \n")

    print(" Your Permanent Account Number Card :",ref_pan)

    print(" Your Name :",name)

    print(" Your Date of Birth :",DOB)




