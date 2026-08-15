import pytesseract
from PIL import Image
import numpy as np
import cv2

def extract_text_from_image(preprocessed_image: np.ndarray) -> str:
    """
    Extracts text from a preprocessed OpenCV image array using Tesseract OCR.
    """
    # Convert OpenCV image (numpy array) to PIL Image
    pil_img = Image.fromarray(preprocessed_image)
    
    # Run tesseract
    text = pytesseract.image_to_string(pil_img)
    
    return text.strip()
