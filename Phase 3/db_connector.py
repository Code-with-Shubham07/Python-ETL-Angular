from neo4j import GraphDatabase
import os
import sys
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)                
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from common_utils import load_config, setup_logger
    
class Neo4jConnector:
    def __init__(self):
        setup_logger("Phase 3/logs.txt")

        env_path = os.path.join(PROJECT_ROOT, ".env")
        load_dotenv(env_path)

        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")

        if not all([uri, user, password]):
            cfg = load_config("Phase 3/config.yaml")
            neo4j_cfg = cfg.get("neo4j", {})
            uri = uri or neo4j_cfg.get("uri")
            user = user or neo4j_cfg.get("user")
            password = password or neo4j_cfg.get("password")

        if not all([uri, user, password]):
            raise RuntimeError("Neo4j config not found in .env or Phase 3/config.yaml")

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


    def get_summary(self):
        """Return count of nodes for each main label + total relationships"""
        query = """
        MATCH (n)
        WITH labels(n)[0] AS label, count(n) AS count
        WHERE label IN ['Country', 'League', 'Match', 'Player', 'Team']
        RETURN label, count
        ORDER BY label
        """

        with self.driver.session() as session:
            result = session.run(query)
            summary_data = {record['label']: record['count'] for record in result}

        rel_query = """
        MATCH ()-[r]->()
        RETURN count(r) AS total_relationships
        """

        with self.driver.session() as session:
            rel_result = session.run(rel_query)
            total_relationships = rel_result.single()['total_relationships']

        summary_data["Total_relationships"] = total_relationships

        return summary_data
    

    def get_team_by_id(self, team_id: int):
        query = """
        MATCH (t:Team {team_api_id: $team_id})
        OPTIONAL MATCH (t)<-[:HAS_HOME_TEAM|HAS_AWAY_TEAM]-(m:Match)
        OPTIONAL MATCH (m)-[:PART_OF]->(l:League)
        OPTIONAL MATCH (m)-[:PLAYED_IN]->(c:Country)
        RETURN t,
                collect(DISTINCT l) AS leagues,
                collect(DISTINCT c) AS countries
        """
        with self.driver.session() as session:
            record = session.run(query, team_id=team_id).single()
            if not record:
                return None
            
            team_node = record["t"]
            leagues = record["leagues"] or []
            countries = record["countries"] or []

            return {
                "team": dict(team_node),
                "leagues": [dict(l) for l in leagues if l],
                "countries": [dict(c) for c in countries if c],
            }
        

    def get_team_by_name(self, team_name:str):
        query = """
        MATCH (t:Team)
        WHERE tolower(t.team_long_name) CONTAINS toLower($name)
            OR toLower(t.team_short_name) CONTAINS toLower($name)
        OPTIONAL MATCH (t)<-[:HAS_HOME_TEAM|HAS_AWAY_TEAM]-(m:Match)
        OPTIONAL MATCH (m)-[:PART_OF]->(l:League)
        OPTIONAL MATCH (m)-[:PLAYED_IN]->(c:Country)
        RETURN t,
                collect(DISTINCT l) AS leagues,
                collect(DISTINCT c) AS countries
        """
        with self.driver.session() as session:
            record = session.run(query, name=team_name).single()
            if not record:
                return None
            
            team_node = record["t"]
            leagues = record["leagues"] or []
            countries = record["countries"] or []

            return {
                "team": dict(team_node),
                "leagues": [dict(l) for l in leagues if l],
                "countries": [dict(c) for c in countries if c],
            }
            

    def get_player_by_id(self, player_id: int):
        """Return player info for given player_id from Neo4j"""
        query = """
        MATCH (p:Player)
        WHERE toString(p.player_api_id) = toString($player_id)
        RETURN p.player_api_id AS player_id,
               p.player_name AS player_name,
               p.birthday AS birthday,
               p.height AS height,
               p.weight AS weight
        """
        with self.driver.session() as session:
            result = session.run(query, player_id=player_id)
            record = result.single()
            if record:
                return dict(record)
            else:
                return None
            

    def get_player_by_name(self, player_name: str):
        query = """
        MATCH (p:Player)
        WHERE toLower(p.player_name) CONTAINS toLower($player_name)
        RETURN p.player_api_id AS player_id,
               p.player_name AS player_name,
               p.birthday AS birthday,
               p.height AS height,
               p.weight AS weight
        """
        with self.driver.session() as session:
            result = session.run(query, player_name=player_name)
            record = result.single()
            if record:
                return dict(record)
            else:
                return None
    

    def get_country_with_leagues(self, country_id: int):
        """Return country name and all leagues under it"""
        query = """
        MATCH (c:Country)<-[:BELONGS_TO]-(l:League)
        WHERE toString(c.id) = toString($country_id)
        RETURN c.name AS country_name,
               collect(l.name) AS leagues
        """
        with self.driver.session() as session:
            result = session.run(query, country_id=country_id)
            record = result.single()
            if record:
                return dict(record)
            else:
                return None
     

    def get_country_with_leagues_by_name(self, country_name: str):
        query = """
        MATCH (c:Country)<-[:BELONGS_TO]-(l:League)
        WHERE toLower(c.name) CONTAINS toLower($country_name)
        RETURN c.name AS country_name,
               collect(l.name) AS leagues
        """
        with self.driver.session() as session:
            result = session.run(query, country_name=country_name)
            record = result.single()
            if record:
                return dict(record)
            else:
                return None
            

    def get_team_goals_by_id(self, team_id: int):
        query = """
        OPTIONAL MATCH (m1:Match)
        WHERE toString(m1.home_team_api_id) = toString($team_id)
        WITH coalesce(sum(m1.home_team_goal), 0) AS home_goals

        OPTIONAL MATCH (m2:Match)
        WHERE toString(m2.away_team_api_id) = toString($team_id)
        RETURN home_goals, 
                coalesce(sum(m2.away_team_goal), 0) AS away_goals
        """
        with self.driver.session() as session:
            record = session.run(query, team_id=team_id).single()
            if not record:
                return None
            
            return {
                "home_goals": record["home_goals"],
                "away_goals": record["away_goals"],
            }
        

    def get_team_goals_by_name(self, team_name: str):
        query = """
        MATCH (t:Team)
        WHERE toLower(t.team_long_name) CONTAINS toLower($team_name)
           OR toLower(t.team_short_name) CONTAINS toLower($team_name)
        WITH t

        OPTIONAL MATCH (m1:Match)
        WHERE toString(m1.home_team_api_id) = toString(t.team_api_id)
        WITH t, coalesce(sum(m1.home_team_goal), 0) AS home_goals

        OPTIONAL MATCH (m2:Match)
        WHERE toString(m2.away_team_api_id) = toString(t.team_api_id)
        RETURN home_goals,
                coalesce(sum(m2.away_team_goal), 0) AS away_goals
        """
        with self.driver.session() as session:
            record = session.run(query, team_name=team_name).single()
            if not record:
                return None
            
            return {
                "home_goals": record["home_goals"],
                "away_goals": record["away_goals"],
            }
        