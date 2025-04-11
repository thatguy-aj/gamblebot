import bank
import random
import discord
from discord.ext import commands

#TODO Rewrite the slots.py file and slot commands into this cog file

symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "🍀"]

def get_next_previous(symbol):
    """Return the next and previous symbols for the given symbol."""
    index = symbols.index(symbol)
    prev_symbol = symbols[index - 1] if index > 0 else symbols[-1]  # Wrap around to the last symbol
    next_symbol = symbols[index + 1] if index < len(symbols) - 1 else symbols[0]  # Wrap around to the first symbol
    return prev_symbol, next_symbol

def speen(slots):
    wheel_results = random.choices(symbols, weights= [50, 35, 25, 20, 10, 5], k=slots)
    prev_next_info = [get_next_previous(result) for result in wheel_results]
    next_symbols = [prev_next_info[i][1] for i in range(slots)]
    prev_symbols = [prev_next_info[i][0] for i in range(slots)]
    return wheel_results, next_symbols, prev_symbols

class SlotsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command()
    async def slotcombos(self, ctx):
        ComboSheet = discord.Embed(title='Combo Sheet', color=discord.Colour.purple())
        ComboSheet.add_field(name='**Combos**', value='🍒🍒 = 2x\n🍒🍒🍒 = 3x\n🍋🍋🍋 = 5x\n🍇🍇🍇 = 10x\n🔔🔔🔔 = 25x\n🍀🍀🍀 = 50x')
        await ctx.respond(embed=ComboSheet)

    @discord.slash_command()
    async def slotmachine(self, ctx, chips):
        try:
            intchips = int(chips)
        except ValueError:
            try:
                round(float(chips))
            except:
                await ctx.respond(f'{chips} is an invalid input, please try again')
                return
        if intchips <= 0:
            await ctx.respond('Bet cannot be lower or equal to 0')
            return
        
        # Loads member's bank data
        memberData = bank.loadMemberData(ctx.author.id)
        if memberData.value["chips"] < intchips:
            await ctx.respond('You do not have enough chips to bet that amount, broke ass :P')
            return
        memberData.value["chips"] -= intchips

        # Spins slot wheels, and returns results
        slot_results, next_results, prev_results = speen(3)
        
        # Calculates winnings
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
        player_winnings = intchips * winnings
        memberData.value["chips"] += player_winnings
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
        SlotMachine.add_field(name='Results', value=f'=={next_results_combined}==\n**>>{slot_results_combined}<<**\n=={prev_results_combined}==\n\n{win_message}\nCurrent Balance: {memberData.value["chips"]}')
        await ctx.respond(embed=SlotMachine)

