import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
import requests
import json

# Constants
TODAY = datetime.today()
BASE_URL = 'http://stats.nba.com/stats/{endpoint}'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),  # noqa: E501
    'Dnt': ('1'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'origin': ('http://stats.nba.com')
}
NBA = '00'

def _get_json(endpoint, params, referer='scores'):
    """
    Internal method to streamline our requests / json getting
    Args:
        endpoint (str): endpoint to be called from the API
        params (dict): parameters to be passed to the API
    Raises:
        HTTPError: if requests hits a status code != 200
    Returns:
        json (json): json object for selected API call
    """
    h = dict(HEADERS)
    h['referer'] = 'http://stats.nba.com/{ref}/'.format(ref=referer)
    _get = requests.get(BASE_URL.format(endpoint=endpoint), params=params,
               headers=h)
    # print _get.url
    _get.raise_for_status()
    return _get.json()

def _api_scrape(json_inp, ndx, HAS_PANDAS=False):
    """
    Internal method to streamline the getting of data from the json
    Args:
        json_inp (json): json input from our caller
        ndx (int): index where the data is located in the api
    Returns:
        If pandas is present:
            DataFrame (pandas.DataFrame): data set from ndx within the
            API's json
        else:
            A dictionary of both headers and values from the page
    """

    try:
        headers = json_inp['resultSets'][ndx]['headers']
        values = json_inp['resultSets'][ndx]['rowSet']
    except KeyError:
        # This is so ugly but this is what you get when your data comes out
        # in not a standard format
        try:
            headers = json_inp['resultSet'][ndx]['headers']
            values = json_inp['resultSet'][ndx]['rowSet']
        except KeyError:
            # Added for results that only include one set (ex. LeagueLeaders)
            headers = json_inp['resultSet']['headers']
            values = json_inp['resultSet']['rowSet']
    if HAS_PANDAS:
        return pd.DataFrame(values, columns=headers)
    else:
        # Taken from www.github.com/bradleyfay/py-goldsberry
        return [dict(zip(headers, value)) for value in values]




def get_all_player_ids(ids="shots"):
    """
    Returns a pandas DataFrame containing the player IDs used in the
    stats.nba.com API.
    Parameters
    ----------
    ids : { "shots" | "all_players" | "all_data" }, optional
        Passing in "shots" returns a DataFrame that contains the player IDs of
        all players have shot chart data.  It is the default parameter value.
        Passing in "all_players" returns a DataFrame that contains
        all the player IDs used in the stats.nba.com API.
        Passing in "all_data" returns a DataFrame that contains all the data
        accessed from the JSON at the following url:
        http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2015-16
        The column information for this DataFrame is as follows:
            PERSON_ID: The player ID for that player
            DISPLAY_LAST_COMMA_FIRST: The player's name.
            ROSTERSTATUS: 0 means player is not on a roster, 1 means he's on a
                          roster
            FROM_YEAR: The first year the player played.
            TO_YEAR: The last year the player played.
            PLAYERCODE: A code representing the player. Unsure of its use.
    Returns
    -------
    df : pandas DataFrame
        The pandas DataFrame object that contains the player IDs for the
        stats.nba.com API.
    """
    url = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2018-19"

    # get the web page
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    # access 'resultSets', which is a list containing the dict with all the data
    # The 'header' key accesses the headers
    headers = response.json()['resultSets'][0]['headers']
    # The 'rowSet' key contains the player data along with their IDs
    players = response.json()['resultSets'][0]['rowSet']
    # Create dataframe with proper numeric types
    df = pd.DataFrame(players, columns=headers)

    return df
    # # Dealing with different means of converision for pandas 0.17.0 or 0.17.1
    # # and 0.15.0 or loweer
    # if '0.17' in pd.__version__:
    #     # alternative to convert_objects() to numeric to get rid of warning
    #     # as convert_objects() is deprecated in pandas 0.17.0+
    #     df = df.apply(pd.to_numeric, args=('ignore',))
    # else:
    #     df = df.convert_objects(convert_numeric=True)

    # if ids == "shots":
    #     df = df.query("(FROM_YEAR >= 2001) or (TO_YEAR >= 2001)")
    #     df = df.reset_index(drop=True)
    #     # just keep the player ids and names
    #     df = df.iloc[:, 0:2]
    #     return df
    # if ids == "all_players":
    #     df = df.iloc[:, 0:2]
    #     return df
    # if ids == "all_data":
    #     return df
    # else:
    #     er = "Invalid 'ids' value. It must be 'shots', 'all_shots', or 'all_data'."
    # raise ValueError(er)

def get_player_img(player_id):
    """
    Returns the image of the player from stats.nba.com as a numpy array and
    saves the image as PNG file in the current directory.
    Parameters
    ----------
    player_id: int
        The player ID used to find the image.
    Returns
    -------
    player_img: ndarray
        The multidimensional numpy array of the player image, which matplotlib
        ca plot.
    """
    url = "http://stats.nba.com/media/players/230x185/"+str(player_id)+".png"
    img_file = str(player_id) + ".png"
    pic = urlretrieve(url, img_file)
    player_img = plt.imread(pic[0])
    return player_img