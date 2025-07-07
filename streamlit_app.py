from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

app = FastAPI()

class Item(BaseModel):
    name: str
    value: int

@app.post("/process/")
def process_item(item: Item):
    return {"result": item.value * 2}
