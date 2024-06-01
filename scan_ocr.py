import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import pytesseract
import cv2
import numpy as np

# Initialize the OCR engine
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Image Selector")
        
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        
        self.image = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.crop_rectangle = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Exit", command=root.quit)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.crop_rectangle = (self.start_x, self.start_y, end_x, end_y)
        self.scan_image()

    def scan_image(self):
        if self.crop_rectangle:
            x1, y1, x2, y2 = self.crop_rectangle
            cropped_image = self.image.crop((x1, y1, x2, y2))
            cropped_image_np = np.array(cropped_image)
            gray_image = cv2.cvtColor(cropped_image_np, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

            custom_config = r'--oem 3 --psm 6 outputbase digits'
            text = pytesseract.image_to_string(binary_image, config=custom_config)
            print("Extracted Text:", text)

            boxes = pytesseract.image_to_boxes(binary_image, config=custom_config)

            draw = ImageDraw.Draw(cropped_image)

            for b in boxes.splitlines():
                b = b.split()
                x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                digit = b[0]
                draw.rectangle([x, cropped_image.size[1] - y, w, cropped_image.size[1] - h], outline="green")
                center_x = (x + w) // 2
                center_y = cropped_image.size[1] - (y + h) // 2
                draw.text((x, cropped_image.size[1] - y), f"({center_x}, {center_y})", fill="blue")
                print(f"Digit '{digit}' found at coordinates (x, y, w, h): {x}, {y}, {w}, {h}")
                print(f"Center coordinates: {center_x}, {center_y}")

            cropped_photo = ImageTk.PhotoImage(cropped_image)
            self.canvas.create_image(x1, y1, anchor=tk.NW, image=cropped_photo)
            self.canvas.image = cropped_photo

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
