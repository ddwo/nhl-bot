import parsedatetime as pdt

from util import http

CAL = pdt.Calendar()

NHL_TEAMS = [
    (1, ('njd', 'nj', 'devils')),
    (2, ('nyi', 'islanders')),
    (3, ('nyr', 'rangers', 'rags')),
    (4, ('phi', 'philly', 'flyers')),
    (5, ('pit', 'pittsburgh', 'pens', 'penguins')),
    (6, ('bos', 'boston', 'bruins')),
    (7, ('buf', 'buffalo', 'sabres')),
    (8, ('mon', 'montreal', 'canadiens', 'habs')),
    (9, ('ott', 'ottawa', 'senators', 'sens')),
    (10, ('tor', 'toronto', 'leafs', 'maple leafs')),
    (12, ('car', 'carolina', 'hurricanes', 'canes')),
    (13, ('fla', 'florida', 'panthers', 'cats')),
    (14, ('tbl', 'tampa', 'tampa bay', 'lightning', 'bolts')),
    (15, ('was', 'washington', 'capitals', 'caps')),
    (16, ('chi', 'chicago', 'blackhawks', 'hawks')),
    (17, ('det', 'detroit', 'red wings', 'wings', 'wangs')),
    (18, ('nsh', 'nashville', 'predators', 'preds')),
    (19, ('stl', 'st. louis', 'st louis', 'blues')),
    (20, ('cgy', 'calgary', 'flames')),
    (21, ('col', 'colorado', 'avalanche', 'avs')),
    (22, ('edm', 'edmonton', 'oilers', 'oil')),
    (23, ('van', 'vancouver', 'canucks')),
    (24, ('ana', 'anaheim', 'ducks', 'dorks')),
    (25, ('dal', 'dallas', 'stars')),
    (26, ('lak', 'la', 'los angeles', 'kings')),
    (28, ('sjs', 'sj', 'san jose', 'sharks', 'teal boys')),
    (29, ('cbj', 'cjb', 'lumbus', 'columbus', 'blue jackets', 'bjs')),
    (30, ('min', 'minnesota', 'wild')),
    (52, ('wpg', 'winnipeg', 'jets')),
    (53, ('ari', 'arizona', 'coyotes', 'yotes', 'aroos'))
]



def get_scores(inp, status):
    """Return NHL games with a specific status"""
    date = get_date(inp)
    j = get_nhl_json(date)
    scores = []
    games = j['dates'][0]['games']
    for game in games:
        if game['status']['abstractGameState'] == status:
            scores.append(game)
    return scores

def get_date(inp):
    """Parse the input as a date and return a format suitable for the nhl.com API"""
    if not inp:
        inp = 'today'
    return CAL.parseDT(inp)[0].date().isoformat()

def get_nhl_json(start_date, end_date=None, team_id=None):
    nhl_schedule_url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=%s&endDate=%s&expand=schedule.teams,schedule.broadcasts.all,schedule.linescore"
    if end_date is None:
        end_date = start_date
    if team_id:
        return http.get_json(nhl_schedule_url % (start_date, end_date) + "&teamId=%s" % team_id)
    return http.get_json(nhl_schedule_url % (start_date, end_date))
