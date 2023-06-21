import cv2

cap= cv2.VideoCapture(0)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 5)
cap.set(cv2.CAP_PROP_CONTRAST, 64)
cap.set(cv2.CAP_PROP_HUE, 0)
cap.set(cv2.CAP_PROP_SATURATION, 0)
cap.set(cv2.CAP_PROP_SHARPNESS, 6)
cap.set(cv2.CAP_PROP_GAMMA, 100)
cap.set(cv2.CAP_PROP_GAIN, 25)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

writer= cv2.VideoWriter('Data/basicvideo.mp4', cv2.VideoWriter_fourcc(*"MPJG"), 30.0, (width,height))
record = False

while True:
    ret,frame= cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    if record == True:
        writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('w'):
        print("BEGINNING RECORDING")
        record = True


cap.release()
writer.release()
cv2.destroyAllWindows()