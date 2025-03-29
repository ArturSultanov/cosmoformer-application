from pydantic import BaseModel

class InferenceResponse(BaseModel):
    predicted_class: str
