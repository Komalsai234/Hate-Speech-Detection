from hate_speech.pipeline.prediction import PredictionPipeline
from fastapi import FastAPI
import uvicorn
import os
from fastapi.responses import Response, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

executor = ThreadPoolExecutor(max_workers=1)

obj = None
pipeline_initialized = False

def initialize_pipeline():
    global obj, pipeline_initialized
    obj = PredictionPipeline()
    pipeline_initialized = True

@app.on_event("startup")
async def startup_event():
    executor.submit(initialize_pipeline)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    global pipeline_initialized
    try:
        pipeline_initialized = False 
        os.system("python main.py")
        initialize_pipeline() 
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict")
async def predict_route(text: str):
    if not pipeline_initialized:
        return JSONResponse(content={"warning": "Please wait until the pipeline is fully initialized."}, status_code=503)
    try:
        prediction = obj.predict(text)
        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    APP_HOST = "0.0.0.0"
    APP_PORT = 8080
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
