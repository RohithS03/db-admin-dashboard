from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    expected_username = os.environ.get("ADMIN_USER", "admin")
    expected_password = os.environ.get("ADMIN_PASS", "secret")
    
    correct_username = secrets.compare_digest(credentials.username, expected_username)
    correct_password = secrets.compare_digest(credentials.password, expected_password)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
