import cv2
import mediapipe as mp
import pygame
import math
import time

pygame.mixer.init()
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

piano_notes = ['a1', 'a1s', 'b1', 'c1', 'c1s', 'd1', 'd1s', 'e1', 'f1', 'f1s', 'g1', 'g1s', 'c2']
piano_sounds = {note: pygame.mixer.Sound(f'sounds/{note}.wav') for note in piano_notes}

drum_sounds = {
    'crash': pygame.mixer.Sound('drums/crash.wav'),
    'ride': pygame.mixer.Sound('drums/ride.wav'),
    'snare': pygame.mixer.Sound('drums/snare.wav'),
    'tom': pygame.mixer.Sound('drums/tom.wav'),
    'rimshot': pygame.mixer.Sound('drums/rimshot.wav'),
    'mallet': pygame.mixer.Sound('drums/mallet.wav'),
    'red': pygame.mixer.Sound('drums/red.wav')
}

mode = None
pressed = {}
highlight_drum = {}
prev_finger_pos = {}
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame_height, frame_width = frame.shape[:2]
key_width = frame_width // len(piano_notes)

drum_layout = {
    'crash':    {'pos': (int(0.25 * frame_width), int(0.2 * frame_height)), 'radius': 50, 'color': (255, 255, 0)},
    'ride':     {'pos': (int(0.75 * frame_width), int(0.2 * frame_height)), 'radius': 50, 'color': (0, 255, 255)},
    'snare':    {'pos': (int(0.2 * frame_width), int(0.5 * frame_height)), 'radius': 45, 'color': (0, 255, 0)},
    'tom':      {'pos': (int(0.5 * frame_width), int(0.5 * frame_height)), 'radius': 45, 'color': (0, 0, 255)},
    'rimshot':  {'pos': (int(0.8 * frame_width), int(0.5 * frame_height)), 'radius': 45, 'color': (255, 0, 0)},
    'mallet':   {'pos': (int(0.5 * frame_width), int(0.75 * frame_height)), 'radius': 55, 'color': (255, 0, 255)},
    'red':      {'pos': (int(0.1 * frame_width), int(0.75 * frame_height)), 'radius': 45, 'color': (255, 150, 0)}
}

def get_finger_movement(id, current):
    prev = prev_finger_pos.get(id)
    prev_finger_pos[id] = current
    if not prev:
        return 0
    return abs(current[1] - prev[1])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    fingers = []

    if result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y = int(hand_landmarks.landmark[8].y * frame.shape[0])
            fingers.append((x, y))
            cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)

    for _, y in fingers:
        if y < 50:
            mode = None
            time.sleep(1)

    if mode is None:
        half = frame.shape[1] // 2
        cv2.rectangle(frame, (0, 0), (half, frame.shape[0]), (100, 100, 255), -1)
        cv2.rectangle(frame, (half, 0), (frame.shape[1], frame.shape[0]), (255, 100, 100), -1)
        cv2.putText(frame, "PIANO", (half // 2 - 60, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.putText(frame, "DRUM", (half + half // 2 - 60, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        for x, y in fingers:
            if y < frame.shape[0] // 2:
                if x < half:
                    mode = "piano"
                else:
                    mode = "drum"
                time.sleep(1)
                break

    elif mode == "piano":
        for i, note in enumerate(piano_notes):
            x1 = i * key_width
            x2 = (i + 1) * key_width
            color = (50, 50, 50) if 's' in note else (255, 255, 255)
            text_color = (255, 255, 255) if 's' in note else (0, 0, 0)
            cv2.rectangle(frame, (x1, 0), (x2, int(0.25 * frame_height)), color, -1)
            cv2.rectangle(frame, (x1, 0), (x2, int(0.25 * frame_height)), (0, 0, 0), 2)
            cv2.putText(frame, note.upper(), (x1 + 5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

        for i, (x, y) in enumerate(fingers):
            move_y = get_finger_movement(f"piano_{i}", (x, y))
            key_index = x // key_width
            if key_index < len(piano_notes) and y < int(0.25 * frame_height):
                note = piano_notes[key_index]
                key = (note, 'piano')
                if not pressed.get(key, False) and move_y > 10:
                    piano_sounds[note].play()
                    pressed[key] = True
            else:
                for note in piano_notes:
                    pressed[(note, 'piano')] = False

    elif mode == "drum":
        for drum, info in drum_layout.items():
            x, y = info['pos']
            r = info['radius']
            base_color = (255, 255, 255) if highlight_drum.get(drum, False) else info['color']
            cv2.circle(frame, (x + 4, y + 4), r + 2, (0, 0, 0), -1)
            cv2.circle(frame, (x, y), r, base_color, -1)
            cv2.circle(frame, (x, y), r, (0, 0, 0), 2)
            cv2.putText(frame, drum.upper(), (x - 30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        if fingers:
            x_f, y_f = fingers[0]  # Only index finger (landmark 8)
            move_y = get_finger_movement("drum_index", (x_f, y_f))
            for drum, info in drum_layout.items():
                x_d, y_d = info['pos']
                r = info['radius']
                dist = math.hypot(x_f - x_d, y_f - y_d)
                key = (drum, 'drum')
                if dist < r:
                    if not pressed.get(key, False) and move_y > 10:
                        drum_sounds[drum].play()
                        highlight_drum[drum] = True
                        pressed[key] = True
                else:
                    pressed[key] = False

        for drum in highlight_drum:
            if highlight_drum[drum]:
                highlight_drum[drum] = False

    cv2.imshow("Virtual Instrument", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
