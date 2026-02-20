import requests, os
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")
API_TOKEN = os.getenv("MY_APP_TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    if REMOVE_BG_API_KEY:
        return {"status": "success", "message": "Render environment variables are loaded!"}
    else:
        return {"status": "error", "message": "Keys not found. Check Render Environment tab."}

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