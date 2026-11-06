from fastapi import FastAPI

app = FastAPI(title="Income Statement")


@app.get("/")
def hello_world():
    return {"message": "Hello World"}
