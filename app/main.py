from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {"text": "Hello, world"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
  return {"id": item_id, "q": q}