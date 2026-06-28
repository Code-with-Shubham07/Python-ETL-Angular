"""
Defines graph structure for Neo4j loading in Phase 2.
"""

graph_model = {
    "nodes": {
        "Country": ["id", "name"],
        "League": ["id", "name", "country_id"],
        "Team": ["team_api_id", "team_long_name", "team_short_name"],
        "Player": ["player_api_id", "player_name", "birthday", "height", "weight"],
        "Match": ["match_api_id", "date", "home_team_api_id", "away_team_api_id", "home_team_goal", "away_team_goal", "id", "country_id", "league_id"],
        "player_attr": ["player_api_id", "overall_rating", "potential"],
        "team_attr": ["team_api_id", "buildUpPlaySpeed", "chanceCreationPassing"]
    },
    "relationships": {
        #League is associated with a country.
        "League-BELONGS_TO->Country": ("League", "Country", "country_id=id"),

        #A Match has one designated home team.
        "Match-HAS_HOME_TEAM->Team": ("Match", "Team", "home_team_api_id=team_api_id"),

        #A Match has one designated away team.
        "Match-HAS_AWAY_TEAM->Team": ("Match", "Team", "away_team_api_id=team_api_id"),

        #Every Match belongs to a specific league.
        "Match-PART_OF->League": ("Match", "League", "league_id=id"),

        #A Match is played in a particular country.
        "Match-PLAYED_IN->Country": ("Match", "Country", "country_id=id"),

        #player_attr describes a player.
        "Player_attr-DESCRIBES_PLAYER->Player": ("player_attr", "Player", "player_api_id=player_api_id"),

        #Team_attr describes a team.
        "team_attr-DESCRIBES_TEAM->Team": ("team_attr", "Team", "team_api_id=team_api_id"),
    }
}
