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


@router.get("/config/")
async def get_install_guide():
    """
    Returns an LLM-friendly installation guide for all available configs.
    """
    guide = """# Development Environment Configuration Guide

This guide helps you install and configure development tools using configs from bartmann.xyz.

## Available Configurations

1. **Claude Code Instructions** (claude.md)
   - Personal instructions for Claude Code CLI
   - Location: ~/.claude/CLAUDE.md

2. **Tmux Configuration** (tmux)
   - Terminal multiplexer settings
   - Prefix: Ctrl+f
   - Location: ~/.tmux.conf

3. **Neovim Configuration** (nvim.tar.gz)
   - Complete Neovim setup with plugins
   - Location: ~/.config/nvim/

## Installation Commands

### Install All Configs
```bash
# Claude Code instructions
curl https://bartmann.xyz/config/claude.md -o ~/.claude/CLAUDE.md

# Tmux configuration
curl https://bartmann.xyz/config/tmux -o ~/.tmux.conf

# Neovim configuration (creates/overwrites ~/.config/nvim/)
curl https://bartmann.xyz/config/nvim.tar.gz | tar -xzf - -C ~/.config/
```

### Install Individual Configs

**Claude Code only:**
```bash
mkdir -p ~/.claude
curl https://bartmann.xyz/config/claude.md -o ~/.claude/CLAUDE.md
```

**Tmux only:**
```bash
curl https://bartmann.xyz/config/tmux -o ~/.tmux.conf
# Reload tmux config if already running:
tmux source-file ~/.tmux.conf
```

**Neovim only:**
```bash
curl https://bartmann.xyz/config/nvim.tar.gz | tar -xzf - -C ~/.config/
```

## Prerequisites

- **curl**: For downloading configs
- **tar**: For extracting nvim archive (usually pre-installed)
- **Claude Code**: Install from https://claude.com/claude-code
- **tmux**: Install via package manager (brew install tmux / apt install tmux)
- **neovim**: Install from https://neovim.io

## Important Notes

- These commands will **overwrite** existing configurations
- Backup your current configs before installing:
  ```bash
  cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup
  cp ~/.tmux.conf ~/.tmux.conf.backup
  cp -r ~/.config/nvim ~/.config/nvim.backup
  ```
- After installing tmux config, restart tmux or reload config
- After installing nvim config, restart neovim

## Verification

After installation, verify configs are in place:
```bash
ls -la ~/.claude/CLAUDE.md
ls -la ~/.tmux.conf
ls -la ~/.config/nvim/
```

## API Endpoints

- `GET /config/claude.md` - Claude Code instructions (text)
- `GET /config/tmux` - Tmux configuration (text)
- `GET /config/nvim.tar.gz` - Neovim config archive (gzip)
- `GET /config/` - This installation guide (text)
"""
    return PlainTextResponse(guide.strip())
