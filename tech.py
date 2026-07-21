import cv2
from ultralytics import YOLO
# Load YOLO model
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("road.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if label in ["car","bus","truck","motorcycle","bicycle"]:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame,label,(x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.imshow("Vehicle Detection", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()