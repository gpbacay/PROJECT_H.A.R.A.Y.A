import mediapipe as mp
import cv2
import datetime
    
def Pose_Recognition_System():
    global position
    position = " "
        
    def setPosition(input_position: str):
        global position
        position = input_position
        
    def getPosition():
        return position
    
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils

    # Capture video
    cap = cv2.VideoCapture(0)

    # Frames Per Second
    fps_start_time = datetime.datetime.now()
    fps = 0
    total_frames = 0

    # Initialize MediaPipe Holistic
    with mp_holistic.Holistic(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        while True:
            success, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not success:
                break

            # Process frame with MediaPipe Holistic
            total_frames += 1
            results = holistic.process(frame)

            # Print Nose Coordinates
            image_height, image_width, _ = frame.shape
            if results.pose_landmarks:
                nose_x = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width
                nose_y = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height
            
                if round(nose_x) < 300 and round(nose_y) < 300:
                    setPosition(input_position="Upper Left")
                    print(f'\rNose Coordinates: ({round(nose_x)}, {round(nose_y)}), {getPosition()}', end="\r")
                elif round(nose_x) > 300 and round(nose_y) < 300:
                    setPosition(input_position="Upper Right")
                    print(f'\rNose Coordinates: ({round(nose_x)}, {round(nose_y)}), {getPosition()}', end="\r")
                elif round(nose_x) < 300 and round(nose_y) > 300:
                    setPosition(input_position="Lower Left")
                    print(f'\rNose Coordinates: ({round(nose_x)}, {round(nose_y)}), {getPosition()}', end="\r")
                elif round(nose_x) > 300 and round(nose_y) > 300:
                    setPosition(input_position="Lower Right")
                    print(f'\rNose Coordinates: ({round(nose_x)}, {round(nose_y)}), {getPosition()}', end="\r")

            #Run command: python poserec.py
            # Draw Landmarks
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.left_hand_landmarks,
                connections=mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1)
            )
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.right_hand_landmarks,
                connections=mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1)
            )
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.face_landmarks,
                connections=mp_holistic.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1)
            )
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=results.pose_landmarks,
                    connections=mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )

            # Calculate and display FPS
            fps_end_time = datetime.datetime.now()
            time_diff = fps_end_time - fps_start_time
            if time_diff.seconds == 0:
                fps = 0
            else:
                fps = (total_frames / time_diff.seconds) * 10
            fps_text = "fps"
            cv2.putText(frame, str(int(fps)) + fps_text, (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)

            # Show Frames Per Second
            cv2.imshow("Pose Recognition AI System", frame)

            # Terminate the Program
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    Pose_Recognition_System()
    
#Run command: python poserec.py
