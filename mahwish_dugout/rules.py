
TEAM_SIZE = 11
MAX_CREDITS = 100
MAX_FROM_ONE_FRANCHISE = 7

# ROLE-> (Minimum, maximum )numbers of players allowed in a team
ROLE_LIMITS = {
    "WK": (1, 2),
    "BAT": (3, 5),
    "AR": (1, 3),
    "BOWL": (3, 5)
}

def check_players_count(team):
    """ The team must have exactly TEAM_SIZE players."""

    if len(team.players) != TEAM_SIZE:
        return [f"Team must have exactly {TEAM_SIZE} players, but has {len(team.players)}"]
    return []

def check_budget(team):
    """ The total credits of the team must not be exceed MAX_CREDITS."""

    total = team.total_credits()
    if total > MAX_CREDITS:
        return [f"Team has {total} credits, but must not exceed {MAX_CREDITS}"]
    return[]

def check_franchise_limit(team):
    """ No more than MAX_FROM_ONE_FRANCHISE players froma single franchise"""
    errors = []
    for franchise, count in team.count_by_franchise().items():
        if count > MAX_FROM_ONE_FRANCHISE:
            errors.append(
                f"Team has {count} players from {franchise},"
                f" but must not exceed {MAX_FROM_ONE_FRANCHISE}"
                )
    return errors

def check_roles(team):
    """Each role must have betweeen its minimum and maximum number of players"""

    counts = team.count_by_role()
    errors =[]
    for role, (low,high) in ROLE_LIMITS.items():
        count = counts.get(role, 0)
        if count < low or count > high:
            errors.append(
                f"Team has {count} players with role {role}, "
                f" but must have between {low} and {high}"
            )
    return errors

def check_captains(team):
    """ captain and vice captain must be chosen, be in the team and be different"""
    #stop early: the checks below would crash on none."""
    if team.captain is None or team.vice_captain is None:
        return[" team must have captain and vice captain."]
    errors = []
    if team.captain not in team.players:
        errors.append (f"Captain {team.captain} is not in the team.")
    if team.vice_captain not in team.players:
        errors.append (f"Vice Captain {team.vice_captain} is not in the team.")
    if team.captain == team.vice_captain:
        errors.append("Captain and vice captain cannot be the same player.")
    return errors

def check_no_duplicates(team):
    """There must be no duplicate player IDs."""
    seen = set()
    errors = []
    for player in team.players:
        if player.player_id in seen:
            errors.append(f"Player ID {player.player_id} appears more than once.")
        seen.add(player.player_id)
    return errors
