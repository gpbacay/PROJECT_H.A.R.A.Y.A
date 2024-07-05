import os
import cv2
import numpy as np
import face_recognition as fr
from datetime import datetime
import mediapipe as mp
import pyttsx3


Header = "\nG.O.D.S.E.Y.E.S (Guided Object Detection and Surveillance for Enhanced Yield Evaluation System)\n"
print(Header)

haraya_engine = pyttsx3.init()
voices = haraya_engine.getProperty('voices')
haraya_engine.setProperty('voice', voices[0].id)

def speak(text):
    haraya_engine.say(text)
    haraya_engine.runAndWait()
    
def Play_Prompt_Sound():
    from playsound import playsound
    mp3_path = U"prompt1.mp3"
    playsound(mp3_path)

        
def Locate_NameHA(name):
    Honorific_Address = ""
    Male_Names = ["Gianne Bacay",
                "Earl Jay Tagud",
                "Gemmuel Balceda",
                "Mark Anthony Lagrosa",
                "Klausmieir Villegas",
                "CK Zoe Villegas", 
                "Pio Bustamante",
                "Rolyn Morales",
                "Alexander Villasis",
                "Meljohn Aborde",
                "Kimzie Torres"]

    Female_Names = ["Kleinieir Pearl Kandis Bacay",
                    "Princess Viznar",
                    "Nichi Bacay",
                    "Roz Waeschet Bacay",
                    "Killy Obligation",
                    "Jane Rose Bandoy"]

    if name in Male_Names:
        Honorific_Address = "Sir"
    elif name in Female_Names:
        Honorific_Address = "Ma'am"
    else:
        Honorific_Address = ""
    return Honorific_Address

Play_Prompt_Sound()
print("Initializing G.O.D.S.E.Y.E.S")
speak("Initializing GODSEYES...")

def Face_Pose_Recognition_System():
    def ClearCSV():
        import csv
        file = open("attendance.csv", "r")
        csvr = csv.reader(file)
        namelist = []
        Header = f'Name, Time'
        Header = Header.split(',')
        namelist.insert(0, Header)
        file = open("attendance.csv", "w", newline='')
        csvr = csv.writer(file)
        csvr.writerows(namelist)
        file.close()

    def get_encoded_faces():
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = fr.load_image_file("faces/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding
        return encoded

    def MarkAttendance(name):
        if name == "Unknown":
            response = "Unknown face was detected"
            print(response)
            speak(response)
        else:
            with open("attendance.csv", 'r+') as attendance:
                MyDatalist = attendance.readlines()
                NameList = []
                for line in MyDatalist:
                    entry = line.split(',')
                    NameList.append(entry[0])
                if name not in NameList:
                    now = datetime.now()
                    Time = now.strftime('%I:%M %p')
                    attendance.writelines(f'\n{name}, {Time}')
                    NameHA = Locate_NameHA(name)
                    response = f"{NameHA} {name} was detected!"
                    print(response)
                    speak(response)

    def resize(frame, size):
        width = int(frame.shape[1] * size)
        height = int(frame.shape[0] * size)
        dimension = (width, height)
        return cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)

    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    ClearCSV()

    with mp_holistic.Holistic(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        response = "System is now online."
        print(response)
        speak(response)
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame = resize(frame, 0.50)
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            results = holistic.process(frame)
            face_locations = fr.face_locations(frame)
            unknown_face_encodings = fr.face_encodings(frame, face_locations)
            face_names = []
            for face_encoding in unknown_face_encodings:
                matches = fr.compare_faces(faces_encoded, face_encoding)
                name = "Unknown"
                face_distances = fr.face_distance(faces_encoded, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    frame = frame.copy()
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=results.face_landmarks,
                        connections=mp_holistic.FACEMESH_TESSELATION,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))
                    font = cv2.FONT_HERSHEY_TRIPLEX
                    cv2.putText(frame, name, (left - 30, top - 30), font + 1, 1, (255, 255, 255), 1)
                    MarkAttendance(name)

            # Draw landmarks for hands, face, and pose
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
                landmark_list=results.pose_landmarks,
                connections=mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
            )

            cv2.imshow('AI Face Pose Recognition System', frame)
            if cv2.waitKey(30) & 0xff == 27:
                cap.release()
                cv2.destroyAllWindows()
                return face_names

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    Face_Pose_Recognition_System()
    Play_Prompt_Sound()
#______________________________python godseyes.py
