import glob
import os
import re
import sys
import cv2
from PIL import Image
import numpy as np
from yolov5.detect import run
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path


def pdf_to_images(pdf_file, img_size=640, stride=32, auto=True, transforms=None): # Function to convert from pdf to images
    """
    Converts PDFs in the given folder to images and returns a dataset-like output for each image
    similar to the `LoadImages` class structure.
   
    Args:
        input_folder (str): Path to the folder containing PDFs.
        img_size (int): Target image size.
        stride (int): Stride used for resizing.
        auto (bool): Whether to use automatic resizing.
        transforms (callable, optional): Optional transformations to apply to images.
   
    Yields:
        tuple: A tuple containing:
            - image_path (str): Path to the saved image.
            - im (np.ndarray): Processed image (e.g., resized).
            - im0 (np.ndarray): Original image.
            - cap (None): Placeholder for video capture (None for images).
            - s (str): Status string describing the processing.
    """

    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    try:
 
        POPPLER_PATH = r"C:\Users\arslan.za\source\repos\KlemmenApp\Csharp_TB27_RoboKlemmen\v5\.venv\poppler-24.07.0\Library\bin"  # Path to Poppler
        images = convert_from_path(pdf_file, poppler_path=POPPLER_PATH)
        for i, im0 in enumerate(images):
            im0 = np.array(im0)
            im0 = im0[:, :, ::-1].copy()
 
            image_name = f"{pdf_name}.jpg"
            print(f"Converting {pdf_file} - Page {i+1}/{len(images)}: {image_name}")
            # Save the image to a temporary location
            temp_dir = os.path.join(os.getcwd(), "temp_images")
            os.makedirs(temp_dir, exist_ok=True)
            image_path = os.path.join(temp_dir, image_name)
            
            # Convert the image to RGB format and save it
            cv2.imwrite(image_path, im0)
            im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)

            image_path = os.path.join(pdf_file, image_name)
 
            if transforms:
                im = transforms(im0)  
            else:
                im = letterbox(im0, img_size, stride=stride, auto=auto)[0]
                im = im.transpose((2, 0, 1))[::-1]
                im = np.ascontiguousarray(im)
 
            s = f"PDF {pdf_file} - Page {i+1}/{len(images)}: {image_name}"
            yield image_path, im, im0, None, s  
    except Exception as e:
        print(f"Failed to convert {pdf_file}: {e}")
 

def letterbox(im, new_shape=640, color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32): # To ensure the converted image is in same format as yolo model expects
    """Resizes an image while keeping its aspect ratio with padding."""
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
 
    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)
 
    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = new_shape
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]
 
    dw /= 2  # divide padding into 2 sides
    dh /= 2
 
    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)



def initial_yolo_detection(input_image):
    # imagesfromPDF = pdf_to_images(input_image)
    """Runs YOLOv5 model to detect and crop the main table from the image."""
    cropped_image, _, crop = run(
        weights="C:/Users/arslan.za/source/repos/KlemmenApp/Csharp_TB27_RoboKlemmen/v5/.venv/yolov5/runs/train/exp14/weights/best.pt",  # Trained YOLO model
        image=input_image,  # Input image
        save_crop=True,  # Return cropped table
        # conf_thres=0.5
    )
    return cropped_image

def cut_image_into_sub_parts(file_path, num_parts=7):
    # print("file_path: ", file_path)

    # Open the image
    img = file_path[0]

    # Get image dimensions
    width, height = img.size

    # Calculate the width of each part
    part_width = width // num_parts

    # List to store the cropped parts
    cropped_parts = []

    for i in range(num_parts):
        left = i * part_width
        right = (i + 1) * part_width if i < num_parts - 1 else width
        box = (left, 0, right, height)
        cropped_parts.append(img.crop(box))

    # for idx, cropped in enumerate(cropped_parts):
    #     cropped.save(f'cropped_part_{idx + 1}.jpg')

    return cropped_parts

