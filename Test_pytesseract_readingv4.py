from PIL import Image
import cv2
import os
import re
from pdf2image import convert_from_path
from wand.image import Image as WandImage
from PyPDF2 import PdfReader

from colorama import Fore, Back, Style
import os
import os.path
import numpy as np
import pandas as pd
import fitz  # PyMuPDF
import io
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageFilter
from xlsxwriter import workbook
import pandas as pd
from pandas import ExcelWriter
import openpyxl as xl
import glob
import os
import openpyxl
from openpyxl import load_workbook
import pytesseract
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\maxik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\maxik\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
def increase_resolution(input_path, output_path, scale_factor):
    with WandImage(filename=input_path) as img:
        # Set resolution
        img.resolution = (img.width * scale_factor, img.height * scale_factor)
        # Save the high-resolution image
        img.save(filename=output_path)
def sharpen_image(input_path, output_path, factor=2):
    # Open the image
    image = Image.open(input_path)

    # Apply the sharpen filter
    sharpened_image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=factor, threshold=1))

    # Save the sharpened image
    sharpened_image.save(output_path)
def crop_item(dir, Le_Up_Ri_Lo, root_dir, left=0, upper=0, right=2000, lower=1000):
    try:
        image = Image.open(dir)  # Replace with the path to your image
    except:
        print(dir+" erro failed to read")
        return 1
    # Define the coordinates of the rectangle you want to crop (left, upper, right, lower)
    list_filename = dir.split('.')
    filename=list_filename[0]+".png"
    #^ nuron network to identify cordinates of a data frame rectangle, 
    # Crop the image
    if((image.width == right-left and image.width == lower-upper) or "193387509182y0198y09812y5398012r098y2103891y9fd34" in filename):
        return filename
    cropped_image = image.crop((left, upper, right, lower))
    filename=list_filename[0]+"193387509182y0198y09812y5398012r098y2103891y9fd34"+".png"
    # Save the cropped image
    cropped_image.save(filename)
    return filename
def detect_horizontal_lines(img_array, threshold=0.95):
    # Calculate the sum of pixel values along each row
    row_sums = np.sum(img_array, axis=1)

    # Detect horizontal lines by finding rows with pixel sums exceeding the threshold
    horizontal_lines = np.where(row_sums >= threshold * img_array.shape[1])[0]
    
    return horizontal_lines

def smart_crop(image_path, output_path):
    # Open the image and convert it to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)

    # Detect and exclude horizontal lines
    horizontal_lines = detect_horizontal_lines(img_array)
    if len(horizontal_lines) > 0:
        # Exclude horizontal lines by adjusting the image array
        img_array = np.delete(img_array, horizontal_lines, axis=0)

    # Identify columns with text by summing up pixel values along each column
    column_sums = np.sum(img_array, axis=0)

    # Find the first and last columns with non-zero pixel sum (indicating text)
    first_column = np.argmax(column_sums > 0)
    last_column = len(column_sums) - np.argmax(np.flip(column_sums) > 0)

    # Find the first row with non-zero pixel sum
    first_row = 0
    try:
        while True:
            if(np.sum(img_array[first_row])==0):
                break
            first_row += 1
    except:
        pass
    # Find the last row with non-zero pixel sum
    last_row = img_array.shape[0] - 1
    try:
        while np.sum(img_array[last_row]) == 0:
            last_row -= 1
            if(last_row == -1):
                break
    except:
        pass
    # Crop the image using the identified boundaries
    #cropped_img = img.crop((first_column, 0, last_column, 100)) #first_row
    cropped_img = img.crop((first_row, first_column, -last_row, last_column))
    # Save the cropped image
    #cropped_img.save(output_path)
    
    return cropped_img


def pdf_to_image_array(pdf_path, output_image_path, page_number=0):
    output_filename = output_image_path.split(".")
    output_filename = output_filename[0] + "v6"+".png"
    print(output_filename)
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[page_number]
    zoom = 4    # zoom factor
    mat = fitz.Matrix(zoom, zoom)
    image = page.get_pixmap(matrix = mat)
    
    
    # Save the image to the specified path

    image.save(output_filename, "PNG")
    # Close the PDF document
    #pdf_document.close()
def margin_detect_verticle_lines(img_array):
    viritile_lines = []
    column_sums = np.sum(img_array, axis=0)
    for i in column_sums:
        if i == min(column_sums):
            viritile_lines.append(column_sums.index(i))
    return viritile_lines
