from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator


class Ticker(BaseModel):
    code: str
    code_international: Optional[str] = None
    company_name: str
    source_info: str
    dt_extracted: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


    @model_validator(mode="before")
    @classmethod
    def generate_code_international(cls, values):
        """Garante a inclusão do atributo code_international para representação do ticker"""
        values["code_international"] = values["code"] + ".SA"
        return values


    @field_validator("source_info")
    @classmethod
    def normalize_source_info(cls, value: str):
        """Garante a padronização do atributo source_info"""
        return value.strip().lower()
