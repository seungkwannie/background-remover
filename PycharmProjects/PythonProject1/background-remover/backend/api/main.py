from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse  # <--- Add this import
from rembg import remove
from PIL import Image
import io


app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # 1. Read and open the image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # 2. Process the image
    output = remove(image)

    # 3. Save to a byte buffer
    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    # 4. Return as a proper Image Stream
    return StreamingResponse(buffer, media_type="image/png")