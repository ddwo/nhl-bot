import parsedatetime as pdt
from dateutil.parser import parse
from pytz import timezone

from util import hook, http

EASTERN = timezone('US/Eastern')

def get_scores(inp, status):
    """Return NHL games with a specific status"""
    nhl_scores_url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&expand=schedule.linescore,schedule.teams"
    j = get_nhl_json(inp, nhl_scores_url)
    scores = []
    games =  j['dates'][0]['games']
    for game in games:
        if game['status']['abstractGameState'] == status:
            scores.append(game)
    return scores

def get_date(inp):
    """Parse the input as a date and return a format suitable for the nhl.com API"""
    if not inp:
        inp = 'today'
    cal = pdt.Calendar()
    return cal.parseDT(inp)[0].date().isoformat()

def get_nhl_json(inp, url):
    """Take the input as a raw date and return json from provided (nhl.com) url"""
    date = get_date(inp)
    return http.get_json(url % (date, date))

@hook.command('schedule', autohelp=False)
def nhl_schedule(inp):
    """Return the schedule for either the current or specified day"""
    nhl_schedule_url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&expand=schedule.teams,schedule.broadcasts.all"
    j = get_nhl_json(inp, nhl_schedule_url)
    schedule = []
    for game in j['dates'][0]['games']:
        game_date = parse(game['gameDate']).astimezone(EASTERN).strftime('%-I:%M %p')
        teams = "%s @ %s" % (game['teams']['away']['team']['teamName'],
                             game['teams']['home']['team']['teamName'])
        broadcasts = []
        for stations in game['broadcasts'] :
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
            loser =  (game['teams']['home']['team']['teamName'], home)
        else:
            winner = (game['teams']['home']['team']['teamName'], home)
            loser =  (game['teams']['away']['team']['teamName'], away)
        scores.append("\x02%s: %s\x02, %s: %s" %
                      (winner[0].ljust(12), winner[1],
                       loser[0].ljust(12), loser[1]))
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
