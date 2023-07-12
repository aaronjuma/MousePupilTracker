import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)
print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()