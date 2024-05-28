import cv2
import pytesseract

def extract_cabin_numbers(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Pre-process the image (convert to grayscale and threshold)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Extract text using Tesseract OCR
    extracted_text = pytesseract.image_to_string(threshold_image)

    # Parse the extracted text to get cabin numbers
    cabin_numbers = [int(num) for num in extracted_text.split() if num.isdigit()]

    return cabin_numbers

def calculate_coordinates(cabin_numbers):
    num_cabins = len(cabin_numbers)
    x_coordinates = [i / num_cabins for i in range(num_cabins)]
    y_coordinate = 0.5  # Assuming all cabins are at the same y-coordinate

    return [(cabin, (x, y_coordinate)) for cabin, x in zip(cabin_numbers, x_coordinates)]

if __name__ == "__main__":
    image_path = './Azamara-3711.png'  # Replace with your actual image path
    cabins = extract_cabin_numbers(image_path)
    coordinates = calculate_coordinates(cabins)

    print("Cabin Numbers and Coordinates:")
    for cabin, (x, y) in coordinates:
        print(f"Cabin {cabin}: ({x:.2f}, {y:.2f})")