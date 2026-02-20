import requests, os
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# This pulls the key from Render's settings
REMOVE_BG_API_KEY = os.getenv("bg-remover")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TOKEN = os.getenv("V14Srv7wBExGeEUFBzdCSTEf")

@app.get("/")
async def root():
    if API_TOKEN:
        return {"status": "success", "message": "Token is loaded from Render!"}
    else:
        return {"status": "error", "message": "Token not found in environment variables"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not REMOVE_BG_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured on server")

    input_data = await file.read()

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': input_data},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    )

    if response.status_code == requests.codes.ok:
        return StreamingResponse(BytesIO(response.content), media_type="image/png")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)