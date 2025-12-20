# Config Files

This directory contains public configuration files exposed via the `/config/{config_name}` API endpoint.

## Files

- **claude.md** - Claude Code instructions (from `~/.claude/CLAUDE.md`)
- **tmux** - tmux configuration (from `~/.tmux.conf`)
- **nvim.tar.gz** - neovim configuration archive (from `~/.config/nvim/`)

## How to Update These Files

### Updating claude.md
```bash
cp ~/.claude/CLAUDE.md app/config/claude.md
```

### Updating tmux
```bash
cp ~/.tmux.conf app/config/tmux
```

### Updating nvim.tar.gz
```bash
tar -czf app/config/nvim.tar.gz -C ~/.config nvim/
```

## Security

The `app/routes/config.py` file uses a hardcoded whitelist (`ALLOWED_CONFIGS`) to prevent path traversal attacks. Only files explicitly listed in the whitelist can be served.

If you add a new config file, you must:
1. Add the file to this directory
2. Add the filename to the `ALLOWED_CONFIGS` list in `app/routes/config.py`

## API Endpoints

- `GET /config/claude.md` - Returns claude.md as plain text
- `GET /config/tmux` - Returns tmux config as plain text
- `GET /config/nvim.tar.gz` - Returns nvim archive for download

## Usage on Other Machines

```bash
# Download claude.md
curl https://bartmann.xyz/config/claude.md -o ~/.claude/CLAUDE.md

# Download tmux config
curl https://bartmann.xyz/config/tmux -o ~/.tmux.conf

# Download and extract nvim config
curl https://bartmann.xyz/config/nvim.tar.gz | tar -xzf - -C ~/.config/
```
