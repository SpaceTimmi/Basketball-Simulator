from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo
import json
import sqlite3
import time

# Functions
def add_teams(lst_of_teams, conn):
    """
    Gets a list of jsons and a database connection.
    Each json contains data for each NBA Team in both conferences.
    conn is the connection to the database.
    """

    atlantic  = ['Celtics', 'Nets', 'Knicks', '76ers', 'Raptors' ] #01
    central   = ['Bulls', 'Cavaliers', 'Pistons', 'Pacers', 'Bucks'] #02
    southeast = ['Hawks', 'Hornets', 'Heats', 'Magic', 'Wizards'] #03

    northwest = ['Nuggets', 'Timberwolves', 'Thunder', 'Blazers', 'Jazz'] #11
    pacific   = ['Warriors', 'Clippers', 'Lakers', 'Suns', 'Kings'] #12
    southwest = ['Mavericks', 'Rockets', 'Grizzlies','Pelicans', 'Spurs'] #13

    eastern_conf = [atlantic, central, southeast] #0
    western_conf = [northwest, pacific, southwest] #1


    for team in lst_of_teams:
        full_name = team['full_name']
        abb = team['abbreviation']
        conference, division = 0, 0
        nickname = team['nickname']

        for index, div in enumerate(eastern_conf):
            if nickname in div:
                conference, division = 0, (index + 1)

        for index, div in enumerate(western_conf):
            if nickname in div:
                conference, division = 1, (index + 1)


        print(full_name, abb, conference, division)
        return


def add_players(lst_of_players, conn):
    """
    Takes in a connection to the database and list of player jsons.
    Calls API with each player id then addes the player and their relevant info to the database.
    conn is the connection to the database.
    """
    for player in lst_of_players:
        # Get json from player ID
        pid = player['id']
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=pid)
        result = player_info.get_json()
        parsed = json.loads(result)

        # Parse data from json
        first_name = parsed['resultSets'][0]['rowSet'][0][1]
        last_name = parsed['resultSets'][0]['rowSet'][0][2]
        height = parsed['resultSets'][0]['rowSet'][0][11]
        position = parsed['resultSets'][0]['rowSet'][0][15]
        team_name = parsed['resultSets'][0]['rowSet'][0][19]
        ppg = parsed['resultSets'][1]['rowSet'][0][3]
        ast = parsed['resultSets'][1]['rowSet'][0][4]
        reb = parsed['resultSets'][1]['rowSet'][0][5]
        pie = parsed['resultSets'][1]['rowSet'][0][6]

        print(parsed)
        return
        time.sleep(5)

        # Insert data into database
    return




# Main
conn = sqlite3.connect('./data/basketball_db.sqlite')
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS CONFERENCE;
DROP TABLE IF EXISTS DIVISION;
DROP TABLE IF EXISTS TEAMS;
DROP TABLE IF EXISTS PLAYERS;

CREATE TABLE CONFERENCE (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name VARCHAR(123)
);

CREATE TABLE DIVISION (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name VARCHAR(123),
    conference_id INTEGER
);

CREATE TABLE TEAMS (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name VARCHAR(123),
    abb VARCHAR(123),
    conference_id INTEGER,
    divison_id INTEGER
);

CREATE TABLE PLAYERS (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    fname VARCHAR(123),
    lname VARCHAR(123),
    height VARCHAR(123),
    position VARCHAR(123),
    team_id INTEGER,
    ppg REAL,
    ast REAL,
    reb REAL,
    pie REAL
);
""")


active_players = players.get_active_players()
add_players(active_players, '')
#print(active_players)




"""
if __name__ == '__main__':
    #active_players = players.get_active_players()
    #add_players(active_players)

    #nba_teams = teams.get_teams()
    #add_teams(nba_teams)

"""