def smart_crop_relative(image_path, output_path):
    list_filename = output_path.split('.')
    img= Image.open(image_path).convert('L')
    img_array = np.array(img)

    relative_verticle_lines = margin_detect_verticle_lines(img_array)
    if(len(relative_verticle_lines) > 0):
        for i in relative_verticle_lines:
            if(relative_verticle_lines.index(i)<=0):
                left = 0
            else:
                try:
                    left=relative_verticle_lines.index(i-1)
                except:
                    left = 0
            up = 50
            right = i
            bottom = 100
            cropped_image = img.crop((left, up, right, bottom))
            cropped_image.save(image_path)
            filename=list_filename[0]+i+".png"
            cropped_image.save(filename)
dir=r"C:\Users\maxik\Documents\GitHub\Nuron-text-recognition\WNB-PUCD6-DH-1432-jdg\WNB-PUCD6-DH-1229v6193387509182y0198y09812y5398012r098y2103891y9fd34.png"
cropped_images = smart_crop_relative(dir, dir)
print(cropped_images)
# if cropped_images:
#     for idx, cropped_img in enumerate(cropped_images):
#         cropped_img.show()
# else:
#     print("No valid cropped images.")


# sharpen_image(dir, dir, 2)
# print(dir)
# crop_item
# image = Image.open(dir)  # Replace with the path to your image
# custom_config = r'--oem 3 --psm 2'
# print("error")
# # Use pytesseract with custom configuration
# text_colums = pytesseract.image_to_string(image)
# print("error")
# custom_config = r'--psm 6'  # Horizontal text mode
# text_lines = pytesseract.image_to_string(image, config=custom_config)
# for i in text_lines:
#     if(i=="\n" and (text_lines[text_lines.index(i)-1]=="\n" or text_lines[text_lines.index(i)-1]==" ")):
#         text_lines[text_lines.index(i)]=""
# for i in text_colums:
#     if(i=="\n" and (text_colums[text_colums.index(i)-1]=="\n" or text_colums[text_colums.index(i)-1]==" ")):
#         text_colums[text_colums.index(i)]=""

#     #creats lists
# text_rows_inline = text_lines.split("\n")
# text_colums_nline = text_colums.split("\n")
# rows2, cols2 = (len(text_colums_nline)), (len(text_rows_inline))
# print(text_colums)
    

def PrecentageMatch(string1, string2):
    precetage_count = 0
    for i in range(len(string1)):
        #print(string1)
        #print(string2)
        try:
            if(string1[i] == string2[i]):
                precetage_count=+1
        except:
            precetage_count= precetage_count

    if(precetage_count!=0):
        return precetage_count/len(string1)*100
    return 0
def Compare(string1, string2):
    '''
    Compares two lists in a loop. Once the lists do not
    match retures charater of lists that do not match.
    '''

    for i in range(len(string1)):
        try:
            if(string1[i] != string2[i]):
                return string1
        except:
            pass
    return "error"
def match_join(string1, string2):
    #print(string1)
    #print(string2)
    try:
        string1_list = string1.split()
    except:
        print(" ")
        #print("except_string1")
    try:
        string2_list = string2.split()
    except:
        #print("excelption_string2")
        print(" ")
    bitmap_append = []
    output_string = " "
    for i in range(len(string1_list)):
        try:
            if(string1_list[i] == string2_list[i]):
                bitmap_append.append(1)
            else:
                bitmap_append.append(0)
        except:
            bitmap_append.append(0)
    for j in range(len(bitmap_append)):
        try:
            if(bitmap_append[j]==1):
                output_string = output_string+string2_list[j]
        except:
            pass
    return output_string
def create_scv(dir, filename_out, data_list):
    #data frame
    filename_outC = dir+filename_out+".cvs"
    filename_outX = dir+filename_out+".xlsx"
    df = pd.DataFrame(data_list)
    print(filename_outX)
    display(df)
    df.to_excel(filename_outX)
    #df.to_csv(filename_outC)
def pytesseractRead(dir, output_dir, sizeofDataframeROWSCOLS):
    sharpen_image(dir, dir, 2)
    print(dir)
    image = Image.open(dir)  # Replace with the path to your image
    custom_config = r'--oem 3 --psm 14'

