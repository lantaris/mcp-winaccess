#!/usr/bin/env python3
"""mcp-winaccess: cross-platform MCP server using adapter pattern (pyautogui + platform-specific automation)."""
import base64
import subprocess
import sys
from typing import Optional

from mcp.server.mcpserver import MCPServer
from adapter import get_adapter

adapter = get_adapter()

mcp = MCPServer("mcp-winaccess")


# --- Core functions (always available) ---

@mcp.tool(description="Capture full desktop screen and return a base64-encoded JPEG string. Optional save_path saves the image to disk. Returns format: IMAGE_BASE64:{base64_string}.")
def screenshot(save_path: Optional[str] = None) -> str:
    return adapter.screenshot(save_path)

@mcp.tool(description="Perform a left mouse click at absolute screen coordinates (x, y). Returns confirmation with coordinates.")
def click(x: int, y: int) -> str:
    return adapter.click(x, y)

@mcp.tool(description="Perform a double mouse click at absolute screen coordinates (x, y). Defaults to (0, 0) for current position. Returns confirmation.")
def double_click(x: int = 0, y: int = 0) -> str:
    return adapter.double_click(x, y)

@mcp.tool(description="Type the provided text string at the current keyboard focus using pyautogui. Returns confirmation with typed text.")
def type_text(text: str) -> str:
    return adapter.type_text(text)

@mcp.tool(description="Move the mouse cursor to absolute screen coordinates (x, y) without clicking. Returns confirmation with target coordinates.")
def move_mouse(x: int, y: int) -> str:
    return adapter.move_mouse(x, y)

