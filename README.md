# mcp-winaccess

Cross-platform desktop automation via MCP adapter (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`).

## Install

```bash
# pip
pip install mcp-winaccess
# uv
uv tool install mcp-winaccess
# or
uv pip install mcp-winaccess
```

## Run

```bash
uvx mcp-winaccess
```

Or directly:
```bash
python server.py
```

Or with adapter module:
```bash
python -m adapter
```

## OpenCode Config (`opencode.jsonc`)

```jsonc
{
  "mcp": {
    "winaccess": {
      "type": "local",
      "command": [
        "uvx",
        "mcp-winaccess"
      ],
      "enabled": true
    }
  }
}
```

## Unavailable functions by platform

- **Windows** (`pywinauto` + `pyautogui`): none unavailable (all 22 functions available).
- **Linux** (`pyatspi` + `pyautogui`): unavailable — `manage_window`, `get_all_controls`, `wait_for_element`, `get_window_state`, `set_text`, `type_in_element`, `drag_element` (return errors).
- **macOS** (`pyautogui` only): unavailable — all window automation functions (`find_window`, `list_windows`, `click_element`, `read_text`, `manage_window`, `wait_for_window`, `get_text`, `set_text`, `get_all_controls`, `wait_for_element`, `get_window_state`, `type_in_element`, `double_click` (on element), `drag_element`).

Unsupported functions are hidden from MCP on each platform.
