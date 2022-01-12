import logging
from urllib.parse import quote as _uriquote
import aiohttp
import json
import asyncio
import time
import datetime as dt

log = logging.getLogger(__name__)

VRML_URL = "https://vrmasterleague.com"

class Route:
    BASE = 'https://api.vrmasterleague.com'

    def __init__(self, method, path, **parameters):
        self.method = method
        self.path = path
        
        url = (self.BASE + self.path)
        if parameters:
            self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k,v in parameters.items()})
        else:
            self.url = url

async def request(route, **kwargs):
    method = route.method
    url = route.url

    async with aiohttp.ClientSession() as session:
        for tries in range(5):
            async with session.request(method, url, **kwargs) as r:
                data = json.loads(await r.text(encoding="utf-8"))

                # request successfull, return json data
                if r.status == 200:
                    log.debug("%s %s has returned %s", method, url, r.status)
                    return data
                
                # rate limited, wait and try again if tries left
                if r.status == 429:
                    wait_time = float(r.headers['X-RateLimit-Reset-After'])
                    log.warning("We're being rate limited. Retry in %.3f seconds.", wait_time)
                    
                    if r.headers['X-RateLimit-Global'] == 'True':
                        log.warning("Rate limit is global. %s", r.headers['X-RateLimit-Global'])
                    
                    await asyncio.sleep(wait_time)
                    log.debug("Done waiting for rate limit. Retrying...")
                    
                    continue

        # ran out of retries
        raise Exception(f"{route.method} {route.url} with querry params {kwargs} ran out of retries.")


async def get_search_team(game: str, name: str, season: str = None, region: str = None):
    '''Gets the Teams having a name that contains the search criteria.

    Args:
        game (str): Game to search teams for. Examples: Onward, EchoArena, Pavlov, Snapshot.
        name (str): The search criteria.
        season (str, optional): The season id.
        region (str, optional): Team's region. Examples: NA, EU, OCE or none.

    Returns:
        list of dict with found teams. The dicts contain:
            {
                `id: (str) The Team id`
                `name: (str) The Team name`
                `image: (str) The Team logo URL`
            }
    '''
    params = {"name": name}
    if season is not None:
        params['season'] = season
    if region is not None:
        params['region'] = region
    return await request(Route("GET", "/{game}/Teams/Search", game=game), params=params)


async def get_team(team_id: str):
    '''Gets information on the specified Team.
    
    Args:
        team_id (str): The Team id
    
    Returns:
        dict with team data containing:
            {
                `"rankWorldwide": (int) The Team rank in the worldwide standings`
                `"rank": (int) The Team rank in their respective Region standings`
                `"division": (str) The Team division name`
                `"divisionLogo": (str) The Team division logo URL`
                `"gp": (int) The number of games played in the season`
                `"w": (int) The number of wins in the current season`
                `"t": (int) The number of ties in the current season`
                `"l": (int) The number of loses in the current season`
                `"pts": (int) The number of points total in the current season`
                `"mmr"?: (str, optional) For ladder Teams only. The rounded MMR or "TBD"`
                `"cycleGP"?: (int, optional) For master Teams only. The number of games played in the current cycle`
                `"cycleW"?: (int, optional) For master Teams only. The number of wins in the current cycle`
                `"cycleT"?: (int, optional) For master Teams only. The number of ties in the current cycle`
                `"cycleL"?: (int, optional) For master Teams only. The number of loses in the current cycle`
                `"cycleTieBreaker"?: (int, optional) For master Teams only. The tie breaker indicator (number of wins against tied Teams) in the current cycle`
                `"cyclePlusMinus"?: (int, optional) For master Teams only. The plus/minus points in the current cycle`
                `"cycleScoreTotal"?: (int, optional) For master Teams only. The total points in the current cycle`
                `"isRecruiting": (bool) Indicates if the Team is actively recruiting`
                `"id": (str) The Team id`
                `"name": (str) The Team name`
                `"logo": (str) The Team logo URL`
                `"regionID": (str) The Region id`
                `"region": (str) The Region name`
            }
    '''

    return await request(Route("GET", "/Teams/{team_id}", team_id=team_id))

async def get_team_matches_history(team_id):
    '''Gets the Matches history for the specified Team.
    Args:
        team.id (str): The Team id

    Returns:
        `list` of `dict`s with matches history containing:
            {
                `id: (str) The Match id`
                `seasonName: (str) The season name`
                `week: (int) The week number`
                `homeTeam: (dict) The home Team information`
                `awayTeam: (dict) The away Team information`
                `winningTeamID: (str) The winning Team 'team id'`
                `losingTeamID: (str) The losing Team 'team id'`
                `homeScore: (int) The score for the home Team`
                `awayScore: (int) The score for the away Team`
                `homeHighlights: (str) The submitted highlights by the home Team`
                `awayHighlights: (str) The submitted highlights by the away Team`
                `vodURL: (str | None) The URL for the VOD if any`
                `mapsSet: (dir) The maps set (aka rounds) for the Match`
                `dateScheduled: (str) The date and time (in UTC) the Match was scheduled`
            }
            
            /{homeTeam}
            /{awayTeam}
                {
                    `name: (str) The Team name`
                    `logo: (str) The Team logo URL`
                    `regionID: (str)	The Region id of the Team`
                    `region: (str) The Region name of the Team`
                }

            /[mapsSet]
                {
                    `mapNum: (int) The order of the map in the Match (or the round number)`
                    `mapName: (str) The name of the map`
                    `homeScore: (int) The home Team score on the map (or round)`
                    `awayScore: (int) The away Team score on the map (or round)`
                }
    '''
    return await request(Route("GET", "/Teams/{team_id}/Matches/History", team_id=team_id))


