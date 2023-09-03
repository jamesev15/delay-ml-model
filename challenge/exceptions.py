from fastapi import HTTPException


class PreprocessException(HTTPException):
    """Bad preprocessing exception"""


class MonthException(HTTPException):
    """Invalid month exception"""


class FlightTypeException(HTTPException):
    """Invalid flight type exception"""


class OperatorException(HTTPException):
    """Invalid operator exception"""
