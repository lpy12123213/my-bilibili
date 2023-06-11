from fastapi import FastAPI
import requests
from module import func
app = FastAPI()

@app.get("/video/place/{items}")
async def read_items(items: str):
    try:
        return {"video": func.get_video_info(items, func.header)}
    except:
        return {"video": "error"}

@app.get("/video/cid/{items}")
async def read_cid(items: str):
    try:
        return {"video": func.get_cid(items, func.header)}
    except:
        return {"video": "error"}