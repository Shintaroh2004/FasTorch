import io
from click import File
import uvicorn
from fastapi import FastAPI,HTTPException, UploadFile,File
from fastapi.staticfiles import StaticFiles
import logging
from PIL import Image

from reqbody import Item
from state import UserState

logger=logging.getLogger(__name__)

app=FastAPI()

app.state.__USER_STATE__= UserState()

@app.get("/test")
async def hello():
    return "こんちわ"

#POSTによるデータ送信
@app.post("/test")
async def hello_post(body:Item):
    return f"hello {body.name} !! nice to meets you !!"

#パスパラメータによるデータ送信
@app.get("/test/{name}")
async def hello_path_param(name:str):
    return  f"hello {name} !! nice to meets you !!"

#指定されたラベルの犬種を送信
@app.get("/dog/{label}")
async def find_dog(label:str):
    try:
        return app.state.__USER_STATE__.get_dog(label)
    except:
        raise HTTPException("指定されたラベルの犬種が存在しません．")
    
#画像の受け取り
@app.post("/dog")
async def predict_dog(file:UploadFile=File(...)):
    img = await file.read()
    img=io.BytesIO(img)
    img=Image.open(img)
    return f"{type(img)}"

#静的ファイル
app.mount("/",StaticFiles(directory="static",html=True),name="static")

#コード上でuvicornの起動
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)