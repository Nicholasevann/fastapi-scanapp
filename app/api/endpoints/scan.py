from fastapi import APIRouter, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
import re
from PIL import ImageEnhance
import cv2
import numpy as np

router = APIRouter()
def parse_receipt(items):
    parsed = {
        "store_name": None,
        "address": None,
        "date": None,
        "total": None,
        "tax": None,
        "products": []
    }

    # Join text for easier regex
    full_text = "\n".join(items)

    # --- Store name (first line) ---
    parsed["store_name"] = items[0] if items else None

    # --- Address (lines until we find something like "Total" or date) ---
    for i in range(1, len(items)):
        if re.search(r'total|tunai|tgl|date', items[i], re.IGNORECASE):
            parsed["address"] = " ".join(items[1:i])
            break

    # --- Date ---
    date_match = re.search(r'(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})', full_text)
    if date_match:
        parsed["date"] = date_match.group(1)

    # --- Total ---
    total_match = re.search(r'(total|tunai)\D+([\d.,]+)', full_text, re.IGNORECASE)
    if total_match:
        parsed["total"] = total_match.group(2).replace(",", "")

    # --- Tax (PPN) ---
    tax_match = re.search(r'ppn\D+([\d.,]+)', full_text, re.IGNORECASE)
    if tax_match:
        parsed["tax"] = tax_match.group(1).replace(",", "")

    # --- Products ---
    for line in items:
        # Skip headers and totals
        if re.search(r'total|tunai|ppn|tgl|date', line, re.IGNORECASE):
            continue
        # Find pattern: name + price
        m = re.search(r'(.+?)\s+([\d.,]+)$', line)
        if m:
            name = m.group(1).strip()
            price = m.group(2).replace(",", "")
            parsed["products"].append({"name": name, "price": price})

    return parsed
def preprocess_image(image_bytes):
    # Load image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Remove noise
    gray = cv2.medianBlur(gray, 3)

    # Threshold (make black/white)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Optional: Resize to improve OCR accuracy
    scale_percent = 200  # double size
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    thresh = cv2.resize(thresh, (width, height), interpolation=cv2.INTER_LINEAR)

    return thresh
@router.post("")
async def scan_receipt(file: UploadFile = File(...)):
   # Read bytes
    image_bytes = await file.read()

    # Preprocess for better OCR
    processed_img = preprocess_image(image_bytes)

    # Convert processed image (numpy) to PIL for Tesseract
    processed_pil = Image.fromarray(processed_img)

    # OCR with better config
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_pil, config=custom_config)

    # Clean lines (remove empty + strip spaces)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Parse into structured data
    parsed_data = parse_receipt(lines)
    return {"text": text, "items": parsed_data, "parsed": parsed_data}

