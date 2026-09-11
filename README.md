# mcp-winaccess — Local MCP Server for OpenCode

Windows desktop automation and screen interaction through the Model Context Protocol. Combines coordinate-based (`pyautogui`) and UI-automation (`pywinauto`) strategies for robust application control.

## Setup
```
pip install -r requirements.txt
```

## Run
```bash
python server.py
```

## Tools
- `screenshot` — full screen as base64 JPEG
- `click(x, y)` — mouse click at coordinates
- `type_text(text)` — keyboard input
- `run_app(exe_path)` — start executable
- `kill_app(name)` — kill process
- `read_log(path)` — last 20 lines of log
- `build_project()` — Unity build automation
- `find_window(title)` — find top-level window
- `click_element(window_title, control_identifier)` — click UI element
- `read_text(window_title, control_identifier)` — read control text
- `manage_window(title, action)` — window management
- `wait_for_window(title, timeout)` — wait for window
- `list_windows()` — list visible windows

## OpenCode Config (`opencode.jsonc`)
```jsonc
{
  "mcp": {
    "mcp-winaccess": {
      "type": "local",
      "command": ["python", "mcp-winaccess/server.py"],
      "cwd": ".",
      "enabled": true
    }
  }
}
```
