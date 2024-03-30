import discord
import requests
import os  # To load your API key from an environment variable
from dotenv import load_dotenv  # To load your API key from a .env file

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') 
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') # Store your keys safely
BOT_PREFIX = os.getenv('BOT_PREFIX')  # Customize the bot's prefix
client = discord.Client(intents=discord.Intents.all())  # Enable all intents

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:  # Prevent the bot from responding to itself
        return
    
    #command with prefix
    if message.startswith(BOT_PREFIX):
        command = message.content[len(BOT_PREFIX):].strip()
        if command == "ask":
            prompt = message.content[len(BOT_PREFIX + "ask"):].strip()
            response = call_gemini_api(prompt)
            await message.channel.send(response)
            
    #respond to mentions
    elif client.user in message.mentions:
        prompt = message.content.split(">")[1].strip()
        response = call_gemini_api(prompt)
        await message.channel.send(response)
    

def call_gemini_api(prompt):
    url = "https://api.gemini.google.com/v1/documents/text:create"  # Adjust the endpoint if needed
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    data = {
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["document"]  # Extract the response text
    else:
        return "Sorry, I had trouble getting a response from Gemini."

client.run(DISCORD_BOT_TOKEN) 
