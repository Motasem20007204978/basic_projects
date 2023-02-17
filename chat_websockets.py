import websockets as ws 
import asyncio 
from websockets import exceptions
import signal


def parse_room(path:str):
    path = path.removeprefix('/?')
    l = path.split('=')
    room_name = l[1]
    return room_name

ROOMS = {}
def add_room_clilent(websocket, room_name):
    ROOMS[room_name] = ROOMS.get(room_name, []) + [websocket]

async def send_to_room_clients(room_name, message):
    for client in ROOMS[room_name]:
        await client.send(message)

def remove_client(client, room_name):
    index = ROOMS[room_name].index(client)
    del ROOMS[room_name][index]

async def chat(websocket, path):
    room_name = parse_room(path)
    add_room_clilent(websocket, room_name)
    while True: # each connection is still in this loop waiting a message
        try:
            message = await websocket.recv()
            await send_to_room_clients(room_name, message)
        except exceptions.ConnectionClosed:
            remove_client(websocket, room_name)
            break

def sign_handler(signal, frame):
    print('program stopped')
    exit(0)

async def main():
    signal.signal(signal.SIGINT, sign_handler)
    async with ws.serve(chat, 'localhost', 3000):
        print('start serving... press ctrl+c to stop')
        await asyncio.Future() # for ever

if __name__ == '__main__':
    asyncio.run(main())