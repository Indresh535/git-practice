import cv2
import pytesseract
import pandas as pd

# Load the image
image_path = './Azamara-3711.png'
image = cv2.imread(image_path)

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Detect text using Tesseract
detection = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

# Extract cabin numbers and coordinates
data = {'CabinNo': [], 'Category': [], 'Coordinates': []}
for i in range(len(detection['level'])):
    text = detection['text'][i]
    if text.isdigit():  # Assuming cabin numbers are digits
        x, y, w, h = detection['left'][i], detection['top'][i], detection['width'][i], detection['height'][i]
        data['CabinNo'].append(text)
        data['Coordinates'].append((x, y))
        # Category extraction logic (to be implemented based on the specific image layout)

# Convert data to DataFrame for better structuring
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('cabin_details.csv', index=False)

print(df)
