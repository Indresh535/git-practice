import cv2
import requests
import json

# Function to perform inference using Roboflow model
def infer_roboflow(image_path, api_key, model_endpoint):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        
    response = requests.post(
        model_endpoint,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/octet-stream'
        },
        data=image_data
    )
    return response.json()

# Path to your image file
image_path = './Azamara-3711.png'
api_key = 'z4dhEUk0Zbvo0z884oc3'  # Replace with your actual Roboflow API key
model_endpoint = './Azamara/train/_annotations.coco.json'  # Replace with your actual Roboflow model endpoint

# Perform inference using Roboflow model
result = infer_roboflow(image_path, api_key, model_endpoint)

# Read the image using OpenCV
image = cv2.imread(image_path)

# Process results and draw bounding boxes
for prediction in result['predictions']:
    x, y, w, h = prediction['x'], prediction['y'], prediction['width'], prediction['height']
    x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
    number = prediction['class']
    
    # Draw the rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Calculate the center coordinates
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    
    # Draw the center coordinates on the image
    coordinates_text = f"({center_x}, {center_y})"
    cv2.putText(image, coordinates_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    print(f"Number '{number}' found at coordinates (x1, y1, x2, y2): {x1}, {y1}, {x2}, {y2}")
    print(f"Center coordinates: {center_x}, {center_y}")

# Show the image with rectangles and coordinates
cv2.imshow('Image with Numbers Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
