from openai import OpenAI

import os

from dotenv import load_dotenv

load_dotenv(".env")


client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")

fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
"""

prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Technical specifications: ```{fact_sheet_chair}```
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "2021年的世界足球大賽冠軍是哪一個國家取得，叫什麼隊伍? 請用中文回答",
        },
        # {
        #     "role": "assistant",
        #     "content": "我不知道你說什麼",
        # },
        {"role": "user", "content": "2021年的世界足球大賽冠軍義大利隊? 確定嗎？"},
        {
            "role": "user",
            "content": "2021年的世界足球大賽冠軍，隊長叫什麼名字? 確定嗎？",
        },
        {
            "role": "user",
            "content": "真的是義大利嗎? 確定嗎？",
        },
    ],
    temperature=0.8,
    max_tokens=64,
    top_p=1,
)

print(response)
