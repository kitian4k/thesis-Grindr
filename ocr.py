import easyocr
import cv2

# Load the input image (replace 'input_image.jpg' with your actual image file)
image_path = 'input\doc2\page_1.png'
image = cv2.imread(image_path)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the language(s) you want to support (e.g., English)
reader.detector = reader.initDetector('craft_mlt_25k\craft_mlt_25k.pth')
# Perform OCR on the image
result = reader.readtext(image, detail=0)  # Extract only recognized texts

# Print the extracted text
for text in result:
    print(text)
