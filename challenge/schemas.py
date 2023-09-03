from pydantic import BaseModel, Field, validator

from challenge.exceptions import (
    FlightTypeException,
    MonthException,
    OperatorException,
)


class Flight(BaseModel):
    opera: str = Field(alias="OPERA")
    tipo_vuelo: str = Field(alias="TIPOVUELO")
    mes: int = Field(alias="MES")

    def data(self):
        return {
            "OPERA": self.opera,
            "TIPOVUELO": self.tipo_vuelo,
            "MES": self.mes,
        }

    @validator("mes")
    def validator_mes(cls, value):
        if value not in range(1, 13):
            raise MonthException(status_code=400)

    @validator("tipo_vuelo")
    def validator_tipo_vuelo(cls, value):
        if value not in ["I", "N"]:
            raise FlightTypeException(status_code=400)

    @validator("opera")
    def validator_opera(cls, value):
        available_operators = [
            "Grupo LATAM",
            "Sky Airline",
            "Aerolineas Argentinas",
            "Copa Air",
            "Latin American Wings",
            "Avianca",
            "JetSmart SPA",
            "Gol Trans",
            "American Airlines",
            "Air Canada",
            "Iberia",
            "Delta Air",
            "Air France",
            "Aeromexico",
            "United Airlines",
            "Oceanair Linhas Aereas",
            "Alitalia",
            "K.L.M.",
            "British Airways",
            "Qantas Airways",
            "Lacsa",
            "Austral",
            "Plus Ultra Lineas Aereas",
        ]

        if value not in available_operators:
            raise OperatorException(status_code=400)


class Payload(BaseModel):
    flights: list[Flight]
