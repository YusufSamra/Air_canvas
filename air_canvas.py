import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
history = []   

prev_x, prev_y = None, None
alpha = 0.6
smooth_x, smooth_y = None, None

drawing = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        h, w, _ = frame.shape

        mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        lm = handLms.landmark[8]
        x, y = int(lm.x * w), int(lm.y * h)

        if smooth_x is None:
            smooth_x, smooth_y = x, y
        else:
            smooth_x = int(alpha * x + (1 - alpha) * smooth_x)
            smooth_y = int(alpha * y + (1 - alpha) * smooth_y)

        draw_x, draw_y = smooth_x, smooth_y

        fingers = []
        tips = [8, 12, 16, 20]
        for tip in tips:
            fingers.append(handLms.landmark[tip].y < handLms.landmark[tip - 2].y)

        index_up = fingers[0]
        middle_up = fingers[1]
        all_up = all(fingers)
        none_up = not any(fingers)

        if index_up and not middle_up and not fingers[2] and not fingers[3]:
            drawing = True

        elif all_up:
            drawing = False
            prev_x, prev_y = None, None

        elif none_up:
            canvas = np.zeros((480, 640, 3), dtype=np.uint8)
            history.clear()
            prev_x, prev_y = None, None

        elif index_up and middle_up and not fingers[2] and not fingers[3]:
            if history:
                canvas = history.pop()
            prev_x, prev_y = None, None
            drawing = False

        if drawing:
            cv2.circle(frame, (draw_x, draw_y), 6, (0, 255, 0), -1)
            if prev_x is not None:
                history.append(canvas.copy())
                cv2.line(canvas, (prev_x, prev_y), (draw_x, draw_y), (0, 255, 0), 4)
            prev_x, prev_y = draw_x, draw_y
        else:
            prev_x, prev_y = None, None

    else:
        smooth_x, smooth_y = None, None
        prev_x, prev_y = None, None

    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    cv2.imshow("Air Drawing", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("drawing.png", canvas)
        print("Saved drawing.png")

cap.release()
cv2.destroyAllWindows()
