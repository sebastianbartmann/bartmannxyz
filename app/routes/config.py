from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from pathlib import Path

router = APIRouter()

# Whitelist of allowed configs for security (prevents path traversal attacks)
ALLOWED_CONFIGS = ["claude.md", "tmux", "nvim.tar.gz"]


@router.get("/config/{config_name}")
async def get_config(config_name: str):
    # Security: whitelist only
    if config_name not in ALLOWED_CONFIGS:
        raise HTTPException(status_code=404, detail=f"Config '{config_name}' not found")

    config_dir = Path(__file__).parent.parent / "config"
    config_file = config_dir / config_name

    if not config_file.exists():
        raise HTTPException(status_code=404, detail=f"Config '{config_name}' not found")

    # Return archive file for nvim
    if config_name == "nvim.tar.gz":
        return FileResponse(
            path=config_file,
            media_type="application/gzip",
            filename="nvim.tar.gz"
        )

    # Return text files
    return PlainTextResponse(config_file.read_text().strip())
