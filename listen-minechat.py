from dotenv import load_dotenv
import asyncio
import aiofiles
import argparse
import datetime

load_dotenv()


# TODO сделать проверку на обрыв соединения
async def tcp_echo_client(host, port, filename):
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(filename, mode='a') as file:
        while True:
            data = await reader.read(500)
            time_now = datetime.datetime.now()
            formated_time = time_now.strftime('%e.%m.%Y %H:%M:%S')
            await file.write(f"[{formated_time}] {data.decode()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read messages from TCP connection')
    parser.add_argument('--port', help='Port to connection')
    parser.add_argument('--host', help='Host to connection')
    parser.add_argument('--file', help='Output file with chat')
    args = parser.parse_args()

    asyncio.run(tcp_echo_client(args.host, args.port, args.file))
