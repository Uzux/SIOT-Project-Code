import discord
from discord.ext import commands
import asyncio
import getData

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

client.run("INPUT TOKEN HERE")