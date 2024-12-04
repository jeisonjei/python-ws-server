import asyncio
import websockets

connections = set()
history = []
server_url = None  # Переменная для хранения текущего URL сервера

async def get_server_url(server):
    global server_url
    server_url = f'ws://{server.sockets[0].getsockname()[0]}:{server.sockets[0].getsockname()[1]}'
    print(f'Server is running at {server_url}')

async def chat(websocket, path):
    global history
    connections.add(websocket)

    # Отправляем историю сообщений новому клиенту
    for message in history:
        await websocket.send(message)

    try:
        async for message in websocket:
            # Сохраняем сообщение в истории
            history.append(message)

            # Рассылаем сообщение всем подключённым клиентам
            for conn in connections:
                await conn.send(message)
    finally:
        connections.remove(websocket)

async def main():
    server = await websockets.serve(chat, '0.0.0.0', 8765)
    await get_server_url(server)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())