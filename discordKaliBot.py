import discord
from discord.ext import commands
import asyncio
import getData

# def SendMsg(msg):
#     client = commands.Bot(command_prefix="!", intents=discord.Intents.default())
#     @client.event
#     async def on_ready():
#         print("We good to go!")
#         uzux = await client.fetch_user("138510803610370048")
#         await uzux.send(msg)
#         await client.close()
#         print("closed")

#     client.run("MTE3OTg3MDE1ODQxMjU5OTM0Nw.GhnLYW.a_uE1v7Jj8ilHFrpNvkbHGUDsKyMdOlQhVdtFI")
#     client.close()

client = commands.Bot(command_prefix="!", intents=discord.Intents.default())
@client.event
async def on_ready():
    print("We good to go!")
    try:
        while True:
            msg = getData.main(15, 10)
            if msg:
                uzux = await client.fetch_user("138510803610370048")
                print(msg)
                await uzux.send(msg)
            await asyncio.sleep(600)
    except KeyboardInterrupt:
        print("Stopped")

client.run("MTE3OTg3MDE1ODQxMjU5OTM0Nw.GhnLYW.a_uE1v7Jj8ilHFrpNvkbHGUDsKyMdOlQhVdtFI")