from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

from security import require_setup_token

router = APIRouter()

# Whitelist of allowed configs for security (prevents path traversal attacks)
ALLOWED_CONFIGS = ["claude.md", "tmux", "nvim.tar.gz"]

SETUP_GUIDE = """# Setup API

Single entry point for machine bootstrap and configuration.

## Entry Point

- `GET /setup` - this guide

## Authentication

All setup endpoints require one of these headers:

- `X-Setup-Token: <token>`
- `Authorization: Bearer <token>`

## Quickstart

```bash
export SETUP_TOKEN='c5125794ff68841579e822ca4c05edb644e16aeccb36916aa46970f7fe915de9'
curl -H "X-Setup-Token: $SETUP_TOKEN" https://bartmann.xyz/setup
```

## Config Endpoints

- `GET /setup/config/claude.md`
- `GET /setup/config/tmux`
- `GET /setup/config/nvim.tar.gz`

Install all:
```bash
curl -H "X-Setup-Token: $SETUP_TOKEN" https://bartmann.xyz/setup/config/claude.md -o ~/.claude/CLAUDE.md
curl -H "X-Setup-Token: $SETUP_TOKEN" https://bartmann.xyz/setup/config/tmux -o ~/.tmux.conf
curl -H "X-Setup-Token: $SETUP_TOKEN" https://bartmann.xyz/setup/config/nvim.tar.gz | tar -xzf - -C ~/.config/
```

## SSH Key Endpoints

- `GET /setup/ssh/keys` - list available key names
- `GET /setup/ssh/keys/all` - get all keys
- `GET /setup/ssh/keys/{key_name}` - get one key by name

Example:
```bash
curl -H "X-Setup-Token: $SETUP_TOKEN" https://bartmann.xyz/setup/ssh/keys/all
```

## Compatibility Aliases

Legacy paths still work:

- `/config/*`
- `/ssh/keys*`
"""


def _config_path(config_name: str) -> Path:
    if config_name not in ALLOWED_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Config '{config_name}' not found")

    config_dir = Path(__file__).parent.parent / "config"
    config_file = config_dir / config_name
    if not config_file.exists():
        raise HTTPException(status_code=404, detail=f"Config '{config_name}' not found")
    return config_file


def _ssh_keys_dir() -> Path:
    ssh_keys_dir = Path(__file__).parent.parent / "ssh_keys"
    if not ssh_keys_dir.exists():
        raise HTTPException(status_code=404, detail="SSH keys directory not found")
    return ssh_keys_dir


@router.get("/setup", response_class=PlainTextResponse)
@router.get("/setup/", response_class=PlainTextResponse, include_in_schema=False)
@router.get("/config/", response_class=PlainTextResponse, include_in_schema=False)
async def get_setup_guide(_: None = Depends(require_setup_token)):
    return PlainTextResponse(SETUP_GUIDE.strip())


@router.get("/setup/config/{config_name}")
@router.get("/config/{config_name}", include_in_schema=False)
async def get_config(config_name: str, _: None = Depends(require_setup_token)):
    config_file = _config_path(config_name)

    if config_name == "nvim.tar.gz":
        return FileResponse(
            path=config_file,
            media_type="application/gzip",
            filename="nvim.tar.gz",
        )

    return PlainTextResponse(config_file.read_text().strip())


@router.get("/setup/ssh/keys", response_class=PlainTextResponse)
@router.get("/ssh/keys", response_class=PlainTextResponse, include_in_schema=False)
async def list_ssh_keys(_: None = Depends(require_setup_token)):
    ssh_keys_dir = _ssh_keys_dir()
    keys = [f.stem for f in ssh_keys_dir.glob("*.pub")]
    return "\n".join(keys)


@router.get("/setup/ssh/keys/all", response_class=PlainTextResponse)
@router.get("/ssh/keys/all", response_class=PlainTextResponse, include_in_schema=False)
async def get_all_ssh_keys(_: None = Depends(require_setup_token)):
    ssh_keys_dir = _ssh_keys_dir()
    all_keys = [key_file.read_text().strip() for key_file in ssh_keys_dir.glob("*.pub")]
    return "\n".join(all_keys)


@router.get("/setup/ssh/keys/{key_name}", response_class=PlainTextResponse)
@router.get("/ssh/keys/{key_name}", response_class=PlainTextResponse, include_in_schema=False)
async def get_ssh_key(key_name: str, _: None = Depends(require_setup_token)):
    ssh_keys_dir = _ssh_keys_dir()
    key_file = ssh_keys_dir / f"{key_name}.pub"
    if not key_file.exists():
        raise HTTPException(status_code=404, detail=f"SSH key '{key_name}' not found")
    return key_file.read_text().strip()
