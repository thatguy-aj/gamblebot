from imaplib import Commands
import discord
from discord.ext import commands
import logging
import os
import random
import time
import bank
import slots
from dotenv import load_dotenv

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
gamblebot = discord.Bot()


'''events'''
@gamblebot.event
async def on_ready():
    print(f'Logged in as {gamblebot.user}')

#@gamblebot.event (Make it so it DMs the user welcoming them to the server and telling them their current bank balance)


'''commands'''
@gamblebot.command(description="Gets the bot's ping")
async def ping(ctx):
    await ctx.respond(f'Pong! {gamblebot.latency} ms')

#TODO Re-write for a text file
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

'''Slot Machine commands'''
@gamblebot.command()
async def slotcombos(ctx):
    ComboSheet = discord.Embed(title='Combo Sheet', color=discord.Colour.purple())
    ComboSheet.add_field(name='**Combos**', value='🍒🍒 = 2x\n🍒🍒🍒 = 3x\n🍋🍋🍋 = 5x\n🍇🍇🍇 = 10x\n🔔🔔🔔 = 25x\n🍀🍀🍀 = 50x')
    await ctx.respond(embed=ComboSheet)

@gamblebot.command()
async def slotmachine(ctx, bet):
    int_bet = int(bet)
    memberData = bank.loadMemberData(ctx.author.id)
    memberData.chips -= int_bet

    if int_bet < 25 or int_bet > 200:
        await ctx.respond('Invalid Chip Amount: Min Bet: 25, Max Bet: 200')
        return 0
    slot_results, next_results, prev_results = slots.speen(3)
    '''Yandere dev ahhh code'''
    if slot_results == ['🍒','🍒','🍒']:
        winnings = 3
    elif slot_results[0:2] == ['🍒','🍒'] or slot_results[1:3] == ['🍒','🍒']:
        winnings = 2
    elif slot_results == ['🍋','🍋','🍋']:
        winnings == 5
    elif slot_results == ['🍇','🍇','🍇']:
        winnings == 10
    elif slot_results == ['🔔','🔔','🔔']:
        winnings = 25
    elif slot_results == ['🍀', '🍀', '🍀']:
        winnings = 50
    else:
        winnings = 0


    '''Adds winnings to the players chips'''
    player_winnings = int_bet * winnings
    memberData.chips += player_winnings
    bank.saveMemberData(ctx.author.id, memberData)

    if winnings == 0: #Did not win
        color_flair = discord.Color.brand_red()
        win_message = 'Sorry, better luck next time :('
    elif winnings == 50: #Jackpot
        color_flair = discord.Color.yellow()
        win_message = f'WOWZA, {ctx.author.mention} JUST GOT THE JACKPOT AND WON {player_winnings} CHIPS!!!'
    else: #Won
        color_flair = discord.Color.brand_green()
        win_message = f'Congrats, you won {player_winnings} Chips!'

    next_results_combined = " | ".join(next_results)
    prev_results_combined = " | ".join(prev_results)
    slot_results_combined = " | ".join(slot_results)
    
    SlotMachine = discord.Embed(title='Spinny Bob\'s Slot Machine',description='Only losers do drugs' ,color=color_flair)
    SlotMachine.add_field(name='Results', value=f'=={next_results_combined}==\n**>>{slot_results_combined}<<**\n=={prev_results_combined}==\n\n{win_message}\nCurrent Balance: {memberData.chips}')


'''Owner commands'''
@gamblebot.command()
@commands.is_owner()
async def admingift(ctx, target:discord.Member):
    memberData = bank.loadMemberData(target.id)
    

gamblebot.run(TOKEN)