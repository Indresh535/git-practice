import cv2
import pytesseract
import numpy as np

# Set the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define color categories (as BGR in OpenCV)
categories = {
    "#7EB3C8": "SP Suite",
    "#A2ACCE": "CW Suite",
    "#CCD1E5": "CO Suite",
    "#B8E3E6": "N1 Suite",
    "#DAEFF2": "N2 Suite",
    "#FFFFFF": "W",
    "#F68933": "P1 Balcony",
    "#DFC3C3": "P2 Balcony",
    "#C6979A": "P3 Balcony",
    "#FED5B3": "V1 Balcony",
    "#D0A893": "V2 Balcony",
    "#EDDCD1": "V3 Balcony",
    "#9DA768": "04 OceanView",
    "#FFDD97": "05 OceanView",
    "#CBDBD5": "10 Inside"
}

def extract_cabin_numbers_and_coords(image_path):
    # Load the image file
    image = cv2.imread(image_path)
    original_image = image.copy()

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Extract text using Tesseract OCR
    extracted_text = pytesseract.image_to_data(threshold_image, output_type=pytesseract.Output.DICT)

    cabin_data = []

    n_boxes = len(extracted_text['text'])
    for i in range(n_boxes):
        if int(extracted_text['conf'][i]) > 60:  # Confidence level > 60
            (x, y, w, h) = (extracted_text['left'][i], extracted_text['top'][i], extracted_text['width'][i], extracted_text['height'][i])
            text = extracted_text['text'][i]
            if text.isdigit():  # Assuming cabin numbers are purely numeric
                cabin_number = int(text)
                category, cabin_type_exception = categorize_cabin(image[y:y+h, x:x+w])
                cabin_data.append({
                    'CabinNo': cabin_number,
                    'Category': category,
                    'Cabin Type Exception': cabin_type_exception,
                    'Coordinates': (x, y)
                })
    
    return cabin_data

def categorize_cabin(cabin_image):
    # Resize cabin image to a single pixel to get the average color
    avg_color = cv2.resize(cabin_image, (1, 1)).flatten()
    avg_color_hex = '#{:02x}{:02x}{:02x}'.format(avg_color[2], avg_color[1], avg_color[0]).upper()
    
    category = categories.get(avg_color_hex, "Unknown")
    cabin_type_exception = "None"  # Placeholder, replace with actual logic if needed
    
    return category, cabin_type_exception

if __name__ == "__main__":
    image_path = './Azamara-3711.png'  # Replace with your actual image path
    cabin_data = extract_cabin_numbers_and_coords(image_path)

    print("Cabin Numbers and Coordinates:")
    for data in cabin_data:
        print(f"CabinNo: {data['CabinNo']}, Category: {data['Category']}, Cabin Type Exception: {data['Cabin Type Exception']}, Coordinates: {data['Coordinates']}")
