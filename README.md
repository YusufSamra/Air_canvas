# AirCanvas – Virtual Air Drawing System

AirCanvas is a real-time virtual drawing application that allows users to draw in the air using hand gestures.

The project uses the computer's webcam to detect and track hand landmarks with MediaPipe. The position of the index finger is used as a virtual drawing pointer, allowing the user to draw on a digital canvas without touching a physical surface.

## Features

- Real-time hand tracking using MediaPipe
- Air drawing using the index finger
- Smooth finger movement using position smoothing
- Hand landmark visualization
- Draw on a virtual canvas using OpenCV
- Clear the canvas using a hand gesture
- Undo the last drawing action
- Save the drawing as an image
- Exit the application using the `Q` key

## Hand Gestures

| Gesture | Action |
|---|---|
| Index finger up | Start drawing |
| All fingers up | Stop drawing |
| No fingers up | Clear canvas |
| Index + middle fingers up | Undo last drawing |

## Controls

- `Q` → Exit the application
- `S` → Save the current drawing as `drawing.png`

## Technologies Used

- Python
- OpenCV
- NumPy
- MediaPipe

## How It Works

1. The webcam captures the user's hand.
2. MediaPipe detects the hand landmarks.
3. The index finger tip is tracked in real time.
4. The finger position is smoothed to reduce unwanted movement.
5. When the drawing gesture is detected, OpenCV draws lines on the virtual canvas.
6. Different hand gestures are used to control drawing, clearing, and undo operations.

## Installation

Install the required libraries:

```bash
pip install opencv-python numpy mediapipe
