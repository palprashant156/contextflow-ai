import cv2
import numpy as np

def preprocess_image_for_ocr(image_bytes: bytes) -> np.ndarray:
    """
    Takes raw image bytes, decodes, and applies OpenCV transformations
    to improve OCR accuracy (grayscale, denoise, thresholding).
    """
    # 1. Decode image bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image bytes")

    # 2. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3. Apply Gaussian blur to denoise
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    
    # 4. Apply adaptive thresholding to binarize image (make text black, background white)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Optional: deskewing could be added here if needed
    
    return thresh
