from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
VALID_TOKEN = "shubham"

def verify_token(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials

    if token != VALID_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return True

