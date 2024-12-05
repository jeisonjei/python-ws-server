import asyncio
import websockets
import ssl

# Создаем SSL контекст
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('certs/95.182.120.168.pem', 'certs/95.182.120.168-key.pem')

connections = set()
history = []
server_url = None  # Переменная для хранения текущего URL сервера

async def get_server_url(server):
    global server_url
    server_url = f'wss://0.0.0.0:{server.sockets[0].getsockname()[1]}'
    print(f'Server is running at {server_url}')

async def chat(websocket):
    global history
    connections.add(websocket)

    # Отправляем историю сообщений новому клиенту
    for message in history:
        await websocket.send(message)

    try:
        async for message in websocket:
            # Сохраняем сообщение в истории
            print(f'>>> {message}')
            history.append(message)

            # Рассылаем сообщение всем подключённым клиентам
            for conn in connections:
                await conn.send(message)
    finally:
        connections.remove(websocket)

async def main():
    server = await websockets.serve(chat, '', 8765, ssl=ssl_context)
    await get_server_url(server)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())