"""Serve the frontend and calculator API from one FastAPI service."""

from decimal import Decimal
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from engine.calculator import calculate, format_number

WEB = Path(__file__).resolve().parent.parent / "web"
app = FastAPI(title="Simple Calculator", version="1.0.0")
app.mount("/static", StaticFiles(directory=WEB), name="static")


class CalculationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    first: Decimal = Field(max_digits=30, decimal_places=12, allow_inf_nan=False)
    second: Decimal = Field(max_digits=30, decimal_places=12, allow_inf_nan=False)
    operation: Literal["add", "subtract"]


class CalculationResponse(BaseModel):
    result: str
    expression: str


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/calculate", response_model=CalculationResponse)
def calculation(request: CalculationRequest):
    result = calculate(request.first, request.second, request.operation)
    symbol = "+" if request.operation == "add" else "−"
    return CalculationResponse(
        result=format_number(result),
        expression=f"{format_number(request.first)} {symbol} {format_number(request.second)}",
    )
