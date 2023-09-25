def Face_Log_In():
    import cv2
    import ctypes

    # Load the cascade for face detection
    face_cascade = cv2.CascadeClassifier("C:\\Users\\Gianne Bacay\\Desktop\\PROJECT-H.A.R.A.Y.A\\haarcascade_frontalface_default.xml")

    # Start the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the output
        cv2.imshow("Face detection", img)

        # If a face is detected, log the user into the computer
        if len(faces) > 0:
            ctypes.windll.user32.LockWorkStation()
            break

        # Stop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()

    # Close the window
    cv2.destroyAllWindows()
#________________python facelogin.py