def ocr_recognize_and_highlight(cropped_parts,original_image, missing_numbers):
    """Runs OCR on the cropped images and highlights the detected numbers."""
    
    
    numbers_to_highlight = missing_numbers  # Input the numbers to highlight
    string_list = [str(num) for num in numbers_to_highlight]  # Convert to string if not already
    numbers_regex = [rf'^{re.escape(num)}$' for num in string_list]  # Create exact match regex   
    
    # Initialize max_x_dict and max_x
    max_x_dict = {}  
    max_x = 0 
  
    directory = r"C:\Users\arslan.za\source\repos\KlemmenApp\Csharp_TB27_RoboKlemmen\temp_images" # Load the original image again
    image_files = glob.glob(os.path.join(directory, '*.jpg')) + glob.glob(os.path.join(directory, '*.png'))
    
    # Highlight matched numbers on the original image
    if image_files:
        original_image = cv2.imread(image_files[0])
    
    # Step 1: Store max_x values for each cropped image
    for idx, image_path in enumerate(cropped_parts):
        # image = cv2.imread(image_path)
        image = image_path
        image = np.array(image)  # Convert PIL image to numpy array
        max_x_dict[idx] = max_x
        max_x += image.shape[1]

    # Step 2: Detect and highlight exact numbers
    for idx, image_path in enumerate(cropped_parts):
        # image = cv2.imread(image_path)
        image = image_path
        image = np.array(image)  # Convert PIL image to numpy array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply sharpening filter
        kernel = np.array([[0, -0.25, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)
        
        # Apply thresholding
        _, thresholded_image = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR with Tesseract
        custom_config = r'--oem 3 --psm 6'
        ocr_data = pytesseract.image_to_data(thresholded_image, config=custom_config, output_type=Output.DICT)
        # print("OCR Output:", ocr_data['text'])

        numbers = []
        for i in range(len(ocr_data['text'])):
            text = ocr_data['text'][i].strip()
            
            
            # Check if text is a number and matches exactly
            if text.isdigit() and any(re.match(pattern, text) for pattern in numbers_regex):
                x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])

                # Get correct x-position using max_x_dict
                adjusted_x = x + max_x_dict[idx]

                numbers.append({'number': text, 'x': adjusted_x, 'y': y, 'width': w, 'height': h})

        # Print extracted numbers and their corrected positions
        for num in numbers:
            print(f"Image: {image_path}, Number: {num['number']}, Corrected Position: ({num['x']}, {num['y']}), Size: ({num['width']}x{num['height']})")
        
        # Draw bounding boxes around detected missing numbers
        for num in numbers:
            cv2.rectangle(original_image, (num['x']-8, num['y']+280), 
                        (num['x'] + num['width']+10, num['y'] + num['height']+1100), 
                        (0, 0, 254), 3)  # Red box for highlighting
        cv2.imwrite("wwwroot/images/highlighted_image_from_AI/missing_number_image.jpg",original_image)  # Save the highlighted image
    return "missing_number_image.jpg"  # Return the path of the highlighted image

def main(_input_pdf , missing_numbers):
    
    """Function to invoke the pdf_to_images logic as it would be in __main__ as well."""
    POPPLER_PATH = r"C:\Users\arslan.za\source\repos\KlemmenApp\Csharp_TB27_RoboKlemmen\v5\.venv\poppler-24.07.0\Library\bin"  # Path to Poppler
    
    print("Converting pdf to images...")
    pdf_file = _input_pdf
    images_from_pdf = pdf_to_images(pdf_file)
    
    #list_of_images = list(images)
    #print("converted_image: ",list_of_images)
    # print("images_example:  ", images)

    # Invoking the initial detection function to get the cropped images from YOLOv5
    print("Detetcting OneClassNumbers from image...")
    detect_Images = initial_yolo_detection(images_from_pdf)

    # print("detect_Images:  ", detect_Images)
    # cv2.imwrite("test.jpg", detect_Images)
    #print("images_example:  ", next(images))
    
    image = pdf_to_images(pdf_file)
    for idx, image in enumerate (image):
        original_image = image
        # print("original_image:  ", original_image)

    cropped_parts = cut_image_into_sub_parts(detect_Images)
    path = ocr_recognize_and_highlight(cropped_parts, original_image, missing_numbers)
    
    # print(cropped_parts)
    #print(list_of_images)

    # for i, cropped_image in enumerate(cropped_parts):
    #                 cropped_image_np = np.array(cropped_image)
    #                 cv2.imshow(f'Cropped Image 1 {i+1}', cropped_image_np)
    #                 cv2.waitKey(0)
    #                 cv2.destroyAllWindows()  
 
    return path


# if __name__ == "__main__": 
   
#     POPPLER_PATH = r"C:\Users\arslan.za\source\repos\KlemmenApp\Csharp_TB27_RoboKlemmen\v5\.venv\poppler-24.07.0\Library\bin"  # Path to Poppler
#     pdf_file = r"C:\Users\arslan.za\source\repos\KlemmenApp\Csharp_TB27_RoboKlemmen\v5\.venv\image25(Original).pdf"
#     # images = pdf_to_images(pdf_file)
# # # #     # images = convert_from_path(pdf_file, poppler_path=POPPLER_PATH)
# # # #     print(images)
#     main(pdf_file)