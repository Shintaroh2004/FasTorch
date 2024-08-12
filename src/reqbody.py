from pydantic import BaseModel

#受信するJSONの形
class Item(BaseModel):
    name:str