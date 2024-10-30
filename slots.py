'''The slot machine, used to run all the slots game and deal out winnings'''
import bank
import random

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



    