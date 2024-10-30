# async_helpers.py
import asyncio
from ollama import AsyncClient

async def async_chat(model_name, message):
    async_client = AsyncClient()
    response = await async_client.chat(model=model_name, messages=[{'role': 'user', 'content': message}])
    return response['message']['content']

async def async_chat_stream(model_name, message):
    async_client = AsyncClient()
    async for part in await async_client.chat(model=model_name, messages=[{'role': 'user', 'content': message}], stream=True):
        print(part['message']['content'], end='', flush=True)
