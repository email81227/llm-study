
import json
import pandas as pd
import yfinance as yf

from langchain_core.documents import Document
from langchain_core.tools import tool, BaseTool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Type, List

from chatbot.prompts.yfin_api_prompt import (
    PROMPT_dividends,
    PROMPT_balance_sheet,
    PROMPT_income_stmt,
    PROMPT_cashflow,
    PROMPT_prices
)


# Define the input schema
class TWSE_CODE(BaseModel):
    twse_code: str = Field(
        description=(
            "A 4-digit code or 5 digits and letters used to identify equities "
            "listed on the Taiwan Stock Exchange or Taipei Exchange codes."
        )
    )
    exchange: str = Field(
        description="The exchange which equity listed on."
    )
class TWSE_PRICE(TWSE_CODE):
    days: int = Field(
        description="The days length prices to request, no longer than 90 days."
    )


class Dividends(BaseTool):
    name = "dividends"
    description = PROMPT_dividends
    args_schema: Type[BaseModel] = TWSE_CODE
    return_direct: bool = False

    def _run(self, twse_code: str, exchange: str="TWSE") -> Document:
        if exchange == "TWSE":
            twse_code += ".TW"
        else:
            twse_code += ".TWO"

        eq = yf.Ticker(twse_code)
        dividends = eq.dividends

        if not dividends.empty:
            dividends = pd.DataFrame(dividends)
            dividends.reset_index(inplace=True)
            dividends['Date'] = dividends['Date'].apply(
                lambda x: x.strftime("%Y-%m-%d")
            )
            dividends.set_index('Date', inplace=True)
            return Document(
                page_content=json.dumps(dividends.to_dict()),
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )
        else:
            return Document(
                page_content="No dividend record founded. Maybe try another exchange.",
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )

    def _arun(self, twse_code: str, exchange: str="TWSE") -> Document:
        return self._run(twse_code, exchange)


class Prices(BaseTool):
    name = "prices"
    description = PROMPT_prices
    args_schema: Type[BaseModel] = TWSE_PRICE
    return_direct: bool = False

    def _run(self, twse_code: str, exchange: str="TWSE", days: int=30) -> Document:
        if exchange == "TWSE":
            twse_code += ".TW"
        else:
            twse_code += ".TWO"

        days = min(90, days)
        months = days // 30

        eq = yf.Ticker(twse_code)
        prices = eq.history(period=f"{months}mo")

        if not prices.empty:
            prices = pd.DataFrame(prices)
            prices.reset_index(inplace=True)
            prices['Date'] = prices['Date'].apply(
                lambda x: x.strftime("%Y-%m-%d")
            )
            prices.set_index('Date', inplace=True)
            prices = prices[['Open', 'High', 'Low', 'Close', 'Volume']]
            return Document(
                page_content=json.dumps(prices.to_dict()),
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )
        else:
            return Document(
                page_content="No historical price founded. Maybe try another exchange.",
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )

    def _arun(self, twse_code: str, exchange: str="TWSE") -> Document:
        return self._run(twse_code, exchange)


class BalanceSheet(BaseTool):
    name = "balance_sheet"
    description = PROMPT_balance_sheet
    args_schema: Type[BaseModel] = TWSE_CODE
    return_direct: bool = False

    def _run(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        if exchange == "TWSE":
            twse_code += ".TW"
        else:
            twse_code += ".TWO"

        eq = yf.Ticker(twse_code)
        balance_sheet = eq.balance_sheet

        if not balance_sheet.empty:
            balance_sheet = pd.DataFrame(balance_sheet)

            bs_last_3yr = []
            for col in balance_sheet.columns:
                year_bs = balance_sheet[col].to_dict()
                year_bs["Year"] = col.year

                bs_last_3yr.append(Document(
                    page_content=json.dumps(year_bs),
                    metatata={
                        "exchange": exchange,
                        "twse_code": twse_code,
                        "year": year_bs["Year"]
                    }
                ))

            return bs_last_3yr
        else:
            return [Document(
                page_content="No balance sheet founded. Maybe try another exchange.",
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )]

    def _arun(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        return self._run(twse_code, exchange)


class IncomeStatement(BaseTool):
    name = "income_stmt"
    description = PROMPT_income_stmt
    args_schema: Type[BaseModel] = TWSE_CODE
    return_direct: bool = False

    def _run(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        if exchange == "TWSE":
            twse_code += ".TW"
        else:
            twse_code += ".TWO"

        eq = yf.Ticker(twse_code)
        income_stmt = eq.income_stmt

        if not income_stmt.empty:
            income_stmt = pd.DataFrame(income_stmt)

            is_last_3yr = []
            for col in income_stmt.columns:
                year_is = income_stmt[col].to_dict()
                year_is["Year"] = col.year

                is_last_3yr.append(Document(
                    page_content=json.dumps(year_is),
                    metatata={
                        "exchange": exchange,
                        "twse_code": twse_code,
                        "year": year_is["Year"]
                    }
                ))

            return is_last_3yr
        else:
            return [Document(
                page_content="No income statement founded. Maybe try another exchange.",
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )]

    def _arun(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        return self._run(twse_code, exchange)


class CashFlow(BaseTool):
    name = "cashflow"
    description = PROMPT_cashflow
    args_schema: Type[BaseModel] = TWSE_CODE
    return_direct: bool = False

    def _run(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        if exchange == "TWSE":
            twse_code += ".TW"
        else:
            twse_code += ".TWO"

        eq = yf.Ticker(twse_code)
        cashflow = eq.cashflow

        if not cashflow.empty:
            cashflow = pd.DataFrame(cashflow)

            cf_last_3yr = []
            for col in cashflow.columns:
                year_cf = cashflow[col].to_dict()
                year_cf["Year"] = col.year

                cf_last_3yr.append(Document(
                    page_content=json.dumps(year_cf),
                    metatata={
                        "exchange": exchange,
                        "twse_code": twse_code,
                        "year": year_cf["Year"]
                    }
                ))

            return cf_last_3yr
        else:
            return [Document(
                page_content="No cashflow founded. Maybe try another exchange.",
                metatata={
                    "exchange": exchange,
                    "twse_code": twse_code
                }
            )]

    def _arun(self, twse_code: str, exchange: str="TWSE") -> List[Document]:
        return self._run(twse_code, exchange)


cashflow = CashFlow()
income_stmt = IncomeStatement()
balance_sheet = BalanceSheet()
dividends = Dividends()
prices = Prices()
