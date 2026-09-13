#!/usr/bin/env python3
"""mcp-winaccess: cross-platform MCP server using adapter pattern (pyautogui + platform-specific automation)."""
import subprocess
import sys

from mcp.server.mcpserver import MCPServer
from adapter import get_adapter

adapter = get_adapter()

mcp = MCPServer("mcp-winaccess")


# --- Core functions (always available) ---

@mcp.tool(description="screenshot_base64: Captures full desktop screen and returns base64-encoded JPEG string. Return format is IMAGE_BASE64:{base64_string}. No parameters required. Call this when the agent needs visual feedback of the current screen state.")
def screenshot_base64() -> str:
    return adapter.screenshot_base64()

@mcp.tool(description="screenshot_jpg: Captures full desktop screen and saves it as a JPEG file to the specified path. Parameter: path (str) — absolute or relative file path where the .jpg should be saved. Returns confirmation string with saved path. Call this when agent needs to persist screenshot to disk.")
def screenshot_jpg(path: str) -> str:
    return adapter.screenshot_jpg(path)

@mcp.tool(description="click: Performs a left mouse click at absolute screen coordinates. Parameters: x (int) — horizontal coordinate in pixels; y (int) — vertical coordinate in pixels. Returns confirmation string with coordinates clicked. Use for clicking buttons, links, or any UI element by known position.")
def click(x: int, y: int) -> str:
    return adapter.click(x, y)

@mcp.tool(description="double_click: Performs a double mouse click at absolute screen coordinates. Parameters: x (int, default=0) — horizontal coordinate; y (int, default=0) — vertical coordinate. If both are 0, clicks at current mouse position. Returns confirmation. Use for opening files or activating items by double-click.")
def double_click(x: int = 0, y: int = 0) -> str:
    return adapter.double_click(x, y)

@mcp.tool(description="type_text: Types the provided text string at the current keyboard focus using pyautogui. Parameter: text (str) — the text to type. Returns confirmation with typed text. Use after focusing an input field (e.g., click first, then type_text).")
def type_text(text: str) -> str:
    return adapter.type_text(text)

@mcp.tool(description="move_mouse: Moves the mouse cursor to absolute screen coordinates without clicking. Parameters: x (int) — horizontal pixel coordinate; y (int) — vertical pixel coordinate. Returns confirmation with target coordinates. Use before clicking to position cursor precisely.")
def move_mouse(x: int, y: int) -> str:
    return adapter.move_mouse(x, y)

@mcp.tool(description="drag: Drags the mouse from start coordinates to end coordinates with optional duration. Parameters: x_from (int) — start X; y_from (int) — start Y; x_to (int) — end X; y_to (int) — end Y; duration (float, default=0.5) — drag time in seconds. Returns drag confirmation. Use for selecting text, moving sliders, or resizing elements.")
def drag(x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
    return adapter.drag(x_from, y_from, x_to, y_to, duration)

@mcp.tool(description="right_click: Performs a right-click at absolute screen coordinates. Parameters: x (int, default=0) — horizontal coordinate; y (int, default=0) — vertical coordinate. If both are 0, clicks at current mouse position. Returns confirmation. Use for opening context menus.")
def right_click(x: int = 0, y: int = 0) -> str:
    return adapter.right_click(x, y)

@mcp.tool(description="scroll: Scrolls the mouse wheel down or up at specified screen coordinates. Parameters: direction (str, default='down') — 'down' or 'up'; amount (int, default=3) — number of scroll steps; x (int, default=0) — horizontal coordinate; y (int, default=0) — vertical coordinate. Returns scroll confirmation. Use for navigating long pages or lists.")
def scroll(direction: str = "down", amount: int = 3, x: int = 0, y: int = 0) -> str:
    return adapter.scroll(direction, amount, x, y)

@mcp.tool(description="run_app: Launches an executable by providing its full file path. Parameter: exe_path (str) — absolute path to the executable file. Starts process via subprocess.Popen. Returns start confirmation or error message. Use for opening applications or scripts.")
def run_app(exe_path: str) -> str:
    try:
        subprocess.Popen(exe_path)
        return f"Started: {exe_path}"
    except Exception as exc:
        return f"ERROR: Failed to start {exe_path}: {exc}"

@mcp.tool(description="kill_app: Kills a running process by its executable base name (without .exe extension). Parameter: name (str) — base executable name (e.g., 'notepad'). Uses Windows taskkill /F /IM internally. Returns kill status or error. Use to terminate unresponsive applications.")
def kill_app(name: str) -> str:
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", f"{name}.exe"],
            capture_output=True, text=True
        )
        return f"Killed: {name} (exit={result.returncode})"
    except Exception as exc:
        return f"ERROR: Kill failed: {exc}"

# --- Window automation (conditional based on adapter) ---

