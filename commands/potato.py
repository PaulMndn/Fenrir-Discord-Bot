import aiohttp
import random
import json
import discord
import logging
from lib.errors import CommandError
import utils

from cfg import CONFIG
from commands.base import Cmd

log = logging.getLogger(__name__)


help_text = """I will get you a random potato recipe.

USAGE:
```<PREFIX><COMMAND>```"""

RECIPE_COUNT = 1
BASE_URL = "https://api.spoonacular.com"

async def execute(ctx, pararms):
    global RECIPE_COUNT

    channel = ctx['channel']
    msg = await channel.send(utils.get_loading_msg())

    api_key = CONFIG['spoonacular_api_key']

    for i in range(3):
        async with aiohttp.ClientSession() as session:
            search_params = {
                "apiKey":api_key,
                "query":"potato",
                "number":"1"
            }
            search_params['offset'] = str(random.randint(0,RECIPE_COUNT-1))

            async with session.get(BASE_URL+"/recipes/complexSearch",params=search_params) as r:
                if r.status != 200:
                    log.error(f"Bad API response on recipe search. Status: {r.status}, response: {await r.text(encoding='utf-8')}.")
                    raise CommandError("Bad API response. Please try again later.\n" \
                        "if this issue persists, please contact the bot developer.")
                data = json.loads(await r.text(encoding="utf-8"))
                RECIPE_COUNT = int(data['totalResults'])
                recipe = data['results'][0]
                title = recipe['title']
                id = recipe['id']
                img = recipe['image']
            
            info_params={
                "apiKey": api_key,
                "includeNutrition": "false"
            }
            async with session.get(BASE_URL+f"/recipes/{id}/information", params=info_params) as r:
                if r.status != 200:
                    log.error(f"Bad API response on recipe information. " \
                        + f"Status: {r.status}, response: {await r.text(encoding='utf-8')}.")
                    raise CommandError("Bad API response. Please try again later.\n" \
                        + "If this issue persist, please contact the bot developer.")
                data = json.loads(await r.text(encoding="utf-8"))

                ingredients = ["**INGREDIENTS**"]
                for i in data['extendedIngredients']:
                    amount_float = i['measures']['metric']['amount']
                    amount_int = int(amount_float)
                    amount = amount_int if amount_int == amount_float else amount_float

                    line = f"{round(amount, 2)} {i['measures']['metric']['unitShort']} {i['originalName']}"
                    ingredients.append(line)
                ingredients_text = "\n".join(ingredients)

                instructions = data['analyzedInstructions']

                try:
                    main_instructions = instructions[0]
                except IndexError:
                    # no instructions available
                    continue
                main_steps = [d['step'] for d in main_instructions['steps'] if "step" in d]
                main_steps_text = "\n".join(["**INSTRUCTIONS**"] + main_steps)

                sourceUrl = json.loads(await r.text(encoding="utf-8"))['sourceUrl']

                embed = discord.Embed(
                    title = title, 
                    description = "\n\n".join([ingredients_text,main_steps_text]),
                    url = sourceUrl
                )
                embed.set_thumbnail(url=img)

                if len(instructions) > 1:
                    # sub recipe/instructions exist --> add as fields
                    for i in range(1,len(instructions)):
                        sub_instructions = instructions[i]
                        sub_steps = [d['step'] for d in sub_instructions['steps'] if "step" in d]
                        sub_steps_text = "\n".join(sub_steps)
                        embed.add_field(
                            name=sub_instructions['name'],
                            value=sub_steps_text,
                            inline=False
                        )
            
            card_params = {
                "apiKey":api_key,
                "mask": "ellipseMask",
                "backgroundImage":"background1",
                "backgroundColor": "ffffff",
                "fontColor": "333333"
            }
            async with session.get(BASE_URL+f"/recipes/{id}/card", params=card_params) as r:
                log.debug(f"Looking for recipe card.")
                if r.status == 200:
                    data = json.loads(await r.text(encoding="utf-8"))
                    if data['status'] == "success":
                        embed.set_image(url=data['url'])
                        log.info(f"Recipe card added to discord embed. URL = {data['url']}")
        
        
        await msg.edit(content="", embed=embed)

        return

    # ran out of tries
    raise CommandError("Unknkown error occured. Please try again later.")




command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=False
)