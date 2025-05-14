from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
from dotenv import load_dotenv
import asyncio
import aiohttp
import os

load_dotenv()

async def ready(ready_event: EventData):
    print("Hello! I'm joining a channel")
    await ready_event.chat.join_room(os.environ.get('CHANNEL'))

async def message(msg: ChatMessage):
    print(f"{msg.room.name} {msg.user.name}: {msg.text}")

async def guess(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        pass
    else:
        await cmd.reply(f"{cmd.user.name} guessed {cmd.parameter}")
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://localhost:5000/game/", data=f"{cmd.parameter}")
            # await print(response.read())


async def run():
    scope = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

    twitch = await Twitch(os.environ.get('BOT_ID'), os.environ.get('BOT_SECRET'))
    auth = UserAuthenticator(twitch, scope)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, scope, refresh_token)

    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, ready)
    chat.register_event(ChatEvent.MESSAGE, message)
    chat.register_command("guess", guess)
    chat.start()

    try:
        input("Press enter to stop\n")
    finally:
        chat.stop()
        await twitch.close()

if __name__ == "__main__":
    asyncio.run(run())