import discord
import random

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
client = discord.Client(intents=intents)


prefix = "!"
starting_balance = 100


# Resources and their values
resources = {
    'BTC': 50,
    'ETH': 20,
    'BNB': 10,
    'SOL': 5,
    'PI': -2,  # Negative value means it costs to remove trash
}

# Tools and their prices and multipliers
tools = {
    'cpu_miner': {'price': 200, 'multiplier': 1.5},
    'gpu_miner': {'price': 500, 'multiplier': 2.0},
    'asic_miner': {'price': 1000, 'multiplier': 3.0},
}

# Data store for players and their inventories
players = {}



@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(prefix):
        args = message.content[len(prefix):].split()
        command = args[0].lower()

        if command == 'start':
            await start_game(message)
        elif command == 'mine':
            await mine_resource(message)
        elif command == 'tools':
            await show_tools(message)
        elif command == 'buy':
            await buy_tool(message, args[1].lower())
        elif command == 'inventory':
            await show_inventory(message)
        elif command == 'help':
            await show_help(message)
        elif command == 'balance':
            await show_balance(message)
        elif command == 'rules':
            await show_rules(message) 
        elif command == 'beg':
            await ask_beg(message)  
        else:
            await message.channel.send('Invalid command. Type `!help` to see available commands.')


async def start_game(message):
    if message.author.id not in players:
        players[message.author.id] = {
            'balance': starting_balance,
            'inventory': {resource: 0 for resource in resources},
            'current_tool': 'papermining',
        }
        await message.channel.send(
            f'Welcome to the virtual mining game, {message.author.mention}! You have {starting_balance} coins in your wallet.'
        )
    else:
        await message.channel.send('You have already started the game!')

async def mine_resource(message):
    if message.author.id not in players:
        await message.channel.send('You need to start the game first using `!start` command.')
        return

    player = players[message.author.id]
    current_tool = player['current_tool']
    tool_multiplier = tools[current_tool]['multiplier'] if current_tool in tools else 1

    resource = random.choice(list(resources.keys()))
    amount_mined = int(resources[resource] * tool_multiplier)

    player['inventory'][resource] += amount_mined
    player['balance'] += amount_mined

    await message.channel.send(
        f'{message.author.mention} mined {amount_mined} {resource} using a {current_tool}! You now have {player["balance"]} coins.'
    )

async def show_balance(message):    
    await message.channel.send(f'{message.author.mention} has {players[message.author.id]["balance"]} coins.')


async def show_tools(message):
    tool_list = [f'{tool} - Price: {tools[tool]["price"]} coins' for tool in tools]
    await message.channel.send('Available tools:\n' + '\n'.join(tool_list))

async def buy_tool(message, tool):
    if message.author.id not in players:
        await message.channel.send('You need to start the game first using `!start` command.')
        return

    player = players[message.author.id]

    if tool not in tools:
        await message.channel.send('Invalid tool name. Use `!tools` to see available tools.')
        return

    tool_price = tools[tool]['price']
    if player['balance'] < tool_price:
        await message.channel.send('Insufficient balance to purchase this tool.')
        return

    player['balance'] -= tool_price
    player['current_tool'] = tool

    await message.channel.send(
        f'{message.author.mention} purchased a {tool} for {tool_price} coins. You now have {player["balance"]} coins.'
    )


async def show_inventory(message):
    if message.author.id not in players:
        await message.channel.send('You need to start the game first using `!start` command.')
        return

    player = players[message.author.id]
    inventory_list = [f'{resource}: {player["inventory"][resource]}' for resource in resources]
    await message.channel.send('Your inventory:\n' + '\n'.join(inventory_list))

async def show_help(message):
    await message.channel.send('Type `!rules` to see available commands.'  '\n' + 'Type `!start` to start the game.' '\n' + 'Type `!mine` to mine resources.' '\n' + 'Type `!tools` to see available tools.' '\n' + 'Type `!buy` to buy a tool.' '\n' + 'Type `!inventory` to see your inventory.' '\n' + 'Type `!balance` to see your balance.')

async def show_rules(message):
    await message.channel.send('1. You can only mine with 1 tool at a time.' '\n' + '2.  Buying Better Mining Tool will increase your mining speed.' '\n' + '3.  Bot is under Beta Testing Only.' '\n' + '4.  Planning to Implement In-Game Coins >> Blockchain Token.')



# Command: beg
async def ask_beg(message):
    if message.author.id not in players:
        await message.channel.send('You need to start the game first using `!start` command.')
        return

    player = players[message.author.id]
    beg_amount = random.randint(1, 5)

    player['balance'] += beg_amount
    await message.channel.send(
        f'{message.author.mention} begged and received {beg_amount} coins. You now have {player["balance"]} coins.'
    )



# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token
client.run('BOT_TOKEN')
