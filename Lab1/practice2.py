from fastapi import FastAPI
import uvicorn

asenel = FastAPI()

if __name__ == "__main__":
    uvicorn.run("practice2:asenel", host="127.0.0.1", port=8080, reload=True)