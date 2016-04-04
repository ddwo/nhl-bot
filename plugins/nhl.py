import parsedatetime as pdt
from dateutil.parser import parse
from pytz import timezone
from datetime import timedelta

from util import hook, http
from nhlutil import NHL_TEAMS, get_date, get_nhl_json, get_scores

EASTERN = timezone('US/Eastern')

@hook.command('schedule', autohelp=False)
def nhl_schedule(inp):
    """Return the schedule for either the current or specified day or for a specified team"""
    j = None
    if inp is None:
        # return schedule for current day
        inp = "today"

    inp = inp.lower()
    # Check for a team name/nickname in the input
    for team in NHL_TEAMS:
        for teamname in team[1]:
            if inp == teamname:
                # Return the team schedule for one week after today
                j = get_nhl_json(get_date('today'),
                                 end_date=get_date('next week'),
                                 team_id=team[0])
    if j is not None:
        # We want the team schedule
        schedule = []
        for date in j['dates']:
            # this is assuming only one game per day...
            game = date['games'][0]
            teams = "%s @ %s" % (game['teams']['away']['team']['teamName'],
                                 game['teams']['home']['team']['teamName'])
            broadcasts = []
            for stations in game['broadcasts']:
                broadcasts.append(stations['name'])
            game_date = parse(game['gameDate']).astimezone(EASTERN).strftime('%-I:%M %p')
            schedule.append("%s%s ET (%s)" % (teams.ljust(25),
                                              game_date.rjust(8),
                                              ', '.join(broadcasts)))
        return schedule
    else:
        # We want the schedule of today or some other day
        date = get_date(inp)
        j = get_nhl_json(date)
        schedule = []
        for game in j['dates'][0]['games']:
            game_date = parse(game['gameDate']).astimezone(EASTERN).strftime('%-I:%M %p')
            teams = "%s @ %s" % (game['teams']['away']['team']['teamName'],
                                 game['teams']['home']['team']['teamName'])
            broadcasts = []
            for stations in game['broadcasts']:
                broadcasts.append(stations['name'])
            schedule.append("%s%s ET (%s)" % (teams.ljust(25),
                                              game_date.rjust(8),
                                              ', '.join(broadcasts)))
    return schedule

@hook.command('scores', autohelp=False)
def nhl_scores(inp):
    """Return the scores for either the current or specified day"""
    games = get_scores(inp, 'Live')
    scores = []
    for game in games:
        scores.append("%s: %s, %s: %s (%s %s)" %
                      (game['teams']['away']['team']['name'],
                       game['teams']['away']['score'],
                       game['teams']['home']['team']['name'],
                       game['teams']['home']['score'],
                       game['linescore']['currentPeriodTimeRemaining'],
                       game['linescore']['currentPeriodOrdinal']))
    if not len(scores):
        return "no games to report"
    return scores

@hook.command('finals', autohelp=False)
def nhl_finals(inp):
    """Return final games for the current or specified day"""
    games = get_scores(inp, 'Final')
    scores = []
    for game in games:
        away = game['teams']['away']['score']
        home = game['teams']['home']['score']
        if away > home:
            winner = (game['teams']['away']['team']['teamName'], away)
            loser = (game['teams']['home']['team']['teamName'], home)
        else:
            winner = ("%s:" % game['teams']['home']['team']['teamName'], home)
            loser = ("%s:" %game['teams']['away']['team']['teamName'], away)
        scores.append("\x02%s%s\x02, %s%s" %
                      (winner[0].ljust(13), winner[1],
                       loser[0].ljust(13), loser[1]))
    return scores

@hook.command('pstat')
def nhl_skater_stats(inp):
    return

@hook.command('gstat')
def nhl_goalie_stats(inp):
    return

@hook.command('ptop')
def nhl_ptop(inp):
    return
