from imaplib import Commands
import discord
from discord.ext import commands
import logging
import os
import random
import time
import bank
from cogs import slots
from dotenv import load_dotenv
import asyncio

'''Token for the bot'''
load_dotenv()
TOKEN = os.getenv('TOKEN')

'''Setting intents'''
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

'''logging'''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

'''Initializes bot'''
gamblebot = discord.Bot(intents=intents)

'''events'''
@gamblebot.event
async def on_ready():
    print(f'Logged in as {gamblebot.user}')

async def main():
    async with gamblebot:
        print("Loading extension:", "cogs.slots")
        try:
            gamblebot.add_cog(slots.SlotsCog(gamblebot))
            print('Successfully Loaded: cogs.slots')
        except Exception as e:
            print("Error Loading cogs.slots")
            print(f"Exception: {e}")
        await gamblebot.start(TOKEN) 

#@gamblebot.event (Make it so it DMs the user welcoming them to the server and telling them their current bank balance)

'''commands'''
#TODO Add help command

@gamblebot.command(description="Gets the bot's ping")
async def ping(ctx):
    await ctx.respond(f'Pong! {gamblebot.latency} ms')

@gamblebot.command(description="For when you need a little Inspriation to keep going")
async def inspiration(ctx):
    text_file = 'inspiration.txt'
    with open(text_file, 'r') as file:
        quotes = file.readlines()
        random_quote = random.choice(quotes).strip()
    await ctx.respond(random_quote)

'''Bank commands'''
#TODO Make a daily login reward system
@gamblebot.command()
async def balance(ctx):
    memberData = bank.loadMemberData(ctx.author.id)
    MoneySpread = discord.Embed(title=f'{ctx.author.name}\'s Stats')
    MoneySpread.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
    MoneySpread.add_field(name='💼 Wallet:', value=f':coin: {memberData.chips}')
    MoneySpread.add_field(name=':bank: Bank:', value=f':coin: {memberData.bank}')
    await ctx.respond(embed=MoneySpread)

@gamblebot.command()
async def deposit(ctx, amount):
    memberData = bank.loadMemberData(ctx.author.id)
    try:
        deposit = bank.depositMember(memberData, int(amount))
    except:
        await ctx.respond(f'Invalid Input Dumbass')
        raise ValueError
    if deposit == False:
        await ctx.respond(f'Not enough chips on hand to deposit that amount.')
    else:
        bank.saveMemberData(ctx.author.id, memberData)
        await ctx.respond(f'Deposited {amount} chips into your bank')

@gamblebot.command()
async def withdrawl(ctx, amount):
    memberData = bank.loadMemberData(ctx.author.id)
    try:
        withdrawl = bank.withdrawlMember(memberData, int(amount))
    except:
        await ctx.respond(f'Invalid Input Dumbass')
        raise ValueError
    if withdrawl == False:
        await ctx.respond(f'Not enough chips in bank to withdrawl that amount')
    else:
        bank.saveMemberData(ctx.author.id, memberData)
        await ctx.respond(f'Withdrawled {amount} chips from your bank')

'''Owner commands'''
@gamblebot.command()
@commands.is_owner()
async def admingift(ctx, target:discord.Member, amount):
    if target.id == gamblebot.user.id:
        await ctx.respond("Can't send Chips to the bot you silly billy")
        return
    else:
        memberData = bank.loadMemberData(target.id)
        try:
            memberData.chips += int(amount)
            bank.saveMemberData(target.id, memberData)
            await ctx.respond(f'Sent {amount} Coinage')
        except:
            await ctx.respond('Invalid Amount')

@gamblebot.command()
@commands.is_owner()
async def sleep(ctx):
    await ctx.bot.logout()

if __name__ == "__main__":
    asyncio.run(main())