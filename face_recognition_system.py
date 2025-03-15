import os
import cv2
import numpy as np
import face_recognition as fr
from datetime import  datetime
import mediapipe as mp

def FaceRecognitionSystem():
    def ClearCSV():
        import csv
        file = open("attendance.csv", "r")
        csvr = csv.reader(file)
        namelist = []
        Header = f'Name, Time'
        Header = Header.split(',')
        namelist.insert(0, Header)
        file = open("attendance.csv", "w", newline = '')
        csvr = csv.writer(file)
        csvr.writerows(namelist)
        file.close()
    def get_encoded_faces():
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = fr.load_image_file("faces/" + f)
                    face_encodings = fr.face_encodings(face)
                    if len(face_encodings) > 0:
                        encoding = face_encodings[0]
                        encoded[f.split(".")[0]] = encoding
        return encoded
    def MarkAttendance(name):
        with open("attendance.csv", 'r+') as attendance:
            MyDatalist =  attendance.readlines()
            NameList = []
            for line in MyDatalist :
                entry = line.split(',')
                NameList.append(entry[0])
            if name not in NameList:
                now = datetime.now()
                Time = now.strftime('%H:%M')
                attendance.writelines(f'\n{name}, {Time}')
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    mp_holistic = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    ClearCSV()
    with mp_holistic.Holistic(static_image_mode = True, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as holistic:
        while True:
            success, frame = cap.read()
            if not success:
                break
            def resize(frame, size) :
                width = int(frame.shape[1]*size)
                height = int(frame.shape[0] * size)
                dimension = (width, height)
                return cv2.resize(frame, dimension, interpolation = cv2.INTER_AREA)
            frame = resize(frame, 0.50)
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            results = holistic.process(frame)
            face_locations = fr.face_locations(frame)
            unknown_face_encodings = fr.face_encodings(frame, face_locations)
            face_names = []
            for face_encoding in unknown_face_encodings:
                matches = fr.compare_faces(faces_encoded, face_encoding)
                name = "Unidentified"
                face_distances = fr.face_distance(faces_encoded, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    frame = frame.copy()
                    mp_drawing.draw_landmarks(
                        image = frame, 
                        landmark_list = results.face_landmarks, 
                        connections = mp_holistic.FACEMESH_TESSELATION,
                        landmark_drawing_spec = mp_drawing.DrawingSpec(color = (0,255,0), thickness = 1, circle_radius = 1),
                        connection_drawing_spec = mp_drawing.DrawingSpec(color = (0,255,0), thickness = 1, circle_radius = 1))
                    font = cv2.FONT_HERSHEY_TRIPLEX
                    cv2.putText(frame, name, (left -30, top -30), font + 1, 1, (255, 255, 255), 1)
                    MarkAttendance(name)
            cv2.imshow('AI Face Recognition System', frame)
            key = cv2.waitKey(30) & 0xff
            max_faces = 1
            if len(face_names) >= max_faces or key == 27:
                cap.release()
                cv2.destroyAllWindows()
                return face_names

if __name__ == '__main__':
    FaceRecognitionSystem()
    
#Run Command: python facerec.py