async def get_seasons(game):
    '''Gets the seasons for the specified game name in the URL.
    Args:
        game (str): Examples: Onward, EchoArena, Pavlov, Snapshot
        
    Returns:
        `list` of `dict`s with season information containing:
            {
                `id: (str) The season id`
                `name: (str) The season name`
            }
    '''
    return await request(Route("GET", "/{game}/Seasons", game = game))







###############################################################################
## Classes

class PartialTeam:
    def __init__(self, data):
        self._update(data)
    
    def _update(self, data: dict):
        self.id = data.pop('id', None)
        self.name = data.pop('name', None)
        self.logo_url = data.pop('logo', None)

    async def fetch(self):
        return Team(await get_team(self.id))



class Team:
    def __init__(self, data):
        self._update(data)

    def _update(self, data: dict):
        self.worldwide_rank = data.pop('rankWorldwide', None)
        self.rank = data.pop('rank', None)
        self.division = data.pop('division', None)
        self.division_logo_url = VRML_URL + data.pop('divisionLogo', None)
        self.games_played = data.pop('gp', None)
        self.wins = data.pop('w', None)
        self.ties = data.pop('t', None)
        self.loses = data.pop('l', None)
        self.points = data.pop('pts', None)
        self.cycle_games_played = data.pop('cycleGP', None)
        self.cycle_wins = data.pop('cycleW', None)
        self.cycle_ties = data.pop('cycleT', None)
        self.cycle_loses = data.pop('cycleL', None)
        self.cycle_tie_braker = data.pop('cycleTieBreaker', None)
        self.cycle_plus_minus = data.pop('cyclePlusMinus', None)
        self.cycle_score_total = data.pop('cycleScoreTotal', None)
        self.is_recruiting = data.pop('isRecruiting', None)
        self.id = data.pop('id', None)
        self.name = data.pop('name', None)
        self.logo_url = VRML_URL + data.pop('logo', None)
        self.region_id = data.pop('regionID', None)
        self.region = data.pop('region', None)
    
    
    async def players(self):
        raise NotImplementedError
    
    async def stats_to_other_team(self, other):
        raise NotImplementedError

    async def upcoming_matches(self):
        raise NotImplementedError

    async def matches_history(self):
        return [Match(data) for data in await get_team_matches_history(self.id)]


class Match:
    def __init__(self, data):
        self._update(data)
    
    def _update(self, data):
        self.id = data.pop('id', None)
        self.season_name = data.pop('seasonName', None)
        self.week = data.pop('week', None)
        self.winning_team_id = data.pop('winningTeamID', None)
        self.losing_Team_id = data.pop('losingTeamID', None)
        self.home_team_score = data.pop('homeScore', None)
        self.away_team_score = data.pop('awayScore', None)
        self.home_team_highlights = data.pop('homeHighlights', None)
        self.away_team_highlights = data.pop('awayHighlights', None)
        self.vod_URL = data.pop('vodURL', None)
        self.scheduled_date = dt.datetime.fromisoformat(data.pop('dateScheduled', None))

        self.home_team = PartialTeam(data.pop('homeTeam'))
        self.away_team = PartialTeam(data.pop('awayTeam'))

        self.maps = []
        for m in data.pop('mapsSet', None):
            self.maps.append(MatchSet(m))
        
class MatchSet:     
    # this is a very specific class only working with the maps-data in `csl Match`!
    def __init__(self, data):
        self._update(data)
    
    def _update(self, data):
        self.number = data.pop('mapNum', None)
        self.name = data.pop('mapName', None)
        self.home_team_score = data.pop('homeScore', None)
        self.away_team_score = data.pop('awayScore', None)


class Season:
    def __init__(self, data):
        self._update(data)
    
    def _update(self, data):
        self.id = data.pop('id', None)
        self.name = data.pop('name', None)





###############################################################################
## Functions

async def search_team(game, query, **kwargs):
    '''Search for teams.
    
    Args:
        game (str): Game to search teams for. Examples: Onward, EchoArena, Pavlov, Snapshot.
        name (str): The search criteria.
        season (str, optional): The season id.
        region (str, optional): Team's region. Examples: NA, EU, OCE or none.
    
    Returns:
        `list` of `PartialTeam` corresponding to the search criteria
    '''
    resp = await get_search_team(game, query, **kwargs)
    teams = []
    for data in resp:
        teams.append(PartialTeam(data))
    return teams

async def seasons(game):
    '''Gets the seasons for the specified game name in the URL.
    
    Args:
        game: (str) Examples: Onward, EchoArena, Pavlov, Snapshot
        
    Returns:
        `list` of `Season`
    '''
    seasons = []
    for data in await get_seasons(game):
        seasons.append(Season(data))
    return seasons







###############################################################################
## for testing

async def main():
    start = time.time()

    p_teams = await search_team("EchoArena", "Fenrir")
    if len(p_teams) == 0:
        print("No Teams found")
    elif len(p_teams) > 1:
        print(f"Search was not unambiguous. {len(p_teams)} were found:")
        for t in p_teams:
            print(t.name)
    else:
        team:Team = await p_teams[0].fetch()
        matches_history:list[Match] = await team.matches_history()
        season_list = await seasons("EchoArena")
        current_season = season_list[-1]
        for match in matches_history:
            if match.season_name != current_season.name:
                continue
            print(match.home_team.name, match.home_team_score, ":", match.away_team_score, match.away_team.name)


    end = time.time()
    print(f"Finished in {end-start:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())

