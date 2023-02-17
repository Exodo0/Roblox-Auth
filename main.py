
# Dependencias y Extras
import discord
from backend import check, words
from asyncio import sleep
from discord.ext import commands
from rich.console import Console
from rich import print
from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("Token")
BOT_PREFIX = os.getenv("Prefix")
WORD_FILE = "words.txt"
KEY_COUNT = 5
CHECKS = 60
COOLDOWN = 10
# Setup Console
con = Console()
con.clear()
# Setup Bot
with con.status("[bold green] Bot Funcionando... [bold green]"):
    word_list = words.get_words(WORD_FILE)
    roauth = commands.Bot(command_prefix=BOT_PREFIX,
                          intents=discord.Intents.all(), help_command=None, description="Bot de verificacion de roblox")

    @roauth.event
    async def on_ready():
        print(f"Estamos listos como {roauth.user.name}!")

    @roauth.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Oops!", description=f"Debes esperar {error.retry_after:.2f} segundos para usar este comando.", color=0xff0000)
            await ctx.send(f"{ctx.message.author.mention}", embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed2 = discord.Embed(
                title="Ocurrio un Error", description=f"Debes ingresar un ID de usuario de roblox", color=0xff0000)
            await ctx.send(f"{ctx.message.author.mention}", embed=embed2)

    @commands.cooldown(1, COOLDOWN, commands.BucketType.user)
    @roauth.command(aliases=["verify", "Verify"])
    async def authenticate(ctx, userId: int):
        u = check.user(userId)
        skey = words.generate_key(word_list, KEY_COUNT)
        if u.exists() == True:

            embed2 = discord.Embed(
                # Se agrega el thumbnail con la imagen de perfil de roblox del usuario
                title="Bienvenido a tu verificacion", description=f"**Esta es tu llave Ingresala en tu perfil de roblox:** \n\n↪ **{skey}** ↩ \n\nVerificando usuario: {u.username()}", color=0x00ff00)

            await ctx.send(f"{ctx.author.mention}", embed=embed2)
            for _ in range(CHECKS):
                if u.compare(skey) == True:
                    await ctx.send(f"{ctx.author.mention} Estamos Procesando Tu Verificacion!")
                    await sleep(5)
                    try:
                        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=1063684899304915005))
                        # Se cambia el nombre del usuario a su nombre de roblox
                        await ctx.author.edit(nick=u.username())
                    except:
                        pass
                    break
                else:
                    await sleep(5)
        else:
            embed4 = discord.Embed(
                description="El usuario no existe", color=0x00ff00)
            await ctx.send(f"{ctx.author.mention}", embed=embed4)

    roauth.run(BOT_TOKEN)
