from fastapi import FastAPI

app = FastAPI(title="QuantumTask API")

@app.get("/")
def read_root():
    return {"message": "QuantumTask API Operational"}
