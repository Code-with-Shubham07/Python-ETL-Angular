from fastapi import FastAPI
from api_routes import router
import uvicorn
import os, sys
from fastapi.middleware.cors import CORSMiddleware

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)              
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common_utils import load_config

app = FastAPI(
    title="Football Graph API",
    description="Phase 3 - FastAPI interface to fetch data from Neo4j",
    version="1.0"
)

app.include_router(router)

if __name__ == "__main__":
    cfg = load_config("Phase 3/config.yaml")
    host = cfg["server"]["host"]
    port = cfg["server"]["port"]
    uvicorn.run("main:app",
                host=host,
                port=port,
                reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)    