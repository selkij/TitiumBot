import asyncio
import json
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
@commands.has_permissions(administrator=True)
async def status(ctx, ip, port="25565"):
    await ctx.message.delete()

    while True:
        server_r = requests.get('https://mcapi.us/server/status?ip=' + ip + '&port=' + port)
        server_data = server_r.json()

        desc = server_data["motd"]
        online = server_data["online"]
        status = server_data["status"]
        serverName = "Titium S2"
        playerCount = server_data["players"]["now"]
        playerMax = server_data["players"]["max"]
        version = server_data["server"]["name"]
        duration = server_data["duration"]

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

        if online:
            iconRaw = server_data["favicon"]
            icon = iconRaw.split(',', 1)
            favicon = discord.File(io.BytesIO(base64.b64decode(icon[1])), filename="favicon.png")
        else:
            favicon = None

        serverEmbed = discord.Embed(title=f"{serverName}", color=color)
        serverEmbed.set_thumbnail(url="attachment://favicon.png")
        serverEmbed.add_field(name="Addresse IP:", value=f"{ip}:{port}")
        serverEmbed.add_field(name="Status:", value=online, inline=False)
        serverEmbed.add_field(name="Version:", value=version, inline=False)
        serverEmbed.add_field(name="Players:", value=f"{playerCount} / **{playerMax}** MAX", inline=False)

        if server_data["error"] is not None:
            serverEmbed.add_field(name="Error:", value=server_data["error"], inline=False)

        serverEmbed.set_footer(text=f"Titium S2 | Cela a pris {math.trunc(float(duration) / 1000000)}ms à McAPI")

        print(server_data)
        await ctx.send(embed=serverEmbed, file=favicon, delete_after=90)
        await asyncio.sleep(90)


@status.error
async def statusError(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("> ⛔ Tu n'as pas la permission `administrator` pour effectuer cette commande!", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("> ⛔ Veuillez entrer une addresse IP et son port \nExemple: `*status hypixel.net <port=25565>", delete_after=5)


bot.run(token)
