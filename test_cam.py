import cv2

print("FILE LOADED") 

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    print("RET =", ret)
    if ret:
        cv2.imshow("Cam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
