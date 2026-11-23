# dugout models.py, at the top 
from mahwish_dugout.errors import InvalidTeamError, PlayerNotFoundError
from mahwish_dugout.rules import(
    check_players_count,
    check_budget,
    check_franchise_limit,
    check_roles,
    check_captains,
)

def find_player(players, player_id):
    """return the player with this id or raise PlayerNotFoundError"""
    if player_id not in players:
        raise PlayerNotFoundError(player_id)
    return players[player_id]


class Player:
    #constructor 
    def __init__(self, player_id, name, franchise, role, credits):
        self.player_id = player_id
        self.name = name 
        self.franchise = franchise
        self.role = role 
        self.credits = credits

    @classmethod
    #"""decorator to create a Player object from a row of data"""
    def from_row(cls, row):
        return cls(
            row["player_id"],
            row["name"],
            row["franchise"],
            row["role"],
            float(row["credits"])
        )

    def __str__(self):
        return f"{self.name} ({self.franchise}, {self.role}, {self.credits} cr)"


class FantacyTeam:
    """A fantacy XI picked by one person"""
    def __init__(self, team_name, owner):
        self.team_name = team_name
        self.owner = owner
        self.players = []
        self.captain = None
        self.vice_captain = None

#inshide class fantacy team 
    
    def add_player(self, player):
        self.players.append(player)

    def total_credits(self):
        total = 0 
        for player in self.players:
            total = total + player.credits 
        return total

    def count_by_role(self):
        counts = {'WK': 0, 'BAT': 0, 'AR': 0, 'BOWL': 0} 
        for player in self.players:
            counts[player.role] = counts[player.role] + 1
        return counts

    def set_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain

    def count_by_franchise(self):
        """return a dictionary of franchise -> number of players from that franchise"""
        counts = {}
        for player in self.players:
            #get(key,0)gives 0 the first time we see a franchise
            counts[player.franchise] = counts.get(player.franchise, 0) + 1
        return counts

    def check_rules(self):
            """return a list of rules violation. An empty list means the team is leagal."""
            errors = []
            errors.extend(check_players_count(self))
            errors.extend(check_budget(self))
            errors.extend(check_franchise_limit(self))
            errors.extend(check_roles(self))
            errors.extend(check_captains(self))
            from mahwish_dugout.rules import check_no_duplicates
            errors.extend(check_no_duplicates(self))
            return errors
    
    
    def __str__(self):
        size = len(self.players)
        cost = self.total_credits()
        return f"{self.team_name} (owner:{self.owner},{size} players, {cost} cr)"

    def validate(self):
        """raise InvalidTeamError if the team vreaks any rule """
        problems = self.check_rules()

        if problems:
            raise InvalidTeamError(self.team_name, problems)


class League:
    """A collection of Fantacy teams, with methods to look up and rank them """
    def __init__(self, name ):
        self.name = name 
        self.teams = {} # owner name -> FantacyTeam 

    def add_team (self, team ):
        self.teams[team.owner] = team

    def find_team (self , owner ):
        """return the FantacyTeam for the given owner, or None if not found ."""
        return self.teams.get(owner) 

    def leagal_teams (self):
        """Return a list of the teams that break no rules."""
        return[team for team in self.teams.values() if not team.check_rules()]

    def rank_teams(self):
        """return a list of teams sorted by total credits (lowest first)"""
        #self.team is dict, so sort its values (the team), not its key 
        return sorted(self.teams.values(), key=lambda team: team.total_credits())

        

