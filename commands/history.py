import discord
from functions import match_history
from lib.errors import CommandError
import utils
import cfg
import random
import lib.vrml as vrml
import logging

from commands.base import Cmd

log = logging.getLogger(__name__)

help_text = """Get a history of matches in the current season for a team.
If no team is specified, the default team is used. This can be changed via \
the settings command.

Usage:
```<PREFIX><COMMAND> [team_name]```\

Examples:
```<PREFIX><COMMAND>
<PREFIX><COMMAND> Team Gravity
<PREFIX><COMMAND> blank```
"""


async def execute(ctx, params):
    r = await ctx["channel"].send(utils.get_loading_msg())

    if not params:
        team_name = ctx['settings']['team_name']
        if team_name is None:
            await r.delete()
            log.error("No team name given and no default value is set.")
            raise CommandError("No team specified and no default team set. This can be changed in the settings.")
        log.debug("Default team name used.")
    else:
        team_name = ctx['params_str']
    
    
    seasons = await vrml.seasons("EchoArena")
    current_season = seasons[-1]    # get latest season

    p_teams: list[vrml.PartialTeam] = await vrml.search_team("EchoArena", team_name, season=current_season.id)
    if not p_teams:
        log.error(f"No teams were found under the name {team_name}.")
        await r.edit(content="No teams were found by that name.")
        return
    elif len(p_teams) > 1:
        if any(i.name == team_name for i in p_teams):
            p_team = next(team for team in p_teams if team.name == team_name)
        else:
            log.warning(f"Multiple Teams were found under the name {team_name}.")
            await r.edit(content="The team search term is not unambiguous. Please specify the exact team.\n" \
                + f"Found Teams: {', '.join(team.name for team in p_teams)}")
            return
    else:
        p_team = p_teams[0]
    
    team = await p_team.fetch()
    history = await team.matches_history()

    embed = discord.Embed(title="Match History", description=current_season.name)
    embed.set_author(
        name = team.name, 
        url = f"https://vrmasterleague.com/EchoArena/Teams/{team.id}",
        icon_url = team.division_logo_url
    ) 
    embed.set_thumbnail(url=team.logo_url)

    footer_lines = []
    for match in history:
        if match.season_name != current_season.name:
            continue
        line = [match.scheduled_date.date().isoformat()+":"]
        if match.home_team.name == team.name:
            # found team is home team
            line.append(match.home_team.name)
            line.append(f"{match.home_team_score} - {match.away_team_score}")
            line.append(match.away_team.name)
            # insert win/lose indicator
            if match.winning_team_id == match.home_team.id:
                line.insert(0, "✅")
            else:
                line.insert(0, "❌")
        else:
            # found team is away team
            line.append(match.away_team.name)
            line.append(f"{match.away_team_score} - {match.home_team_score}")
            line.append(match.home_team.name)
            # insert win/lose indicator
            if match.winning_team_id == match.away_team.id:
                line.insert(0, "✅")
            else:
                line.insert(0, "❌")
        footer_lines.append("  ".join(line))
    
    embed.set_footer(text="\n".join(footer_lines))

    await r.edit(content="", embed=embed)

    return



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=False
)