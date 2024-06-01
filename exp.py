import cv2
import pytesseract
from PIL import Image
import numpy as np

def preprocess_image(image_path, scale):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding
    _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Resize the image based on the scale
    width = int(binary_image.shape[1] * scale)
    height = int(binary_image.shape[0] * scale)
    resized_image = cv2.resize(binary_image, (width, height), interpolation=cv2.INTER_AREA)
    
    return resized_image

def ocr_image(image):
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def main(image_path):
    scales = [0.5, 1, 1.5, 2]  # Different scales to test
    
    for scale in scales:
        preprocessed_image = preprocess_image(image_path, scale)
        text = ocr_image(preprocessed_image)
        cv2.imshow('Image with Four-Digit Numbers Detected', preprocessed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(f"Scale: {scale}x")
        print("OCR Result:")
        print(text)
        print("-" * 50)

if __name__ == "__main__":
    image_path = './ccl.png'
    main(image_path)
