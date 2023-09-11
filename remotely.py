# Remotely by aspectxyz
# People that try to steal this code are fr dumb
import json
import subprocess
import os
import asyncio
import requests
from datetime import datetime, timedelta
try:
    import discord
    from discord.ext import commands
except:
    os.system("pip install discord.py")
try:
    from bs4 import BeautifulSoup
except:
    os.system("pip install beautifulsoup4")
try:
    from rgbprint import gradient_print, Color, rgbprint
except:
    os.system("pip install rgbprint")
try:
    import pyautogui
except:
    os.system("pip install pyautogui")
    os.system("pip install Pillow")

os.system("cls")
with open("config.json") as file:
    config = json.load(file)

token = config['Discord']['Token']
prefix = config['Discord']['Prefix']
pfile = 'main.py'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=f'{prefix}', intents=intents, help_command=None)

start_time = None
process = False

title = """
                     /$$$$$$$                                      /$$               /$$          
                    | $$__  $$                                    | $$              | $$          
                    | $$  \ $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$    /$$$$$$ | $$ /$$   /$$
                    | $$$$$$$/ /$$__  $$| $$_  $$_  $$ /$$__  $$|_  $$_/   /$$__  $$| $$| $$  | $$
                    | $$__  $$| $$$$$$$$| $$ \ $$ \ $$| $$  \ $$  | $$    | $$$$$$$$| $$| $$  | $$
                    | $$  \ $$| $$_____/| $$ | $$ | $$| $$  | $$  | $$ /$$| $$_____/| $$| $$  | $$
                    | $$  | $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$/  |  $$$$/|  $$$$$$$| $$|  $$$$$$$
                    |__/  |__/ \_______/|__/ |__/ |__/ \______/    \___/   \_______/|__/ \____  $$
                                                                                         /$$  | $$
                                                                                        |  $$$$$$/
                                                                                         \______/                    
"""

async def update_title():
    while True:
        gradient_print(title, start_color=Color(0xE10B0B), end_color=Color(0xB20505))
        await asyncio.sleep(2)
        os.system("cls")

@bot.event
async def on_ready():
    bot.loop.create_task(update_title())
    os.system("cls")

