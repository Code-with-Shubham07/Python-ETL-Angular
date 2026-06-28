from fastapi import APIRouter, HTTPException, Path, Query
from db_connector import Neo4jConnector
from fastapi import Depends
from auth import verify_token

router = APIRouter()
db = Neo4jConnector()


@router.get("/summary")
def summary(auth=Depends(verify_token)):
    """Return counts of main node labels"""
    try:
        return {
            "status": "success",
            "data": db.get_summary()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
def team_details(
    team_id: int | None = Query(
        None,
        description="Team ID must be positive"
    ),
    team_name: str | None = Query(
        None, 
        description="Exact or partial team name"
    ),
    auth=Depends(verify_token)
):
    try:
        if team_id is not None and team_id <= 0:
            return{
                "status": "error",
                "message": "team_id must be a positive integer"
            }
        
        if team_id is None and not team_name:
            raise HTTPException(status_code=400, detail="Provide either team_id or team_name.")
        
        if team_id is not None and team_name:
            raise HTTPException(status_code=400, detail="Provide only one of team_id or team_name.")
        
        if team_id is not None:
            team = db.get_team_by_id(team_id)
        else:
            team = db.get_team_by_name(team_name)

        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        return {"status": "success", "data": team}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players")
def player_details(
    player_id:int | None = Query(
        None,
        description="Player ID must be positive."
    ),
    player_name: str | None = Query(
        None,
        description="Partial or full Player name"
    ),
    auth=Depends(verify_token)
):
    try:
        if player_id is not None and player_id <= 0:
            return{
                "status": "error",
                "message": "player_id must be a positive integer"
            }
        
        if player_id is None and not player_name:
            raise HTTPException(status_code=400, detail="Provide either player_id or player_name.")
        
        if player_id is not None and player_name:
            raise HTTPException(status_code=400, detail="Provide only one of player_id or player_name.")
        
        if player_id is not None:
            player = db.get_player_by_id(player_id)
        else:
            player = db.get_player_by_name(player_name)

        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return {"status": "success", "data": player}
    
    except HTTPException:
        raise
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/countries/leagues")
def country_league_details(
    country_id: int | None = Query(
        None,
        description="Country ID must be positive."
    ),
    country_name: str | None =Query(
        None,
        description="Partial of full country name."
    ),
    auth=Depends(verify_token)
):
    try:
        if country_id is not None and country_id <= 0:
            return{
                "status": "error",
                "message": "country_id must be a positive integer"
            }
        
        if country_id is None and not country_name:
            raise HTTPException(status_code=400, detail="Provide either country_id or country_name.")
        
        if country_id is not None and country_name:
            raise HTTPException(status_code=400, detail="Provide only one of country_id or country_name.")
        
        if country_id is not None:
            data = db.get_country_with_leagues(country_id)
        else:
            data = db.get_country_with_leagues_by_name(country_name)

        if not data:
            raise HTTPException(status_code=404, detail="Country or Leagues not found")
        return {"status": "success", "data": data}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/matches")
def team_goals(
    team_id: int | None = Query(
        None,
        description="Team ID must be positve."                  
    ),
    team_name: str | None = Query(
        None,
        description="Partial or full Team name."
    ),
    auth=Depends(verify_token)
):
    try:
        if team_id is not None and team_id <= 0:
            return {
                "status": "error",
                "message": "team_id must be a positive integer."
            }
        
        if team_id is None and not team_name:
            raise HTTPException(status_code=400, detail="Provide either team_id or team_name.")
        
        if team_id is not None and team_name:
            raise HTTPException(status_code=400, detail="Provide only one of team_id or team_name.")
        
        if team_id is not None:
            goals = db.get_team_goals_by_id(team_id)
        else:
            goals = db.get_team_goals_by_name(team_name)

        if not goals:
            raise HTTPException(status_code=404, detail="No matches found for this team")
        return {"status": "success", "data": goals}
    
    except HTTPException:
        raise
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    