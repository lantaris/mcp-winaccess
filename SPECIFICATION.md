# Specification — mcp-winaccess

## Protocol
- MCP (Model Context Protocol) via `mcp` Python SDK v2 (`MCPServer`).
- Transport: stdio (local process spawned by OpenCode).

## Tools
### Vision / Screen
- `screenshot`: Capture full desktop screen and return it as base64 JPEG image. Optionally save to file.
- `click`: Click at absolute screen coordinates (x, y) using `pyautogui`.
- `type_text`: Type text string at current keyboard focus using `pyautogui`.

### Application Lifecycle
- `run_app`: Launch a Windows executable (`.exe`) by path.
- `kill_app`: Terminate a process by executable name (`taskkill`).

### File / Log
- `read_log`: Read the last 20 lines of a text log file.
- `build_project`: Run the Unity build batch script and return stdout/stderr.

### UI Automation (pywinauto)
- `find_window`: Find a top-level window by title or class name.
- `list_windows`: List visible top-level windows with title, class, PID, and rectangle.
- `click_element`: Click a control by automation identifier or handle inside a target window.
- `read_text`: Read text content from a control (Edit, Static, Document) inside a target window.
- `wait_for_window`: Wait until a window with given criteria appears.
- `manage_window`: Minimize, maximize, restore, or move a window by title.

## Dependencies
- Python 3.10+
- `mcp>=2.0.0`
- `pyautogui`
- `pywinauto`
- `Pillow`
- `pywin32`