@mcp.tool(description="Drag the mouse from start coordinates (x_from, y_from) to end coordinates (x_to, y_to) with optional duration in seconds (default 0.5). Returns drag confirmation.")
def drag(x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
    return adapter.drag(x_from, y_from, x_to, y_to, duration)

@mcp.tool(description="Perform a right-click at absolute screen coordinates (x, y). Defaults to (0, 0) for current position. Returns confirmation.")
def right_click(x: int = 0, y: int = 0) -> str:
    return adapter.right_click(x, y)

@mcp.tool(description="Scroll the mouse wheel down or up at screen coordinates (x, y) for a specified number of steps (amount, default 3). Direction is 'down' or 'up'. Returns scroll confirmation.")
def scroll(direction: str = "down", amount: int = 3, x: int = 0, y: int = 0) -> str:
    return adapter.scroll(direction, amount, x, y)

@mcp.tool(description="Launch an executable by providing its full file path (exe_path). Starts the process using subprocess.Popen. Returns start confirmation or error.")
def run_app(exe_path: str) -> str:
    try:
        subprocess.Popen(exe_path)
        return f"Started: {exe_path}"
    except Exception as exc:
        return f"ERROR: Failed to start {exe_path}: {exc}"

@mcp.tool(description="Kill a running process by its executable base name (name, without .exe). Uses Windows taskkill /F /IM. Returns kill status or error.")
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
    @mcp.tool(description="Find a visible top-level window by partial title (str) or window handle (int). Returns window info including title, class, handle, pid, and rectangle.")
    def find_window(value) -> str:
        result = adapter.find_window(value) or f"ERROR: Window '{value}' not found."
        return result

    @mcp.tool(description="Click a UI control inside a window. Parameters: window_title (partial title or handle int), control_identifier (index-based ID 'element_N' or AutoID/Name from get_all_controls). Returns click confirmation or error.")
    def click_element(value, control_identifier: str) -> str:
        result = adapter.click_element(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Read the text content from a UI control inside a window. Uses window_title (partial title/handle) and control_identifier (element_N/AutoID/Name). Returns text or error.")
    def read_text(value, control_identifier: str) -> str:
        result = adapter.read_text(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Manage a window state: minimize, maximize, restore, or move. Parameters: value (window title or handle int), action ('minimize'|'maximize'|'restore'|'move'), x and y (for move). Returns status or error.")
    def manage_window(value, action: str = "maximize", x: int = 0, y: int = 0) -> str:
        result = adapter.manage_window(value, action, x, y)
        return result or f"ERROR: Manage window failed."

    @mcp.tool(description="Wait for a top-level window to appear. Parameters: value (partial title or handle int), timeout in seconds (default 10.0). Returns confirmation or timeout error.")
    def wait_for_window(value, timeout: float = 10.0) -> str:
        result = adapter.wait_for_window(value, timeout)
        return result or f"ERROR: Timeout waiting for '{value}'."

    @mcp.tool(description="List all visible top-level windows with their title, class, PID, and rectangle. Returns a formatted list or 'No visible windows found'.")
    def list_windows() -> str:
        result = adapter.list_windows()
        return result or "No visible windows found."

    @mcp.tool(description="Get detailed text from a control inside a window. Parameters: window_title (partial title/handle), control_identifier (element_N/AutoID/Name). Returns text or error.")
    def get_text(value, control_identifier: str) -> str:
        result = adapter.get_text(value, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Set text into an editable control inside a window. Parameters: window_title, control_identifier (element_N/AutoID/Name), value (text to set). Returns confirmation or error.")
    def set_text(value, control_identifier: str, value_text: str) -> str:
        result = adapter.set_text(value, control_identifier, value_text)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="List all child controls inside a window. Parameter: value (window partial title or handle int). Returns list with index-based IDs 'element_N', AutoID, Name, Class, Type, Text, Handle. Agents should use the 'ID' value for interaction.")
    def get_all_controls(value) -> str:
        result = adapter.get_all_controls(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="Wait for a specific UI element (control) to appear inside a window. Parameters: window_title, control_identifier (element_N/AutoID/Name), timeout in seconds (default 10.0). Returns confirmation or timeout error.")
    def wait_for_element(value, control_identifier: str, timeout: float = 10.0) -> str:
        result = adapter.wait_for_element(value, control_identifier, timeout)
        return result or f"ERROR: Timeout waiting for '{control_identifier}'."

    @mcp.tool(description="Get the current state info of a window by partial title or handle (int). Returns window title, rectangle, handle, and PID.")
    def get_window_state(value) -> str:
        result = adapter.get_window_state(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="Switch focus to a window by partial title or handle (int) and activate it. Restores and sets focus. Returns activation confirmation or error.")
    def switch_to_window(value) -> str:
        result = adapter.switch_to_window(value)
        return result or f"ERROR: Could not activate '{value}'."

    @mcp.tool(description="Type text directly into a specific control inside a window. Parameters: window_title, control_identifier (element_N/AutoID/Name), text. Returns confirmation or error.")
    def type_in_element(value, control_identifier: str, text: str) -> str:
        result = adapter.type_in_element(value, control_identifier, text)
        return result or f"ERROR: Control '{control_identifier}' not found."


    @mcp.tool(description="Perform a double click on a specific control inside a window. Parameters: value (window partial title or handle int), control_identifier (element_N/AutoID/Name), x and y (optional coordinate fallback, default 0). If value and control_identifier are provided, performs element-based double click at control center; otherwise coordinate mode.")
    def double_click_element(value, control_identifier: str = "", x: int = 0, y: int = 0) -> str:
        if value and control_identifier:
            return adapter.double_click_element(value, control_identifier)
        return adapter.double_click_element("", "", x, y)

    @mcp.tool(description="Drag a UI control inside a window to target screen coordinates (x_to, y_to) with optional duration (default 0.5). Parameters: value (window partial title or handle int), control_identifier (element_N/AutoID/Name from get_all_controls), x_to, y_to, duration.")
    def drag_element(value, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        return adapter.drag_element(value, control_identifier, x_to, y_to, duration)

else:
    # For platforms without UI automation (e.g., macOS basic), these functions are not registered.
    pass

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
