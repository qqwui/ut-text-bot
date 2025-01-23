from typing import Set
import dis
import os

import discord
from dotenv import load_dotenv
from urllib.parse import quote


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
base_url="https://www.demirramon.com/gen/undertale_text_box"

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
    file_url = base_url + (".gif" if animated else ".png")
    query_str = f"text={quote(text)}&character={quote(character)}&expression={quote(expression)}&size=2"

    print(f"Username: {inter.user.name}, UserID: {inter.user.id}, Time: {inter.created_at.isoformat(timespec="seconds")}, text: {text}, character: {character if character else "none"}, expression: {expression}")

    await inter.response.send_message(f"{file_url}?{query_str}")

@bot.tree.command(name="randtext", description="Generates a random textbox")
async def randtext(inter: discord.Interaction, animated: bool = False) -> None:
    file_url = base_url + (".gif" if animated else ".png")
    query_str = "random&size=2"

    print(f"Username: {inter.user.name}, UserID: {inter.user.id}, Time: {inter.created_at.isoformat(timespec="seconds")}, Random Textbox")
    await inter.response.send_message(f"{file_url}?{query_str}")

@bot.tree.command()
async def test(inter: discord.Interaction) -> None:
    myembed = discord.Embed()
    myembed.set_image(url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASEAAABMCAYAAAAiAAErAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEd0lEQVR4nO3d0ZLbIAxA0bjT//9l98lTwgACLCFB7nnqNllMsC0wBO113/f9AQAnf7wrAOC3EYQAuPqb/nBdl1c9APyQdBaIkRAAVwQhAK4IQgBcEYQAuCIIAXBFEALgiiAEwBVBCIArghAAVwQhAK4IQgBc/ZXfgs/n/14X9tf5Sfcb9Z4HjfO247nPM/RErjsjIcF9318nNP85ksh1e+vUz2Wh1FaR248gJCj1IJF7ldNd1zXU/qPvP0n+2aMGIh7HDKXD+Nq/S+/PX5N+N7+4Rh8fpKH7SL1myhmpW/7ZajdW/vpoXd7csLX27LkGWnXrvZ7yMmvnJ4rlQehNY3j0aKWL/r5v9bqUbrbWjaNVB+l8jNbrTTmrSHXRDEDSe6Rja7RT9DmtZUFIIxLP9KRvlXoVbfnnarVV6XWp1+/R6pGlUYdUv5ly8nr1fLaeHl+qS89Is4d0DrTbqcTjfplhPidkNVkaeXiZ63lUqf3fyOsz8hHemzJ6WJ239FFk9lFPsx6t9tQa2fSWGTkAfT6GQWjFSs1Oq0FavZuF9Ma1rF/a03vfGJZ1WdGePeVHaOceJo9jq280z/mFltEJQY8ANTqHoTkPFeGc9Uxcz5SnUafP57tes9dThHZuUR8JefX0EUcYj3zVYsU806z8oq+9Nlvm27LekuqiPXoY/TpBz+9K19NurvSPH1o8q662+wkBfoHJX9uIEIAA7IdvTANwdVwQYkQG7EVldUxaJhz9HctyAMRiNhKSVhl6J5C1ygEQk0kQGgkwK8oBEJd6EIr0/Q8A8S3ZwKr1zU3Pb4DOHHs2pYbm54vyrdmRfVRSahGc5bjVMYsUG3nqBY3dzTtPqFvWv1Tuzm0FmcpIKN3TUtrH1buy1ZPGosZyo+BszxyhB49Qh1TvOYy84Re6zDawjl786T6YVkCrHS8tI4rR3DUWjya1OrTy9Ej5implj9Sn9Xut/Ws4j9rjWGkX8spUHlYXaynlw6reOequeotjRe1IYE91JNTKFtd6X+nxLR8NeQ3LNXe8j2QJ1DrmrNZu85mAMZoqwyohGOJZOjH9jCZGA8oTiDzmhDxpZD3c4Zi5E88l6syDUD7X8CZZ1C9enB6PgRbHHCnnOf4umQHxjurj2KpsdLXRVNQMi7NWpFr1PGbPRHzt/cwhncN0JHRK5rcoNNpxdtVS+7gjc22MiM5mklkxHco/oxat4b00wcnF+n0eGDEgovS+NU90nwcgjUDnuVoGQNeS1bHSsn26BN/z8/NvApCMbxtjJ8uW6DVGQW+2dfwy2gWRqQYh6WLX2PiJPixxYxeqE9MPKVjMHMeiTAA+zCempccmzRENwQfYm1lSM+vJUYIPcAbzzIqtFBFvywOwvyXpXR8EEAC549K7AtgLQQiAK4IQAFcEIQCuCEIAXBGEALgiCAFwRRAC4IogBMAVQQiAK4IQAFcEIQCuCEIAXBGEALgiCAFwRRAC4IogBMAVQQiAK4IQAFcEIQCuvhLd8xdOAazGSAiAK4IQAFf/AHRbDdalm+MLAAAAAElFTkSuQmCC")

    await inter.response.send_message(embed=myembed)

@bot.tree.command(name="credits", description="View credits for the bot")
async def credits(inter: discord.Interaction) -> None:
    await inter.response.send_message(
"""Made by @qqwui, DM them if there's any issues! You can view the source on [Github](https://github.com/qqwui/ut-text-bot).
This bot uses Demirramon's [undertale textbox generator](https://www.demirramon.com/generators/undertale_text_box_generator). Thanks so much for the developer interface!""", ephemeral=True, suppress_embeds=True)

bot.run(TOKEN)
