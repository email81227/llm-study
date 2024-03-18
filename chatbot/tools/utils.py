
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict


def dict2content(d: Dict[str, str]) -> str:
    content = str(d)[1:-1]
    content = (
        content
        .replace("'", "")
        .replace("/r/n", "")
        .replace( ", ", '\n')
    )

    return content


# Define the input schema
class OptionalAssetCode(BaseModel):
    twse_code: str = Field(
        default=None,
        description=(
            "A 4-digit code or 5 digits and letters used to identify equities "
            "listed on the Taiwan Stock Exchange or Taipei Exchange codes."
        )
    )


# Define the input schema
class AssetCode(BaseModel):
    twse_code: str = Field(
        description=(
            "A 4-digit code or 5 digits and letters used to identify equities "
            "listed on the Taiwan Stock Exchange or Taipei Exchange codes."
        )
    )


# Define the input schema
class AssetCodeExchange(AssetCode):
    exchange: str = Field(
        description="The exchange which equity listed on."
    )


class AssetCodeExchangeDays(AssetCodeExchange):
    days: int = Field(
        description="The days length prices to request, no longer than 90 days."
    )
