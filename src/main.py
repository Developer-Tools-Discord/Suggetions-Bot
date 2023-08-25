import discord
from discord import Embed
import os
from pymongo.mongo_client import MongoClient
from colorama import Fore
import json

with open('config.json', "r") as f:
    config = json.load(f)

# THIS IS VERY IMPORTANT SECTION PLEASE DON'T Forget Make Mongo_url !!!!!
uri = config['mongo_url']

client = MongoClient(uri)
db = client['Database']
colliction = db['suggestions']

try:
    client.admin.command('ping')
    print(f"{Fore.CYAN}Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{Fore.LIGHTBLACK_EX}=================================================")
    print(f"{Fore.GREEN}[✅] {bot.user} Connected with MongoDB")
    print(f"{Fore.GREEN}[✅] {bot.user} System ran without errors")
    print(f"{Fore.GREEN}[✅] {bot.user} Ready to use!{Fore.RESET} ")
    print(f"{Fore.YELLOW}Made By devM7MD")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Suggestions Bot | /help"))

@bot.slash_command(name="setup-suggestions")
@discord.option(name="channel", description="the channel you need to make it for suggestions")
async def setup_sugg(interaction:discord.Interaction, channel:discord.TextChannel):
    check = colliction.find_one({"_id":channel.id})
    if check:
        await interaction.response.send_message(content="**This channel is already in the database :x:**")
    if not check:
        dic = {
            "_id":channel.id,
            "GUILD_ID":channel.guild.id
        }
        colliction.insert_one(dic)
        await interaction.response.send_message(content=f"**The {channel.mention} channel now it's the one of suggetions channels :white_check_mark:**")

@bot.event
async def on_message(message:discord.Message):
    if message.author.bot: return
    channel_id = message.channel.id
    check = colliction.find_one({"_id":channel_id})
    if check:
        msg = message.content
        await message.delete()
        # Protecting From Links if your guild don't have an anti-links
        if msg.find('https://') or msg.find("http://"): return
        # Create the embed of the suggest
        embed = Embed(
            title=f"Suggest From {message.author.name}",
            color=discord.Color.random(),
            description=msg
        )
        embed.set_thumbnail(url=message.author.avatar.url)
        embed.set_footer(text=f"Requested By {message.author.name}")
        botmsg = await message.channel.send(embeds=[embed])
        # Adding Reacations to the bot message
        await botmsg.add_reaction("✅")
        await botmsg.add_reaction("❌")
    if not check : return

bot.run(os.environ['token'], reconnect=True) # Don't Forget Change The token here
