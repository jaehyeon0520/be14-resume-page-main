import uvicorn
from app import app  # 위에서 만든 FastAPI app 불러오기

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
