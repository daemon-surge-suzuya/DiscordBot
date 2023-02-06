#THIS IS A MULTIPLE PURPOSE DISCORD BOT THAT CAN DO MANY THINGS YOU NEED TO DO IN A COMMUNITY SERVER
#THIS BOT IS CREATED BY DAEMON_SURGE_SUZUYA. 
#DISCORD ID = Daemon Surge Suzuya#1715



import discord
from discord.ext import commands
import openai
import requests
import wikipedia
import socket
import time
import wolframalpha

openai.api_key = "<OpenAiToken>"
model="text-davinci-002"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def kick(ctx, member: discord.Member):
    if ctx.message.author.name + "#" + ctx.message.author.discriminator == "YourUserName#Number":
        await member.kick()
        await ctx.send(f"{member} has been kicked by {ctx.message.author}")
    else:
        await ctx.send("You do not have the permission to use this command.")

@bot.command()
async def ban(ctx, member: discord.Member):
    if ctx.message.author.name + "#" + ctx.message.author.discriminator == "YourUserName#Number":
        await member.ban()
        await ctx.send(f"{member} has been banned by {ctx.message.author}")
    else:
        await ctx.send("You do not have the permission to use this command.")

@bot.command()
async def gpt(ctx,*,arg):
    if arg.lower() == "who made you":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    if arg.lower() == "who made you?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    if arg.lower() == "who created you":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    elif arg.lower() == "who created you?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    elif arg.lower() == "Where were you created?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon Surge Suzuya created me with his own hands!")
    elif arg.lower() == "Who created you?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    elif arg.lower() == "WHO CREATED YOU?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon_Surge_Suzuya created me!")
    elif arg.lower() == "who is daemon?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon Surge Suzuya is a child, But he is a developer, game developer, web developer too!")
    elif arg.lower() == "Who is daemon surge?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon Surge Suzuya is a child, But he is a developer, game developer, web developer too!")
    elif arg.lower() == "Who is daemon surge suzuya?":
        await ctx.channel.send(f"{ctx.author.mention}, Daemon Surge Suzuya is a child, But he is a developer, game developer, web developer too!")
    else:
        query = ctx.message.content
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.5,
            max_tokens=1500,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        await ctx.channel.send(f"{ctx.message.author.mention} " + response['choices'][0]['text'].replace(str(query), ""))

@bot.command()
async def news(ctx):
    # Make a GET request to the news API
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=<API KEY>")
    data = response.json()

    # Get the first 5 articles from the response
    articles = data["articles"][:3]

    # Send a message to the server with the news headlines
    for article in articles:
        await ctx.send(article["title"] + "\n" + article["url"])

@bot.command()
async def search(ctx, *, query):
# Get the wikipedia page for the query
    page = wikipedia.summary(query, sentences=1)
# Check if the page exists
    if page:
# Send the page summary to the user who called the command
        await ctx.send(f"{ctx.author.mention}, here is the result for '{query}': {page}")
    else:
# If the page does not exist, send a message to the user
        await ctx.send(f"{ctx.author.mention}, No results found for '{query}'.")

@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Pinging...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content=f"Pong! Latency: {duration:.2f}ms")

@bot.command()
async def ticket1(ctx, *, reason: str):
    if reason:
        ticket_channel = await ctx.guild.create_text_channel(f'Ticket - {reason}')
        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
        daemon_surge_suzuya = ctx.guild.get_member(725251269369520109)
        if daemon_surge_suzuya:
            if ctx.message.author.name + "#" + ctx.message.author.discriminator == "YourUserName#Number":
                for role in ctx.guild.roles:
                    if role.permissions.administrator or role.permissions.manage_guild:
                        permissions = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                        await ticket_channel.set_permissions(role, overwrite=permissions)
                        await ticket_channel.send(f'Ticket opened by {ctx.author.mention} with reason: {reason}')
            else:
                await ticket_channel.set_permissions(daemon_surge_suzuya, read_messages=True, send_messages=True)
                await ticket_channel.send(f'Ticket opened by {ctx.author.mention} with reason: {reason}')
        await ctx.message.delete()
        await ctx.author.send(f'Your ticket has been created and can be found in {ticket_channel.mention}')
    else:
        await ctx.send('Please specify the reason for your ticket with `!ticket <reason>`')
        
@bot.command(name='ticket_close')
async def ticket_close(ctx):
    if ctx.channel.name.startswith('ticket-'):
        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_channels or (ctx.message.author.name + "#" + ctx.message.author.discriminator == "Daemon Surge Suzuya#1715"):
            await ctx.channel.delete()
        else:
            await ctx.send('Only the owner or a mod can close this ticket.')
    else:
        await ctx.send('This command can only be used in a ticket channel.')

# Wolfram Alpha API setup
app_id = "<WOLFRAM API>"
client_wolfram = wolframalpha.Client(app_id)

@bot.command()
async def solve(ctx, *, query: str):
	res = client_wolfram.query(query)
	try:
		answer = next(res.results).text
	except StopIteration:
		await ctx.send(f"{ctx.message.author.mention}: No results found for the query.")
		return
	await ctx.send(f"{ctx.message.author.mention}: {answer}")


    
if __name__ == "__main__":
    bot.run("TOKEN")
