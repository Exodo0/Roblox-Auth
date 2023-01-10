# Configuration
BOT_TOKEN = "MTAxNDk5MDc5MzI4MDMyMzYyNA.GdscI-.nPdhZeOd0jqJQw6PJi3n_lpa5j4G3_6R-_l3pU"
BOT_PREFIX = "¿"
WORD_FILE = "words.txt"
KEY_COUNT = 5
CHECKS = 10
COOLDOWN = 2

# Imports/Dependencies
import discord
from rich import print
from rich.console import Console
from discord.ext import commands
from asyncio import sleep
from backend import check, words

# Setup rich
con = Console()
con.clear()

# Setup client
with con.status("[red]Setting up client[/red]", spinner="point", spinner_style="white"):
    word_list = words.get_words(WORD_FILE)
    roauth = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())

# Commands
@roauth.event
async def on_ready():
    print(f"[white]RoAuth is online![/white]\n[white]Logged into:[/white] [red]{roauth.user}[/red]\n")
    
@roauth.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown", description=f"Please try again in {error.retry_after} second(s).", color=0xff0000)
        await ctx.send(f"{ctx.message.author.mention}", embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed2 = discord.Embed(title="Oops!", description="Te falto agregar tu ID de Roblox.", color=0xff0000)
        await ctx.send(f"{ctx.message.author.mention}", embed=embed2)

@commands.cooldown(1, COOLDOWN, commands.cooldowns.BucketType.member)

@roauth.command(aliases=["embeds"])
async def ctx(ctx):

    embed4 = discord.Embed(title="Modo de Verificacion", description="Mizu es un bot de verificación de Roblox.", color=0x00ff00)
    embed4.add_field(name="Usa el Comando", value="`.verify [ID de Roblox]`", inline=False)
    embed4.set_footer(text="Para Verificarte")
    await ctx.send(f"{ctx.message.author.mention}", embed=embed4)



@roauth.command(aliases=["verify", "Verify"])
async def authenticate(ctx, userId: int):
    u = check.user(userId)
    skey = words.generate_key(word_list, KEY_COUNT)
    if u.exists() == True:
        embed3 = discord.Embed(title="Verificación", description=f"Agrega estas Frases a tu descripción en roblox: `{skey}` , Te contactare en Roblox como `{u.username()}`", color=0x00ff00)
        await ctx.send(f"{ctx.message.author.mention}", embed=embed3)
        for _ in range(CHECKS):
            if u.compare(skey) == True:
                await ctx.send(f"{ctx.author.mention}, Tu cuenta ha sido verificada.")
                try:
                    await ctx.author.edit(nick=u.username())
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=1054211550803677264))
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=1054214136680157186))
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=1054536499019927572))
                    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, id=1054536345785217034))

                    ##
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=776552716339773501))
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=770074011350073394))
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=947606964920266763))
                    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=839622200876728321))
                    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, id=776552945499504681))
                except: 
                    pass
                break
            else:
                await sleep(5)
    else:
        await ctx.send(f"{ctx.author.mention}, Tu ID de Roblox no existe.")

roauth.run(BOT_TOKEN)