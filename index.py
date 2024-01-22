from ultralytics import YOLO
import streamlit as st
from PIL import Image, ImageDraw
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tempfile import NamedTemporaryFile
import cv2

# Load a model
model = YOLO('api.pt')  # pretrained YOLOv8n model

# Streamlit app
st.title("Object Detection with YOLO")

# Sidebar to upload files and input receiver email
uploaded_file = st.sidebar.file_uploader("Choose an image or video...", type=[
                                         "jpg", "jpeg", "png", "mp4"])
receiver_email = st.sidebar.text_input("Enter Receiver's Email Address", "")

if uploaded_file is not None:
    # Check if the uploaded file is an image or video
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Run inference on the image
        results = model(image)

        # Process results
        for result in results:
            if result:
                for box in result.boxes:
                    cls = int(box.cls.item())
                    if cls == 0 and receiver_email:
                        # Alert email configuration
                        sender_email = "apialrm727@gmail.com"
                        sender_password = "nvlm ynph suqb xfwl"

                        message = MIMEMultipart()
                        message["From"] = sender_email
                        message["To"] = receiver_email
                        message["Subject"] = "API DETECTED"

                        body = "SEARCH LOCATION"
                        message.attach(MIMEText(body, "plain"))

                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587

                        server = smtplib.SMTP(smtp_server, smtp_port)
                        server.starttls()

                        server.login(sender_email, sender_password)

                        server.sendmail(
                            sender_email, receiver_email, message.as_string())

                        server.quit()

                        st.success(f"Warning email sent to {receiver_email}!")

                        # Display the bounding box on the image
                        draw = ImageDraw.Draw(image)
                        bbox = box.xyxy[0].cpu().numpy()
                        draw.rectangle(
                            [(bbox[0], bbox[1]), (bbox[2], bbox[3])], outline="green", width=2)
                        st.image(image, caption='Object Detection Result',
                                 use_column_width=True)

    elif uploaded_file.type.startswith('video'):
        # Temporary file to store video frames
        temp_file = NamedTemporaryFile(delete=False)
        temp_file_path = temp_file.name

        # Save video file to temporary file
        temp_file.write(uploaded_file.read())

        # Display video
        st.video(temp_file_path)

        # Process video frames
        cap = cv2.VideoCapture(temp_file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run inference on the video frame
            results = model(frame)

            # Process results
            for result in results:
                if result:
                    for box in result.boxes:
                        cls = int(box.cls.item())
                        if cls == 0 and receiver_email:
                            # Alert email configuration
                            sender_email = "apialrm727@gmail.com"
                            sender_password = "nvlm ynph suqb xfwl"

                            message = MIMEMultipart()
                            message["From"] = sender_email
                            message["To"] = receiver_email
                            message["Subject"] = "API DETECTED"

                            body = "SEARCH LOCATION"
                            message.attach(MIMEText(body, "plain"))

                            smtp_server = "smtp.gmail.com"
                            smtp_port = 587

                            server = smtplib.SMTP(smtp_server, smtp_port)
                            server.starttls()

                            server.login(sender_email, sender_password)

                            server.sendmail(
                                sender_email, receiver_email, message.as_string())

                            server.quit()

                            st.success(
                                f"Warning email sent to {receiver_email}!")

                            # Display the bounding box on the video frame
                            bbox = box.xyxy[0].cpu().numpy()
                            frame_with_bbox = cv2.rectangle(frame.copy(), (int(bbox[0]), int(
                                bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
                            st.image(frame_with_bbox, channels="BGR",
                                     caption='Object Detection Result', use_column_width=True)

        # Release video capture and delete temporary file
        cap.release()
        cv2.destroyAllWindows()
        temp_file.close()
        st.success("Video processing completed.")
