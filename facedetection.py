import subprocess 

#################################Preparando el ambiente de trabajo#######################################

# Instalar numpy 
subprocess.run(["pip3", "install", "numpy"])

# Instalar opencv-python 
subprocess.run(["pip3", "install", "opencv-python"])

# Instalar tflite_runtime 
subprocess.run(["pip3", "install", "tflite_runtime"])

#########################################################################################################

import numpy as np
import cv2
import datetime
import time
import tflite_runtime.interpreter as tflite

Interpreter = tflite.Interpreter(model_path="model.tflite")
Interpreter.allocate_tensors()

input_details = Interpreter.get_input_details()
output_details = Interpreter.get_output_details()

cv2.ocl.setUseOpenCL(False)

emotion_dict = {0: "Enojado", 1: "Disgustado", 2: "Temeroso", 3: "Feliz", 4: "Neutral", 5: "Triste", 6: "Sorprendido"}

cap = cv2.VideoCapture(0)
Emotions_File = open("emotions_detected.csv", "a")

# Inicializa un contador de tiempo
start_time = time.time()

# Inicializa la variable frame fuera del bloque if
frame = None

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time >= 1.0:
        
        ret, frame = cap.read()
        if not ret:
            break
        facecasc = cv2.CascadeClassifier('cascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            cropped_img = np.array(cropped_img, dtype='f')
            Interpreter.set_tensor(input_details[0]['index'], cropped_img)
            Interpreter.invoke()
            output_data = Interpreter.get_tensor(output_details[0]['index'])
            maxindex = int(np.argmax(output_data))
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), 2, cv2.LINE_AA)

            emocion = emotion_dict[maxindex]
            tc = datetime.datetime.now()
            ts = time.time()
            Emotions_File.write(str((emocion)) + ";" + str(tc) + ";" + str(ts) + "\n")
            
        start_time = current_time

    if frame is not None:  # Comprueba si frame no está vacío antes de redimensionarlo
        cv2.imshow('Video', cv2.resize(frame, (800, 480), interpolation=cv2.INTER_CUBIC))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Emotions_File.close()
cap.release()
cv2.destroyAllWindows()
