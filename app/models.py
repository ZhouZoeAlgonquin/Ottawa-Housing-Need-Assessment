"""Pydantic models for data validation and API schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class Indicator(BaseModel):
    """Metadata for an indicator."""
    indicator_code: str = Field(..., description="Unique code for the indicator")
    title: str = Field(..., description="Indicator title")
    description: Optional[str] = Field(None, description="Indicator description")
    section: str = Field(..., description="Section category (e.g., housing_supply)")
    topic: Optional[str] = Field(None, description="Topic subcategory")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    source: Optional[str] = Field(None, description="Data source")
    license: Optional[str] = Field(None, description="License information")
    tags: Optional[List[str]] = Field(default_factory=list, description="Search tags")
    latest_period: Optional[int] = Field(None, description="Most recent period in data")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "indicator_code": "HS_DEV",
                "title": "Housing Development",
                "description": "Housing completions and starts",
                "section": "housing_supply",
                "topic": "Development",
                "unit": "units",
                "source": "City of Ottawa Open Data",
                "license": "Open Government License",
                "tags": ["housing", "development", "completions"],
                "latest_period": 2024,
                "last_updated": "2025-01-01T00:00:00"
            }
        }


class Observation(BaseModel):
    """A single data observation."""
    indicator_code: str = Field(..., description="Indicator code")
    period: int = Field(..., description="Time period (year)")
    geo: str = Field(default="City of Ottawa", description="Geographic area")
    value: float = Field(..., ge=0, description="Numeric value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    breakdowns: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional breakdown fields")
    
    class Config:
        json_schema_extra = {
            "example": {
                "indicator_code": "HS_DEV",
                "period": 2024,
                "geo": "City of Ottawa",
                "value": 6544,
                "unit": "units",
                "breakdowns": {
                    "chart_type": "Housing Completions",
                    "indicator": "Completions - All"
                }
            }
        }


class TrendData(BaseModel):
    """Trend data for an indicator."""
    indicator_code: str
    geo: str
    data_points: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "indicator_code": "HS_DEV",
                "geo": "City of Ottawa",
                "data_points": [
                    {"period": 2020, "value": 6000},
                    {"period": 2021, "value": 6500},
                    {"period": 2022, "value": 7000}
                ]
            }
        }


class DataLoadError(BaseModel):
    """Data load error record."""
    filename: str
    error_type: str
    error_message: str
    timestamp: datetime
    row_data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "Housing Development.csv",
                "error_type": "ValueError",
                "error_message": "Invalid period value",
                "timestamp": "2025-01-01T00:00:00",
                "row_data": {"Year": "invalid"}
            }
        }


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    database: str
    timestamp: datetime

