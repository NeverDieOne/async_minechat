from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(os.getenv("HOST"), os.getenv("PORT"))

    while True:
        data = await reader.read(1024)
        print(f'{data.decode()!r}')


if __name__ == '__main__':
    asyncio.run(tcp_echo_client())
