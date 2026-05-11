import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

SETUP_USERNAME = "sebastian"
SETUP_PASSWORD = "config"

basic_auth = HTTPBasic()


def require_setup_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth)],
) -> None:
    username_ok = secrets.compare_digest(credentials.username, SETUP_USERNAME)
    password_ok = secrets.compare_digest(credentials.password, SETUP_PASSWORD)

    if username_ok and password_ok:
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )
