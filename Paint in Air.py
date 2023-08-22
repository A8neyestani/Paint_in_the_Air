"""
Interactive Drawing with Hand Detection
Author: Arman Neyestani 
https://github.com/A8neyestani
A8neyestani@protonmail.com


This module captures video from the webcam and allows users to draw lines by tracking their hand movements.
It also offers palette selections to change the color or use an eraser.
"""

import cv2
import handTrackingModule as htm

def initialize_capture(width, height):
    """Initialize video capture with specified width and height."""
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    return cap

def draw_palettes(frame, eraser_image, boxes):
    """Draw eraser and color palettes on the frame."""
    frame[boxes['eraser']['y1']:boxes['eraser']['y2'], boxes['eraser']['x1']:boxes['eraser']['x2']] = eraser_image
    
    for key, box in boxes.items():
        if key != 'eraser':
            color = box['color']
            thickness = -1 if 'plt' in key else 3
            frame = cv2.rectangle(frame, (box['x1'], box['y1']), (box['x2'], box['y2']), color, thickness)

    return frame

def handle_interactions(lmList, boxes):
    """Manage interactions with the Eraser and color palettes."""
    color = None
    clear = False

    try:
        if boxes['eraser']['x1'] < lmList[8][1] < boxes['eraser']['x2'] and boxes['eraser']['y1'] < lmList[8][2] < boxes['eraser']['y2']:
            clear = True
        for key, box in boxes.items():
            if 'plt' in key and box['x1'] < lmList[8][1] < box['x2'] and box['y1'] < lmList[8][2] < box['y2']:
                color = box['color']
    except IndexError:
        pass

    return color, clear

def main():
    WIDTH, HEIGHT = 640, 480
    eraser_image = cv2.resize(cv2.imread('eraser.png'), (100, 100))
    detector = htm.handDetector()

    boxes = {
        'eraser': {'x1': 500, 'y1': 0, 'x2': 600, 'y2': 100},
        'redplt': {'x1': 100, 'y1': 0, 'x2': 200, 'y2': 100, 'color': (0, 0, 255)},
        'blueplt': {'x1': 300, 'y1': 0, 'x2': 400, 'y2': 100, 'color': (255, 0, 0)}
    }

    finger_positions = []
    current_color = (0, 0, 255)  # Default color: red

    cap = initialize_capture(WIDTH, HEIGHT)

    while True:
        _, frame = cap.read()
        if frame is None:
            break

        frame = detector.findHands(frame)
        frame = draw_palettes(frame, eraser_image, boxes)

        lmList = detector.findPosition(frame, draw=False)

        if len(lmList) > 10 and abs(lmList[8][1] - lmList[5][1]) > 25:
            finger_positions.append([lmList[8][1], lmList[8][2]])

        for i in range(1, len(finger_positions)):
            frame = cv2.line(frame, tuple(finger_positions[i-1]), tuple(finger_positions[i]), current_color, 5)

        new_color, erase = handle_interactions(lmList, boxes)

        if new_color:
            current_color = new_color

        if erase:
            finger_positions.clear()

        cv2.imshow("Interactive Drawing", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
