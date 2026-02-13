import secrets
from typing import Annotated, Optional

from fastapi import Header, HTTPException

HARDCODED_SETUP_TOKENS = [
    "c5125794ff68841579e822ca4c05edb644e16aeccb36916aa46970f7fe915de9",
]


def _extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()


def _allowed_tokens() -> list[str]:
    return HARDCODED_SETUP_TOKENS


def _token_matches(candidate: str, allowed: list[str]) -> bool:
    for token in allowed:
        if secrets.compare_digest(candidate, token):
            return True
    return False


def require_setup_token(
    authorization: Annotated[Optional[str], Header()] = None,
    x_setup_token: Annotated[Optional[str], Header()] = None,
) -> None:
    allowed = _allowed_tokens()
    if not allowed:
        # Fail closed: keep setup endpoints unavailable if no token is configured.
        raise HTTPException(status_code=404, detail="Not found")

    bearer = _extract_bearer_token(authorization)
    candidates = [token for token in [x_setup_token, bearer] if token]

    for candidate in candidates:
        if _token_matches(candidate, allowed):
            return

    raise HTTPException(status_code=404, detail="Not found")
