import cv2
import streamlit as st
import numpy as np
from PIL import Image
import time
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("Akses Kamera IP secara Real-time")

camera_url = st.text_input("Masukkan URL Kamera IP:",
                           'http://192.168.1.17:8080/video')

receiver_email = st.text_input("Masukkan Email Penerima:", '')

FRAME_WINDOW = st.empty()

cap = cv2.VideoCapture(camera_url)

while True:
    ret, frame = cap.read()
    model = YOLO('api.pt')
    results = model(source=frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    FRAME_WINDOW.image(img)
    time.sleep(0.003)  # jeda 30 milidetik

    for result in results:
        if result:
            for box in result.boxes:
                cls = int(box.cls.item())
                if cls == 0:
                    # Pengaturan email pengirim
                    sender_email = "apialrm727@gmail.com"
                    sender_password = "nvlm ynph suqb xfwl"

                    # Membuat objek pesan
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    message["Subject"] = "API TERDETEKSI"

                    # Isi pesan
                    body = "CARI LOKASINYA"
                    message.attach(MIMEText(body, "plain"))

                    # Mengonfigurasi server SMTP untuk Gmail
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587

                    # Membuat koneksi ke server SMTP
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()

                    # Login ke akun Gmail
                    server.login(sender_email, sender_password)

                    # Mengirim email
                    server.sendmail(sender_email, receiver_email,
                                    message.as_string())

                    # Menutup koneksi
                    server.quit()

                    print("email peringatan terkirim")

cap.release()
