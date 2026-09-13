# mcp-winaccess

Cross-platform desktop automation via MCP adapter (`adapter/windows.py`, `adapter/linux.py`, `adapter/macos.py`).


## Usage Example

[![Видео](https://img.youtube.com/vi/W9ZyTohDu2Q/maxresdefault.jpg)](https://youtu.be/W9ZyTohDu2Q)

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
- `screenshot_base64()`: Captures full desktop screen and returns base64-encoded JPEG (`IMAGE_BASE64:...`). No parameters. Call when agent needs visual screen feedback.
- `screenshot_jpg(path: str)`: Captures full desktop screen and saves `.jpg` to the given file path (`path`). Returns confirmation with saved path. Call when agent needs to persist screenshot to disk.
- `click(x, y)`: Left-click at absolute screen coordinates (`x`, `y` pixels).
- `double_click(x=0, y=0)`: Double-click at absolute screen coordinates. If both `x` and `y` are `0`, uses current mouse position.
- `double_click_element(value, control_identifier="", x=0, y=0)`: Double-click a control inside a window (`value` = partial title `str` or handle `int`; `control_identifier` = index-based `ID` `element_N` or `AutoID`/`Name`). If `value` and `control_identifier` are provided, performs element-based double click at control center; otherwise uses coordinate mode.
- `right_click(x=0, y=0)`: Right-click at absolute screen coordinates. Defaults to current position when `x=y=0`.
- `drag(x_from, y_from, x_to, y_to, duration=0.5)`: Drag mouse from start (`x_from`, `y_from`) to end (`x_to`, `y_to`) over `duration` seconds.
- `drag_element(value, control_identifier, x_to, y_to, duration=0.5)`: Drag a UI control (`control_identifier` from `get_all_controls`) inside window (`value`) to target screen coordinates (`x_to`, `y_to`).
- `move_mouse(x, y)`: Move cursor to absolute coordinates (`x`, `y`) without clicking.
- `scroll(direction="down", amount=3, x=0, y=0)`: Scroll mouse wheel `down` or `up` at coordinates (`x`, `y`) for `amount` steps.
- `type_text(text)`: Type `text` at current keyboard focus.
- `run_app(exe_path)`: Launch executable at `exe_path`.
- `kill_app(name)`: Kill process by executable base name (`name`, without `.exe`) using `taskkill /F /IM`.
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

