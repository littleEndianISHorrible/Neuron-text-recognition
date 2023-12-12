import cv2
import numpy as np
import matplotlib.pyplot as plt
import time 
from io import BytesIO
from PIL import Image
# Open the default camera (camera index 0)
cap = cv2.VideoCapture(0)
# Check if the camera opened successfully
def convert_to_vector(input_image, output_svg_path):
    # Open the bitmap image using OpenCV
    bitmap_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(bitmap_image, cv2.CV_64F)
    sharpened_image = laplacian+bitmap_image
    bitmap_image = sharpened_image
    # Apply thresholding to create a binary image
    _, binary_image = cv2.threshold(bitmap_image, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank canvas
    vector_image = np.ones_like(bitmap_image) * 255 

    # Draw contours on the blank canvas
    cv2.drawContours(vector_image, contours, -1, (0, 0, 0), 2)

    # Save the vector-like image
    cv2.imshow("vectro", vector_image)
    return vector_image

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
frame_counter = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    numpy_frame = np.array(frame)
    npy_filename = f'C:\\Users\\maxik\\Documents\\GitHub\\Neuron-text-recognition\\FAce_frames\\output-camera-toVector{frame_counter}.jpg'
    # Save the array as a .npy file
    np.save(npy_filename, convert_to_vector(frame, npy_filename))
    # Increment frame counter
    frame_counter += 1
    cv2.imshow('Camera Feed', frame)
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera when done
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()