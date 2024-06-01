# import cv2
# import pytesseract

# # Path to your image file
# image_path = './ccl.png'

# # Read the image using OpenCV
# image = cv2.imread(image_path)

# # Convert the image to grayscale
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Apply thresholding or other preprocessing techniques if necessary
# # For simplicity, we'll apply a binary threshold
# _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

# # Use pytesseract to do OCR on the image
# custom_config = r'--oem 3 --psm 6 outputbase digits'
# text = pytesseract.image_to_string(binary_image, config=custom_config)

# # Print the extracted text
# print("Extracted Text:", text)

# # Get the coordinates of the detected numbers
# boxes = pytesseract.image_to_boxes(binary_image, config=custom_config)

# # Initialize a list to store detected four-digit numbers and their coordinates
# four_digit_numbers = []

# # Iterate over the boxes to extract coordinates and digits
# for b in boxes.splitlines():
#     b = b.split()
#     x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     digit = b[0]
#     # Store the bounding box and digit
#     four_digit_numbers.append((digit, x, y, w, h))

# # Group digits into four-digit numbers
# i = 0
# while i <= len(four_digit_numbers) - 4:
#     group = four_digit_numbers[i:i+4]
#     # Check if we have a valid four-digit number
#     if all(len(d[0]) == 1 and d[0].isdigit() for d in group):
#         x1, y1 = group[0][1], group[0][2]
#         x2, y2 = group[3][3], group[3][4]
#         four_digit_number = ''.join(d[0] for d in group)
#         # Draw the rectangle
#         cv2.rectangle(image, (x1, image.shape[0] - y1), (x2, image.shape[0] - y2), (0, 255, 0), 2)
#         # Calculate the center coordinates
#         center_x = (x1 + x2) // 2
#         center_y = image.shape[0] - (y1 + y2) // 2
#         # Draw the center coordinates on the image
#         coordinates_text = f"({center_x}, {center_y})"
#         cv2.putText(image, coordinates_text, (x1, image.shape[0] - y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
#         print(f"Four-digit number '{four_digit_number}' found at coordinates (x1, y1, x2, y2): {x1}, {y1}, {x2}, {y2}")
#         print(f"Center coordinates: {center_x}, {center_y}")
#         i += 4  # Move to the next potential group
#     else:
#         i += 1  # Move to the next digit

# # Show the image with rectangles and coordinates
# cv2.imshow('Image with Four-Digit Numbers Detected', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# looping image 

import cv2
import pytesseract

# Path to your image file
image_path = './msc.png'

# Read the image using OpenCV
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding or other preprocessing techniques if necessary
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

# Define rectangle size
rect_width = 43
rect_height = 30

# Get image dimensions
image_height, image_width = binary_image.shape

# Iterate over the image using predefined rectangle size
for y in range(0, image_height, rect_height):
    for x in range(0, image_width, rect_width):
        # Define the region of interest (ROI)
        roi = binary_image[y:y+rect_height, x:x+rect_width]
        
        # Use pytesseract to do OCR on the ROI
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(roi, config=custom_config)

        # Remove any non-digit characters
        text = ''.join(filter(str.isdigit, text))

        # Check if the text is a valid four-digit number
        if len(text) == 4:
            # Draw the rectangle
            cv2.rectangle(image, (x, y), (x + rect_width, y + rect_height), (0, 255, 0), 2)
            
            # Calculate the center coordinates
            center_x = x + rect_width // 2
            center_y = y + rect_height // 2
            
            # Draw the center coordinates on the image
            coordinates_text = f"({center_x}, {center_y})"
            cv2.putText(image, coordinates_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            print(f"Four-digit number '{text}' found at coordinates (x, y, w, h): {x}, {y}, {x + rect_width}, {y + rect_height}")
            print(f"Center coordinates: {center_x}, {center_y}")

# Show the image with rectangles and coordinates
cv2.imshow('Image with Four-Digit Numbers Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
