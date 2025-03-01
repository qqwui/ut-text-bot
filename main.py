import os
import io
import requests
import discord
from sys import stderr
from urllib.parse import quote

TOKEN = os.getenv('DISCORD_TOKEN')
base_url="https://www.demirramon.com/gen/"

intents = discord.Intents.default()

bot = discord.Client(intents=discord.Intents.default())
bot.tree = discord.app_commands.CommandTree(bot)

async def setup_hook() -> None:
    await bot.tree.sync()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!', file=stderr)

@bot.tree.command(name="textbox", description="Generates a textbox")
@discord.app_commands.describe(
    text="The text to write", character="The character portrait to use",
    expression="The expression the character should have",
    animated="Whether the text should be animated"
)
async def textbox(inter: discord.Interaction, text: str, character: str = "", expression: str = "default", animated: bool = False) -> None:
    await inter.response.defer()

    file_url = "undertale_text_box" + (".gif" if animated else ".png")
    query_str = f"text={quote(text)}&character={quote(character)}&expression={quote(expression)}&size=2"

    print(f"Username: {inter.user.name}, UserID: {inter.user.id}, Time: {inter.created_at.strftime('%Y-%m-%d %H:%M:%S')}, text: {text}, character: {character if character else 'none'}, expression: {expression}", file=stderr)

    image_request = requests.get(f"{base_url}{file_url}?{query_str}")

    if image_request.status_code == 200:
        # assume the image was sucessfully gotten ig
        myattachment = discord.File(io.BytesIO(image_request.content), filename=file_url)
        await inter.followup.send(file=myattachment)
    else:
        print(f"Get {file_url}?{query_str} failed with error {image_request.status_code}", file=stderr)
        await inter.followup.send("Request image failed", ephemeral=True)

    image_request.close()

@bot.tree.command(name="randtext", description="Generates a random textbox")
@discord.app_commands.describe(animated="Whether the text should be animated")
async def randtext(inter: discord.Interaction, animated: bool = False) -> None:
    await inter.response.defer()

    file_url =  "undertale_text_box" + (".gif" if animated else ".png")
    query_str = "random&size=2"

    print(f"Username: {inter.user.name}, UserID: {inter.user.id}, Time: {inter.created_at.strftime('%Y-%m-%d %H:%M:%S')}, Random Textbox", file=stderr)

    image_request = requests.get(f"{base_url}{file_url}?{query_str}")

    if image_request.status_code == 200:
        myattachment = discord.File(io.BytesIO(image_request.content), filename=file_url)
        await inter.followup.send(file=myattachment)
    else:
        print(f"Get {file_url}?{query_str} failed with error {image_request.status_code}", file=stderr)
        await inter.followup.send("Request image failed", ephemeral=True)

    image_request.close()

@bot.tree.command(name="credits", description="View credits for the bot")
async def credits(inter: discord.Interaction) -> None:
    await inter.response.send_message(
        """Made by @qqwui, DM them if there's any issues! You can view the source on [Github](https://github.com/qqwui/ut-text-bot).
This bot uses Demirramon's [undertale textbox generator](https://www.demirramon.com/generators/undertale_text_box_generator). Thanks so much for the developer interface!""",
    ephemeral=True, suppress_embeds=True
    )

bot.run(TOKEN)
