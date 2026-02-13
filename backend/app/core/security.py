from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in ["admin", "customer"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return credentials.username
