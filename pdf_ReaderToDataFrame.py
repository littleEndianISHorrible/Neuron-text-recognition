import pytesseract
from PIL import Image
import cv2
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\maxik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import re
from pdf2image import convert_from_path

# image = Image.open('path_to_image.png')  # Replace with the path to your image
# text = pytesseract.image_to_string(image)
# print(text)

def extract_text_from_column(image_path, output_path, threshold=150):
    # Open the image
    image = cv2.imread(image_path, 0)  # Read the image in grayscale

    # Apply thresholding to create a binary image
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by x-coordinate (left to right)
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Extract text from each column
    for i, contour in enumerate(contours):
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the image to the bounding box
        column_image = image[y:y+h, x:x+w]

        # Extract text from the cropped column
        column_text = pytesseract.image_to_string(column_image)

        # Save the cropped column image (optional)
        cv2.imwrite(f"{output_path}/column_{i + 1}.png", column_image)

        # Print or use the extracted text as needed
        print(f"Text from Column {i + 1}:\n{column_text}\n{'-'*30}")
def extract_columns_with_flags(image_path, flag_column_index):
    # Open the image using PIL
    image = Image.open(image_path)

    # Use Tesseract to perform OCR on the image
    text = pytesseract.image_to_string(image)

    # Split the text into lines
    lines = text.splitlines()

    # Extract information based on flags
    extracted_data = []
    for line in lines:
        # Split the line into columns
        columns = line.split()

        # Check if the line has enough columns and if the flag is present
        if len(columns) > flag_column_index and columns[flag_column_index] == 'FLAG':
            # Extract information based on your requirements
            extracted_data.append({
                'Column1': columns[0],
                'Column2': columns[1],
                # Add more columns as needed
            })

    return extracted_data
# Create the output directory if it doesn't exist
def pdf_to_jpg(pdf_path, output_folder):
    images = convert_from_path(pdf_path, output_folder=output_folder, fmt="jpeg")
    
    for i, image in enumerate(images):
        image.save(f"{output_folder}/page_{i + 1}.jpg", "JPEG")
def pytesseractRead(dir):
    filename = dir.split("\\")
    print(dir)
    image = Image.open(filename[-1])  # Replace with the path to your image
    text_colums = pytesseract.image_to_string(image)
    text_colums_inline = ""
    for i in text_colums:
        if(i == '\n'):
            text_colums_inline=text_colums_inline+','
        else:
            text_colums_inline=text_colums_inline+i
    custom_config = r'--psm 6'  # Horizontal text mode
    text_lines = pytesseract.image_to_string(image, config=custom_config)
    #text processing begins here
    #text_colums_inline
    

    print(text_lines)
    return text_colums
def crop_item(dir, Le_Up_Ri_Lo, root_dir):
    try:
        image = Image.open(dir)  # Replace with the path to your image
    except:
        print(dir+" erro failed to read")
        return 1
    # Define the coordinates of the rectangle you want to crop (left, upper, right, lower)
    left = 0
    upper = 100
    right = 3700
    lower = 4900
    #^ nuron network to identify cordinates of a data frame rectangle, 
    # Crop the image
    cropped_image = image.crop((left, upper, right, lower))

    # Save the cropped image
    list_filename = dir.split('.')
    filename=list_filename[0]+".png"
    cropped_image.save(filename)
    return filename
def itr_dir(dir, extension):  # Replace with your desired file extension

    # List all files in the directory
    file_list = os.listdir(dir)

    # Filter files by the specified extension
    filtered_files = [file for file in file_list if file.endswith(extension)]

    # Print the filtered file list
    for file in filtered_files:
        dir_file = ""
        dir_file = dir+'\\'+file
        list_filenames = file.split('.')
        if(list_filenames[1] == 'pdf'):
            #pdf_to_jpg(dir_file, dir)
            #extract_text_from_column(dir_file, 0)
            pdf_to_jpg(dir_file, dir)
        elif(list_filenames[1] == 'jpg'):
            extract_text_from_column(dir_file, 0)
        output_dir = crop_item(dir_file, 0, dir)
        if(output_dir != 1):
            text_output = pytesseractRead(output_dir)
        #print(dir_file)
itr_dir(r"C:\Users\maxik\Documents\GitHub\Neuron-text-recognition\WNB-PUCD6-DH-1432", ".pdf")