auto_restarta = False
@bot.command(name="autorestart", aliases=["ar"])
async def autorestart(ctx, toggle=None, interval=None):
    global process,auto_restarta
    if toggle is None and interval is None:
        embed = discord.Embed(
            title='Error',
            description=f':x: | Please specify on/off and the interval between each restart. ex: {prefix}ar on 10m',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)
        return
    
    if toggle is None:
        embed = discord.Embed(
            title='Error',
            description=':x: | Please specify on or off',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)
        return

    if toggle.lower() == "on":
        if interval is None:
            embed = discord.Embed(
                title='Error',
                description=':x: | Please specify the interval between each restart. ex: on 10m',
                color=discord.Color.red()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
            await ctx.send(embed=embed)
            return

        try:
            intervalv, intervalu = parse_interval(interval)
            if intervalv <= 0:
                raise ValueError('Invalid interval value.')

            async def auto_restart():
                global process,auto_restarta
                while auto_restarta:
                    current_pid = os.getpid()
                    processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
                    programs_to_kill = ['python.exe', 'cmd.exe']
                    for proces in processes:
                        for program in programs_to_kill:
                            if program in proces:
                                pid = int(proces.split()[1])
                                if pid != current_pid:
                                    os.system(f'taskkill /PID {pid} /F')
                                    process = False

                    os.system(f"start /B start cmd.exe @cmd /k py {pfile}")
                    process = True
                    await asyncio.sleep(intervalv)

            auto_restarta = True
            bot.loop.create_task(auto_restart())
            response = f'✅ | Sniper will start auto restarting every {interval}.'
            embed = discord.Embed(
                title='Success',
                description=f'{response}',
                color=discord.Color.green()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        except Exception as e:
            response = f'❌ | Error starting auto restart: {e}'
            embed = discord.Embed(
                title='Error',
                description=f'{response}',
                color=discord.Color.red()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')

    elif toggle.lower() == "off":
        if auto_restarta:
            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']
            for proces in processes:
                for program in programs_to_kill:
                    if program in proces:
                        pid = int(proces.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')
                            process = False

            auto_restarta = False
            embed = discord.Embed(
                title='Success',
                description='✅ | Auto restart has been turned off. (*Sniper stopped*)',
                color=discord.Color.green()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        else:
            embed = discord.Embed(
                title='Info',
                description='❗ | Auto restart is not currently active.',
                color=discord.Color.blue()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
    else:
        embed = discord.Embed(
            title='Error',
            description=':x: | Invalid toggle. Please use `on` or `off`.',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')

    await ctx.send(embed=embed)

def parse_interval(interval):
    intervalv = int(interval[:-1])
    intervalu = interval[-1]
    if intervalu == 'm':
        intervalv *= 60
    elif intervalu == 'h':
        intervalv *= 3600
    elif intervalu == 'd':
        intervalv *= 86400
    else:
        raise ValueError('Invalid interval unit.')

    return intervalv, intervalu

@bot.command(name="ss")
async def screenshot(ctx):
    try:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        waitmsg = await ctx.send("Please wait...")

        filename = "screenshot.png"
        filepath = os.path.join("screenshots", filename)
        pyautogui.screenshot(filepath)

        file = discord.File(filepath, filename=filename)
        embed = discord.Embed(
            title="Screenshot",
            description="Here is a screenshot of your PC:",
            color=discord.Color.blue()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        embed.set_image(url=f"attachment://{filename}")

        await ctx.send(embed=embed, file=file)
        await waitmsg.delete()
    except Exception as e:
        response = f'❌ | Error taking a screenshot: {e}'
        embed = discord.Embed(
            title='Error',
            description=f'{response}',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)
        await waitmsg.delete()

@bot.command(name="check", aliases=["c"])
async def check(ctx, id):
    try:
        id = int(id)
    except ValueError:
        embed = discord.Embed(
            title='Error',
            description='❌ | Please provide a valid ID.',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)
        return
    
    if id is not None:
        try:
            waitmsg = await ctx.send("Please wait...")
            fcsrf = requests.post('https://auth.roblox.com/v1/usernames/validate')
            csrf = fcsrf.headers['x-csrf-token']
            fetch = 'https://catalog.roblox.com/v1/catalog/items/details'
            headers = {
                'X-Csrf-Token': f'{csrf}'
            }
            payload = {
                'items': [
                    {
                        'itemType': 1,
                        'id': id
                    }
                ]
            }
            response = requests.post(fetch, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json().get('data', [])
                if data:
                    item = data[0]
                    price = item.get('price')
                    status = item.get('priceStatus')
                    type_value = item.get('saleLocationType')
                    quantity = item.get('totalQuantity')
                    limit = item.get('quantityLimitPerUser')
                    description = item.get('description')
                    item_name = item.get('name')
                    item_id = item.get('id')
                    creator_name = item.get('creatorName')
                    
                    findimage = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={item_id}&returnPolicy=PlaceHolder&size=420x420&format=Png&isCircular=false").json()
                    images = findimage.get('data', [])
                    if images:
                        getimage = images[0].get('imageUrl')
                    else:
                        getimage = None
                    
                    embed_description = f"• __**Name:**__ {item_name}\n\n• __**Creator:**__ {creator_name}\n\n"
                    
                    if price is not None:
                        embed_description += f"• __**Price:**__ {price}\n\n"
                    if status is not None:
                        embed_description += f"• __**Status:**__ {status}\n\n"
                    if limit is not None:
                        embed_description += f"• __**Limit:**__ {limit}\n\n"
                    if quantity is not None:
                        embed_description += f"• __**Quantity:**__ {quantity}\n\n"
                    embed_description += f"• __**Type:**__ {type_value}\n\n"
                    embed_description += f"• __**Link:**__ https://roblox.com/catalog/{item_id}/Remotely\n\n"
                    if description is not None:
                        embed_description += f"• __**Description:**__ ```{description}```"
                    
                    embed = discord.Embed(
                        title='Info',
                        description=embed_description,
                        color=discord.Color.blue()
                    )
                    
                    if getimage is not None:
                        embed.set_thumbnail(url=getimage)
                    
                    await ctx.send(embed=embed)
                    await waitmsg.delete()
                else:
                    await ctx.send(f"❌ | No data found for the ID {id}.")
                    await waitmsg.delete()
            elif response.status_code == 429:
                embed = discord.Embed(
                    title='Rate Limit!',
                    description=f'❌ | Rate limit exceeded. Please wait 1m and try again!',
                    color=discord.Color.red()
                )
                embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
                await ctx.send(embed=embed)
                await waitmsg.delete()
            else:
                embed = discord.Embed(
                    title='Weird..',
                    description=f'❌ | Something weird happened while fetching your ID.',
                    color=discord.Color.red()
                )
                embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
                await ctx.send(embed=embed)
                await waitmsg.delete()
        except Exception as e:
            embed = discord.Embed(
                title='Error',
                description=f'❌ | An error occurred: {e}',
                color=discord.Color.red()
            )
            embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
            await ctx.send(embed=embed)
            await waitmsg.delete()

@check.error
async def checkerr(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) and error.param.name == 'id':
        embed = discord.Embed(
            title='Error',
            description='❌ | Please provide an ID.',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)


@bot.command(name="config", aliases=["cf"])
async def config_command(ctx):
    try:
        with open("config.json") as file:
            data = json.load(file)

        if auto_restarta:
            config = f"**Auto restart:** Enabled\n"
        else:
            config = f"**Auto restart:** Disabled\n"
        config += f"**ID(s):** {len(data['Items'])}\n"
        config += f"**Wait time:** {data['Speed']['Wait_time']}\n"
        config += f"**Buy Cookie:** ||{data['Buy_cookies']}||\n"
        config += f"**Check Cookie:** ||{data['Check_cookie']}||\n"
        embed = discord.Embed(
            title='Configuration Settings',
            description=config,
            color=discord.Color.blue()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occured: {e}',
            color=discord.Color.red()
        )
        embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')
        await ctx.send(embed=embed)    

    


@bot.command(name="help", aliases=['h'], description="Shows the help message.")
async def help_command(ctx):
    pages = [
        [
            {"name": f'{prefix}autorestart `[toggle]` `[interval]`   |   {prefix}ar `[toggle]` `[interval]`', "value": 'Automatically restarts death sniper every X amount of time. Toggle: on, off'},
            {"name": f'{prefix}config   |   {prefix}cf', "value": 'View the current configuration settings.'},
            {"name": f"{prefix}ss", "value": "Takes a screenshot of your PC."},
            {"name": f"{prefix}check `<id>`   |   {prefix}c `<id>`", "value": "Checks information about a catalog item."},
            {"name": f"{prefix}help   |   {prefix}h", "value": "Shows this message."},
        ],
    ]

    page = 0

    async def update_embed():
        embed.clear_fields()
        embed.title = f"• Remotely's Commands - Page {page + 1}"
        embed.description = "**THESE ARE THE COMMANDS YOU CAN USE - **"
        for command in pages[page]:
            embed.add_field(name=command['name'], value=command['value'], inline=False)
        await message.edit(embed=embed)

    embed = discord.Embed(
        title=f"• Remotely's Commands - Page {page + 1}",
        url="https://discord.gg/wHAx7zEVFW",
        description="**THESE ARE THE COMMANDS YOU CAN USE - **",
        color=discord.Color.blue()
    )
    for command in pages[page]:
        embed.add_field(name=command['name'], value=command['value'], inline=False)
    embed.set_footer(text='Death Sniper on top', icon_url='https://cdn-icons-png.flaticon.com/512/521/521269.png')

    message = await ctx.send(embed=embed)
    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['◀', '▶'] and reaction.message.id == message.id

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            break

        if str(reaction.emoji) == '◀' and page > 0:
            page -= 1
            await update_embed()
            await message.remove_reaction('◀', user)
        elif str(reaction.emoji) == '▶' and page < len(pages) - 1:
            page += 1
            await update_embed()
            await message.remove_reaction('▶', user)
        elif str(reaction.emoji) == '▶' and page == len(pages) - 1:
            await message.remove_reaction('▶', user)
        elif str(reaction.emoji) == '◀' and page == 0:
            await message.remove_reaction('◀', user)

    await message.clear_reactions()

loop = asyncio.get_event_loop()
loop.create_task(update_title())
bot.run(token)