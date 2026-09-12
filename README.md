# mcp-winaccess

Cross-platform desktop automation via MCP adapter (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`).


## Usage Example

<iframe width="560" height="315" src="https://www.youtube.com/embed/W9ZyTohDu2Q" title="Usage Example" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Install

```
pip install mcp-winaccess
uv tool install mcp-winaccess
```

## Run

```
uvx mcp-winaccess
```

Or directly:
```
python server.py
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

## Tools

### Always Available
- `screenshot(save_path?)`: Full screen base64 JPEG.
- `click(x, y)`: Left-click at screen coordinates.
- `double_click(x=0, y=0)`: Double-click at screen coordinates (coordinate mode only).
- `double_click_element(value, control_identifier="", x=0, y=0)`: Double-click a control by index-based `ID` (`element_N`) or `AutoID`/`Name`; `value` is partial window title (`str`) or handle (`int`).
- `right_click(x=0, y=0)`: Right-click at screen coordinates.
- `drag(x_from, y_from, x_to, y_to, duration?)`: Drag mouse.
- `drag_element(value, control_identifier, x_to, y_to, duration?)`: Drag control to target; `value` is partial title (`str`) or handle (`int`).
- `move_mouse(x, y)`: Move cursor without clicking.
- `scroll(direction="down", amount=3, x=0, y=0)`: Scroll down or up at screen coordinates. Note: `value`/`control_identifier` removed in v1.0.1+.
- `type_text(text)`: Type text at keyboard focus.
- `run_app(exe_path?)`: Launch executable.
- `kill_app(name?)`: Kill process.
- `switch_to_window(value)`: Restore and activate window by partial title (`str`) or handle (`int`).

### Window Automation (Windows / Linux with `pywinauto` / `pyatspi`)
- `find_window(value?)`: Find visible top-level window by partial title (`str`) or handle (`int`). Returns info with title, class, handle, pid, rect.
- `list_windows()`: List visible windows.
- `click_element(value, control_identifier)`: Click UI control inside window. `value` = partial title (`str`) or handle (`int`); `control_identifier` = index-based `ID` (`element_0`) or `AutoID`/`Name`.
- `read_text(value, control_identifier)`: Read control text by `ID`.
- `manage_window(value, action="maximize", x=0, y=0)`: Manage window state (`minimize`/`maximize`/`restore`/`move`). `value` = title (`str`) or handle (`int`).
- `wait_for_window(value, timeout?)`: Wait for window by partial title (`str`) or handle (`int`).
- `get_all_controls(value)`: List child controls inside window (`value` = title `str` or handle `int`). Returns index-based IDs (`element_0`, `element_5`), `AutoID`, `Name`, `Class`, `Type`, `Text`, `Handle`. Agents must use the `ID` value (e.g., `element_5`) as `control_identifier` for interaction with controls.
- `wait_for_element(value, control_identifier, timeout?)`: Wait for control by `ID`.
- `get_window_state(value)`: Window state info (`str` or `int`).
- `get_text(value, control_identifier)`: Full text from control.
- `set_text(value, control_identifier, value_text)`: Set text in edit control.
- `type_in_element(value, control_identifier, text)`: Type directly into control.


Unsupported functions are hidden from MCP on each platform.

