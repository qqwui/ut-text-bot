import os

import discord
from dotenv import load_dotenv
from urllib.parse import quote


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
generator_baseurl="https://www.demirramon.com/gen/"


intents = discord.Intents.default()

bot = discord.Client(intents=discord.Intents.default())
bot.tree = discord.app_commands.CommandTree(bot)


async def setup_hook() -> None:  # This function is automatically called before the bot starts
    await bot.tree.sync()   # This function is used to sync the slash commands with Discord it is mandatory if you want to use slash commands

bot.setup_hook = setup_hook


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.tree.command(name="textbox", description="Generates a textbox")
@discord.app_commands.describe(text="The text to write", character="The character portrait to use", expression="The expression the character should have", animated="Whether the text should be animated")
async def textbox(inter: discord.Interaction, text: str, character: str = "", expression: str = "default", animated: bool = False) -> None:
    file_url = "https://www.demirramon.com/gen/undertale_text_box" + (".gif" if animated else ".png")
    query_str = f"text={quote(text)}&character={quote(character)}&expression={quote(expression)}&size=2"

    print(f"Username: {inter.user.name}, UserID: {inter.user.id}, Time: {inter.created_at.isoformat(timespec="seconds")}, text: {text}, character: {character if character else "none"}, expression: {expression}")

    await inter.response.send_message(f"{file_url}?{query_str}")

@bot.tree.command(name="credits", description="View credits for the bot")
async def credits(inter: discord.Interaction) -> None:
    await inter.response.send_message(
"""Made by @qqwui, DM them if there's any issues!
This bot uses Demirramon's [undertale textbox generator](https://www.demirramon.com/generators/undertale_text_box_generator). Thanks so much for the developer interface!""", ephemeral=True, suppress_embeds=True)

bot.run(TOKEN)
