import cv2
import pytesseract

def process_image(image_path):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding the image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Save the preprocessed image for OCR
    preprocessed_image_path = 'C:/Users/Dell/Downloads/Azamara-3711-pp.png'
    cv2.imwrite(preprocessed_image_path, thresh)

    # Perform OCR using Tesseract
    result = pytesseract.image_to_string(preprocessed_image_path)

    return result

# Example usage
if __name__ == '__main__':
    image_path = './Azamara-3711.png'  # Replace with your image path
    result = process_image(image_path)
    print(result)
