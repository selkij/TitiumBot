import asyncio
import math
import time
import os
from dotenv import load_dotenv

import discord, io, base64, requests
from discord.ext import commands

bot = commands.Bot(command_prefix="*")

load_dotenv()

token = os.getenv("TOKEN")


@bot.event
async def on_ready():
    game = discord.Game("Titium S2!")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print("Bot ready")


@bot.command()
async def minecraft(ctx, ip, port="25565"):
    while True:
        r = requests.get('https://mcapi.us/server/status?ip=' + ip + '&port=' + port)
        json_data = r.json()

        desc = json_data["motd"]
        online = json_data["online"]
        status = json_data["status"]
        serverName = "Titium S2"
        playerCount = json_data["players"]["now"]
        playerMax = json_data["players"]["max"]
        version = json_data["server"]["name"]
        duration = json_data["duration"]

        if online:

            if status != "success":
                online = "⚠️ **Problèmes de connexion détectés**"
                color = 0xffdc00
            else:
                online = "✅ **Ouvert**"
                color = 0x49ff00
        else:
            online = "❌ **Fermé**"
            color = 0xdf1515

        if online == "True":
            iconRaw = json_data["favicon"]
            icon = iconRaw.split(',', 1)
            favicon = discord.File(io.BytesIO(base64.b64decode(icon[1])), filename="favicon.png")
        else:
            favicon = None

        serverEmbed = discord.Embed(title=f"{serverName}", color=color)
        serverEmbed.set_thumbnail(url="attachment://favicon.png")
        serverEmbed.add_field(name="Status:", value=online, inline=False)
        serverEmbed.add_field(name="Version:", value=version, inline=False)
        serverEmbed.add_field(name="Players:", value=f"{playerCount} / **{playerMax}** MAX", inline=False)

        if json_data["error"] is not None:
            serverEmbed.add_field(name="Error:", value=json_data["error"], inline=False)

        serverEmbed.set_footer(text=f"Titium S2 | Cela a pris {math.trunc(float(duration) / 1000000)}ms")

        print(json_data)
        await ctx.send(embed=serverEmbed, file=favicon, delete_after=60)
        await asyncio.sleep(60)


bot.run(token)
