import cv2
import mediapipe as mp
import serial
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

def connect_arduino():
    for attempt in range(5):
        try:
            ser = serial.Serial(
                port='COM16',
                baudrate=115200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1,
                write_timeout=1
            )
            time.sleep(2)
            print("Connected on COM16 at 115200 baud")
            return ser
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            time.sleep(1)
    return None

def count_fingers(hand_landmarks):
    landmarks = hand_landmarks.landmark
    fingers = [
        landmarks[4].x < landmarks[3].x - 0.02,  
        landmarks[8].y < landmarks[6].y - 0.02,  
        landmarks[12].y < landmarks[10].y - 0.02, 
        landmarks[16].y < landmarks[14].y - 0.02,
        landmarks[20].y < landmarks[18].y - 0.02
    ]
    return sum(fingers)

def main():
    ser = connect_arduino()
    cap = cv2.VideoCapture(0)
    prev_count = -1
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            continue
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        finger_count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                
                finger_count = count_fingers(hand_landmarks)
        
        
        if 0 <= finger_count <= 5 and finger_count != prev_count:
            if ser and ser.is_open:
                try:
                    ser.write(f"{finger_count}\n".encode())
                    ser.flush()
                    print(f"Sent: {finger_count} fingers")
                    prev_count = finger_count
                except Exception as e:
                    print(f"Send error: {e}")
                    ser = connect_arduino()
        
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        relay_state = "ON" if finger_count in [1,3] else "OFF"
        cv2.putText(frame, f"Relay: {relay_state}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, "COM16: " + ("Connected" if ser else "Disconnected"), 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.imshow('Finger Control with Joints', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    if ser:
        ser.close()

if __name__ == "__main__":
    main()