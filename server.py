import asyncio
import websockets

connections = set()
history = []  # Список для хранения истории сообщений

async def chat(websocket):
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
    async with websockets.serve(chat, 'localhost', 8765) as server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())