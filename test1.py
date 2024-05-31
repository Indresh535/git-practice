import pytesseract
from PIL import Image
import numpy as np

def extract_vertical_text(image_path):
    # Load the image
    img = Image.open(image_path)
    
    # Convert the image to grayscale
    gray = img.convert('L')
    
    # Apply OCR to extract text
    data = pytesseract.image_to_data(gray, config='--psm 5', output_type=pytesseract.Output.DICT)
    
    # Extracting vertical text
    vertical_text = []
    n_boxes = len(data['level'])
    
    for i in range(n_boxes):
        # if int(data['width'][i]) <= 250:  # Assuming numbers are aligned vertically within a narrow width
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        vertical_text.append(data['text'][i])
    
    # Clean and join the vertical text
    cleaned_text = [text for text in vertical_text if text.strip() != '']
    final_text = '\n'.join(cleaned_text)
    
    return final_text

# Example usage
image_path = './Azamara-3711.png'
cabin_numbers = extract_vertical_text(image_path)
print("Extracted Cabin Numbers:")
print(cabin_numbers)
