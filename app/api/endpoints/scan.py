from fastapi import APIRouter, File, UploadFile
import base64
from app.core.config import settings
import json
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@router.post("")
async def scan_receipt(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
Kamu adalah sistem yang menerima gambar struk dan mengubahnya menjadi JSON. 
Hanya keluarkan JSON valid tanpa teks tambahan. 
Pastikan semua nilai angka berupa integer tanpa titik ribuan, dan field sesuai struktur ini:

{
  "store": {
    "name": "",
    "phone": ""
  },
  "receipt": {
    "number": "",
    "cashier": "",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS"
  },
  "items": [
    {
      "name": "",
      "quantity": 0,
      "unit_price": 0,
      "total_price": 0,
      "discount": 0
    }
  ],
  "summary": {
    "total_items": 0,
    "subtotal": 0,
    "ppn": 0,
    "service": 0,
    "total_discount": 0,
    "delivery_price": 0,
    "total": 0
  },
  "feedback": {
    "phone": "",
    "code": ""
  }
}

Baca teks pada gambar struk ini lalu keluarkan hasilnya dalam format JSON sesuai struktur yang sudah ditentukan.
Jangan sertakan teks atau penjelasan lain, hanya JSON valid.
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",  
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
    )

    # Ambil konten, parse ke dict
    content_str = response.choices[0].message.content
    try:
        json_data = json.loads(content_str)
    except json.JSONDecodeError:
        raise ValueError("Model tidak mengembalikan JSON valid")

    return json_data
