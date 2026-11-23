from mahwish_dugout.errors import InvalidTeamError, PlayerNotFoundError
from mahwish_dugout.loader import load_player, load_teams
 
players = load_player("data/players.csv")
 
for team in load_teams("data/sample_teams.csv",
                       players):
    try:
        team.validate()
        print(f"{team.team_name}: LEGAL")
    except InvalidTeamError as error:
        print(f"{team.team_name}: {error}")

try:
    raise PlayerNotFoundError("P999")
except PlayerNotFoundError as error:
    print(f"Handled missing player: {error}")