# Use pytesseract with custom configuration
    text_colums = pytesseract.image_to_string(image, config=custom_config)
    custom_config = r'--psm 6'  # Horizontal text mode
    text_lines = pytesseract.image_to_string(image, config=custom_config)
    for i in text_lines:
        if(i=="\n" and (text_lines[text_lines.index(i)-1]=="\n" or text_lines[text_lines.index(i)-1]==" ")):
            text_lines[text_lines.index(i)]=""
    for i in text_colums:
        if(i=="\n" and (text_colums[text_colums.index(i)-1]=="\n" or text_colums[text_colums.index(i)-1]==" ")):
            text_colums[text_colums.index(i)]=""

    #creats lists
    text_rows_inline = text_lines.split("\n")
    text_colums_nline = text_colums.split("\n")
    rows, cols = sizeofDataframeROWSCOLS
    rows2, cols2 = (len(text_colums_nline)), (len(text_rows_inline))
    print(text_colums)
    datalistdf = [[[]]*(rows+rows2)]*(cols+cols2)
    for elementSTR in text_colums_nline:
        for linestr in text_rows_inline:
            for i in linestr:
                if(elementSTR not in linestr):
                    break
                try:
                    if(elementSTR[0]==i):
                        pass
                except:
                    break
                if(elementSTR[0]==i):
                    #print(elementSTR)
                    if(Compare(linestr, elementSTR)!=int and Compare(linestr, elementSTR) != "error"):
                        try:
                            buffer = Compare(linestr, elementSTR)
                            if(PrecentageMatch(buffer, elementSTR)>=0.00):
                                print(PrecentageMatch(buffer, elementSTR)+elementSTR)
                                if(text_colums_nline.index(elementSTR) > cols):
                                    #print("element"+text_rows_inline.index(linestr)+","+text_colums.index(elementSTR))
                                    #datalistdf[text_rows_inline.index(linestr)].append(elementSTR)
                                    if(text_colums_nline.index(elementSTR) > cols):
                                        try:
                                            datalistdf[text_colums_nline.index(elementSTR)]
                                        except:
                                            pass
                                            #pytesseractRead(dir, output_dir, (1, text_colums_nline.index(elementSTR)))
                                elif(text_colums_nline.index(elementSTR) != 0 or text_colums_nline.index(elementSTR) < cols):
                                    #print("element"+(text_rows_inline.index(linestr),text_colums.index(elementSTR)))
                                    datalistdf[text_rows_inline.index(linestr)][text_colums.index(elementSTR)]=(elementSTR)
                            else:
                                #print("error:::"+PrecentageMatch(buffer, elementSTR))
                                pass
                            break
                        except:
                            pass
                            #print("error in match sector")
    #iterates through lists, # -> | & -->  r, w, 
    #print(datalistdf)
    # for i in text_rows_inline:
    #     for j in text_colums_nline:
    #         for k in j:
    #             try:
    #                 if(PrecentageMatch(j,i) !=0):
    #                     print(j)
    #                     #print("match::"+match_join(j,i))
    #                     datalistdf[text_colums_nline.index(j)][text_rows_inline.index(i)]=match_join(i,j)
    #             except:
    #                 print("except")
    #                 pass
    text_rows_inline
    #print(datalistdf)
    filename = output_dir.split("\\")
    try:
        create_scv(dir, filename[-1], datalistdf)
    except:
        create_scv(dir, filename[0], datalistdf)
    return 0


def itr_dir(dir, extension, jdg_dir=r"C:\Users\maxik\Documents\Github\Nuron-text-recognition\WNB-PUCD6-DH-1432-jdg"):  # Replace with your desired file extension
    # List all files in the directory

    # Filter files by the specified extension
    # Print the filtered file list
    try:
        file_list = os.listdir(jdg_dir)
        filtered_files = [file for file in file_list if file.endswith(".png")]
    except:
        file_list = []
        filtered_files = []
    if(len(file_list) != 0 and len(filtered_files)!=0):
        file_list = os.listdir(jdg_dir)
        filtered_files = [file for file in file_list if file.endswith(".png")]
        if(len(filtered_files) == 0):
            return 1
        print("hello!")
        for file in filtered_files:
            dir_fle = ""
            print("hello")
            dir_file = jdg_dir+'\\'+file
            list_filenames = file.split('.')
            print('extrancting')
            output_dir = crop_item(dir_file, 0, jdg_dir)
            if(output_dir != 1):
                print("crop")
                print(output_dir)
                pytesseractRead(output_dir, dir, (0,0))
        return 3
    else:
        file_list = os.listdir(dir)
        filtered_files = [file for file in file_list if file.endswith(extension)]
        os.makedirs(jdg_dir, exist_ok=True)
        for file in filtered_files:
            dir_file = ""
            dir_file = dir+'\\'+file
            list_filenames = file.split('.')
            dir_filejpg = ""
            dir_filejpg = jdg_dir+'\\'+file
            if(list_filenames[-1] == "pdf"):
                    #pdf_to_jpg(dir_file, dir)
                    #extract_text_from_column(dir_file, 0)
                pdf_to_image_array(dir_file, dir_filejpg)
                #print(dir_file)
        return 2
input_dir=r"C:\Users\maxik\Documents\GitHub\Nuron-text-recognition\WNB-PUCD6-DH-1432"
jdg_dir = r"C:\Users\maxik\Documents\Github\Nuron-text-recognition\WNB-PUCD6-DH-1432-jdg"
if(itr_dir(input_dir, ".pdf") == 2):
    itr_dir(input_dir, ".pdf")

