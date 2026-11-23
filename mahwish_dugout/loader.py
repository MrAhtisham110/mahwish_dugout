"""functions that read players and teams from csv file"""

import csv
from mahwish_dugout.models import Player, FantacyTeam

def load_player(path):
     """Return a dict of player id -> Player for every row in the CSV file at path."""
     players = {}
     with open(path, newline="", encoding="utf-8") as f:
        # DictReader turns each row into a dict keyed by the header names
      for row in csv.DictReader(f):
          player = Player.from_row(row)
          players[player.player_id] = player
     return players 


def team_from_row(row, players):
    """Return a FantasyTeam built from one row (a dict) of a teams CSV file.
 
    The CSV stores player ids such as "P012;P089", so we use the players
    dict to turn each id back into a real Player object.
    """
 
    team = FantacyTeam(row["team_name"], row["owner"])
 
    for player_id in row["players"].split(";"):
        team.add_player(players[player_id.strip()])
    
    team.set_captain(players[row["captain"]], players[row["vice_captain"]])
 
    return team
 
 
def load_team(path, players):
    """Return the first team in a teams CSV file, or None if the file has no teams."""
 
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            return team_from_row(row, players)  # return on the first row only
 


# def team_from_row(row,players):
#     team = FantasyTeam(row["team_name"], row["owner_name"])



def load_teams(path,players):
     """return a list of every team is a teams CSV file. """
     teams =[]
     with open(path, newline = "", encoding = "utf-8") as f:
         for row in csv.DictReader(f):
             teams.append (team_from_row (row, players))
     return teams
