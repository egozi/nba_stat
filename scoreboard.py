# score-board

from nba_util import TODAY, NBA
from nba_util import _get_json
from nba_util import _api_scrape

class Scoreboard:
    """ A scoreboard for all games for a given day
    Displays current games plus info for a given day

    Args:
        :month: Specified month (1-12)
        :day: Specified day (1-31)
        :year: Specified year (YYYY)
        :league_id: ID for the league to look in (Default is 00)
        :offset: Day offset from which to operate

    Attributes:
        :json: Contains the full json dump to play around with
    """
    _endpoint = 'scoreboard'

    def __init__(self,
                 month=TODAY.month,
                 day=TODAY.day,
                 year=TODAY.year,
                 league_id=NBA,
                 offset=0):
        self._game_date = '{month:02d}/{day:02d}/{year}'.format(month=month,
                                                                day=day,
                                                                year=year)
        self.json = _get_json(endpoint=self._endpoint,
                              params={'LeagueID': league_id,
                                      'GameDate': self._game_date,
                                      'DayOffset': offset})

    def game_header(self):
        return _api_scrape(self.json, 0)      

    def line_score(self):
        return _api_scrape(self.json, 1)                                    
