import cv2

index = 0
frames = []

while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        print(f"Camera Device {index}: OK")

    index += 1

while True:
    index = 0
    frames = []

    # Capture frames from all connected cameras
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        ret, frame = cap.read()
        frames.append(frame)
        index += 1

    # Concatenate frames horizontally and display the result
    if frames:
        result = cv2.hconcat(frames)
        cv2.imshow("Video Feed", result)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
