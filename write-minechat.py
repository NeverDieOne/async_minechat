import argparse
import asyncio
import logging
import json
from dotenv import load_dotenv
import os


async def register(username, writer, reader):
    print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')

    if not username:
        username = input('Введи желаемый nickname: ')

    writer.write(f"{username}\n\n".encode())
    await writer.drain()

    logging.info(await reader.readuntil(b'\n'))
    recieved_data = json.loads(await reader.readuntil(b'\n'))
    logging.info(recieved_data)

    print(f'Запомни свой токен: {recieved_data["account_hash"]}')
    return recieved_data


async def authorise(token, writer, reader):
    logging.info(await reader.readuntil(b'\n'))

    if not token:
        token = input('Введи token: ')

    writer.write(f"{token}\n".encode())
    await writer.drain()

    recieved_data = json.loads(await reader.readuntil(b'\n'))
    logging.info(recieved_data)
    return recieved_data


async def submit_message(writer, message=None):
    if not message:
        message = input('>> ')

    writer.write(f"{message}\n\n".encode())
    await writer.drain()


# TODO придумать как убрать \n в сообщениях (шаг 12)
async def write_to_tcp_connection(arguments):
    host = os.getenv('HOST') or arguments.host
    port = os.getenv('WRITE_PORT') or arguments.port
    message = arguments.text
    token = os.getenv('TOKEN') or arguments.token
    username = os.getenv('USERNAME') or arguments.username

    reader, writer = await asyncio.open_connection(host, port)
    recieved_data = await authorise(token, writer, reader)

    if not recieved_data:
        recieved_data = await register(username, writer, reader)

    await reader.readuntil(b'\n')
    print(f'Добро пожаловать в чат {recieved_data["nickname"]}')

    await submit_message(writer, message)


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Write messages to TCP connection')
    parser.add_argument('--token', help='Token to connect')
    parser.add_argument('--text', help='Text message to write in chat')
    parser.add_argument('--host', help='Host to connection')
    parser.add_argument('--port', help='Port to connection')
    parser.add_argument('--username', help='Username to connect')
    args = parser.parse_args()

    asyncio.run(write_to_tcp_connection(args))
