import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user.name}'.format(bot))
    quote_of_the_day.start()

async def create_channel(guild):
    print('no channel found // creating channel...')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(send_messages=True)
    }
    await guild.create_text_channel('out-of-context-quotes', overwrites=overwrites)


@tasks.loop(hours=24)
async def quote_of_the_day():
    for guild in bot.guilds:
        generalChannel = discord.utils.get(guild.channels, name='general')
        quoteChannel = discord.utils.get(guild.channels, name='out-of-context-quotes')
        if(quoteChannel == None):
            create_channel(guild)
            return

        quotes = await quoteChannel.history(limit=None).flatten()
        message = random.choice(quotes)
        responseContent = message.content
        time = message.created_at
        time = time.strftime("On %A, %B %d, %Y at %I:%M%p ")
        response = '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\nQUOTE OF THE DAY:\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{0}{1}'.format(time, responseContent)
        await generalChannel.send(response)

@bot.command(name='quote', help='TTS an out of context quote // Optional argument to search for a quote with given keyword')
async def reciteQuote(ctx, name=None):

    quoteChannel = discord.utils.get(ctx.guild.channels, name='out-of-context-quotes')
    if(quoteChannel == None):
        create_channel(ctx.guild)
        return

    quotes = await quoteChannel.history(limit=None).flatten()
    if not name:
        message = random.choice(quotes)
    else:
        newquotes = []
        for msg in quotes:
            if name.upper() in msg.content.upper():
                newquotes.append(msg)
        try:
            message = random.choice(newquotes)
        except:
            await ctx.send('There are no matching quotes!')
            return
    responseContent = message.content
    time = message.created_at
    time = time.strftime("On %A, %B %d, %Y at %I:%M%p ")
    response = time + responseContent
    await ctx.send(response, tts=True)

@bot.command(name='addQuote', help='Add an out of context quote // format: <author> <quote>')
async def addQuote(ctx, quote_author, *, quote):
    quoteChannel = discord.utils.get(ctx.guild.channels, name='out-of-context-quotes')
    if(quoteChannel == None):
        create_channel(ctx.guild)
        return

    response = '{0} said: "{1}"'.format(quote_author.capitalize(), quote)
    await quoteChannel.send(response)

bot.run(TOKEN)
