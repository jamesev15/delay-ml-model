import pandas as pd
from fastapi import FastAPI

from challenge.exceptions import PreprocessException
from challenge.model import DelayModel
from challenge.schemas import Payload

app = FastAPI()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(payload: Payload) -> dict:
    flights_to_process = [flight.data() for flight in payload.flights]
    flights_df = pd.DataFrame(flights_to_process)

    model = DelayModel()
    features = model.preprocess(data=flights_df)
    if isinstance(features, tuple):
        raise PreprocessException(status_code=400)

    predictions = model.predict(features=features)

    return {"predict": predictions}
