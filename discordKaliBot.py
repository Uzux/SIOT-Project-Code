import discord
from discord.ext import commands

def SendMsg(msg):
    client = commands.Bot(command_prefix="!", intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print("We good to go!")
        uzux = await client.fetch_user("138510803610370048")
        # uzux = await client.fetch_user("320660152770494468") # Tristans
        await uzux.send(msg)
        await client.close()

    client.run("MTE3OTg3MDE1ODQxMjU5OTM0Nw.GhnLYW.a_uE1v7Jj8ilHFrpNvkbHGUDsKyMdOlQhVdtFI")