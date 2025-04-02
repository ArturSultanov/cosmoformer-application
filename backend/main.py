from fastapi import FastAPI, UploadFile, HTTPException
from PIL import Image
from contextlib import asynccontextmanager
from model import Cosmoformer
from config import settings
from logger import logger
from schemas.inference import InferenceResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
import io

cosmoformer: Cosmoformer

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info('Loading the Cosmoformer model')
        global cosmoformer
        cosmoformer = Cosmoformer(model_path=settings.MODEL_PATH)
        yield
    except Exception as e:
        logger.error("Error has occurred: ",e)
    finally:
        logger.info('Shutting down the app...')

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {f"Hello World!"}

@app.get("/modelname")
async def model():
    return {f"Model: {cosmoformer.get_name()}"}

@app.post("/inference", response_model=InferenceResponse)
async def inference(file: UploadFile):

    if file.content_type not in settings.ACCEPTED_MIME_TYPES:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Supported types: {settings.ACCEPTED_MIME_TYPES}"
        )

    file_bytes = await file.read()

    try:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        logger.error(f"Error parsing uploaded image: {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while uploaded image processing.")

    predicted_class = cosmoformer.predict(image)
    logger.debug(f"Predicted class: {predicted_class}")

    return InferenceResponse(predicted_class=predicted_class)