if adapter.supports_ui_automation:
    @mcp.tool(description="find_window: Finds a visible top-level window by partial title or window handle. Parameter: value (str or int) — partial window title substring or integer handle. Returns formatted info string with title, class, handle, PID, and rectangle, or error if not found. Call before interacting with unknown windows.")
    def find_window(value) -> str:
        result = adapter.find_window(value) or f"ERROR: Window '{value}' not found."
        return result

    @mcp.tool(description="click_element: Clicks a specific UI control inside a window. Parameters: value (str or int) — partial window title or handle; control_identifier (str) — index-based ID (e.g., 'element_0', 'element_5') or AutoID/Name from get_all_controls. Returns click confirmation or error. Call after get_all_controls to identify the correct control_identifier.")
    def click_element(value, control_identifier: str) -> str:
        result = adapter.click_element(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="read_text: Reads text content from a UI control inside a window. Parameters: value (str or int) — partial window title or handle; control_identifier (str) — index-based ID or AutoID/Name. Returns text content or error. Use to extract labels, messages, or field values.")
    def read_text(value, control_identifier: str) -> str:
        result = adapter.read_text(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="manage_window: Manages the state of a window. Parameters: value (str or int) — partial title or handle; action (str, default='maximize') — one of 'minimize', 'maximize', 'restore', 'move'; x (int, default=0) and y (int, default=0) — coordinates for 'move' action only. Returns status confirmation or error. Use to bring windows to front or rearrange workspace.")
    def manage_window(value, action: str = "maximize", x: int = 0, y: int = 0) -> str:
        result = adapter.manage_window(value, action, x, y)
        return result or f"ERROR: Manage window failed."

    @mcp.tool(description="wait_for_window: Waits for a top-level window to appear, with timeout. Parameters: value (str or int) — partial title or handle; timeout (float, default=10.0) — maximum wait time in seconds. Returns confirmation when found, or timeout error. Use when launching apps and waiting for their windows.")
    def wait_for_window(value, timeout: float = 10.0) -> str:
        result = adapter.wait_for_window(value, timeout)
        return result or f"ERROR: Timeout waiting for '{value}'."

    @mcp.tool(description="list_windows: Lists all visible top-level windows. No parameters required. Returns formatted list with title, class, PID, and rectangle for each window, or 'No visible windows found'. Call first to discover available windows before other window operations.")
    def list_windows() -> str:
        result = adapter.list_windows()
        return result or "No visible windows found."

    @mcp.tool(description="get_text: Gets full text content from a UI control inside a window. Parameters: value (str or int) — window identifier; control_identifier (str) — index-based ID or AutoID/Name. Alias for read_text. Returns text or error.")
    def get_text(value, control_identifier: str) -> str:
        result = adapter.get_text(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="set_text: Sets text into an editable control inside a window. Parameters: value (str or int) — window identifier; control_identifier (str) — index-based ID or AutoID/Name; value_text (str) — text to insert. Returns confirmation or error. Use for filling input forms.")
    def set_text(value, control_identifier: str, value_text: str) -> str:
        result = adapter.set_text(value, control_identifier, value_text)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="get_all_controls: Lists all child controls inside a window. Parameter: value (str or int) — partial window title or handle. Returns index-based IDs ('element_0', 'element_5') plus AutoID, Name, Class, Type, Text, Handle for each control. Agents must use the 'ID' value (e.g., 'element_5') as control_identifier for click_element, set_text, read_text, wait_for_element, etc. Call before interacting with unknown windows.")
    def get_all_controls(value) -> str:
        result = adapter.get_all_controls(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="wait_for_element: Waits for a specific UI element (control) to appear inside a window. Parameters: value (str or int) — window identifier; control_identifier (str) — index-based ID or AutoID/Name; timeout (float, default=10.0) — max wait seconds. Returns confirmation when found, or timeout error. Use after get_all_controls to ensure control exists before interaction.")
    def wait_for_element(value, control_identifier: str, timeout: float = 10.0) -> str:
        result = adapter.wait_for_element(value, control_identifier, timeout)
        return result or f"ERROR: Timeout waiting for '{control_identifier}'."

    @mcp.tool(description="get_window_state: Gets state info of a window. Parameter: value (str or int) — partial title or handle. Returns window title, rectangle, handle, and PID, or error if not found. Use to verify window position and identity.")
    def get_window_state(value) -> str:
        result = adapter.get_window_state(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="switch_to_window: Switches focus to a window and activates it. Parameter: value (str or int) — partial title or handle. Restores and sets focus. Returns activation confirmation or error. Use before interacting with background windows.")
    def switch_to_window(value) -> str:
        result = adapter.switch_to_window(value)
        return result or f"ERROR: Could not activate '{value}'."

    @mcp.tool(description="type_in_element: Types text directly into a specific control inside a window. Parameters: value (str or int) — window identifier; control_identifier (str) — index-based ID or AutoID/Name; text (str) — text to type. Returns confirmation or error. More precise than click + type_text for form filling.")
    def type_in_element(value, control_identifier: str, text: str) -> str:
        result = adapter.type_in_element(value, control_identifier, text)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="double_click_element: Performs a double click on a specific control inside a window, or at screen coordinates. Parameters: value (str or int) — partial window title or handle; control_identifier (str, default='') — index-based ID or AutoID/Name; x (int, default=0) and y (int, default=0) — coordinate fallback. If value and control_identifier are provided, performs element-based double click at control center; otherwise uses coordinate mode. Returns confirmation or error.")
    def double_click_element(value, control_identifier: str = "", x: int = 0, y: int = 0) -> str:
        if value and control_identifier:
            return adapter.double_click_element(value, control_identifier)
        return adapter.double_click_element("", "", x, y)

    @mcp.tool(description="drag_element: Drags a UI control inside a window to target screen coordinates. Parameters: value (str or int) — window identifier; control_identifier (str) — index-based ID or AutoID/Name from get_all_controls; x_to (int) — target X; y_to (int) — target Y; duration (float, default=0.5) — drag duration in seconds. Returns drag confirmation or error. Use for moving sliders, rearranging items, or resizing within windows.")
    def drag_element(value, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        return adapter.drag_element(value, control_identifier, x_to, y_to, duration)

else:
    # For platforms without UI automation (e.g., macOS basic), these functions are not registered.
    pass


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
