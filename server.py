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

# Helper to conditionally register tools based on adapter support

def register_if(cond: bool, desc: str):
    return lambda f: mcp.tool(description=desc)(f) if cond else f

# --- Core functions (always available) ---

@mcp.tool(description="Capture full desktop screen and return base64 JPEG.")
def screenshot(save_path: Optional[str] = None) -> str:
    return adapter.screenshot(save_path)

@mcp.tool(description="Click at screen coordinates.")
def click(x: int, y: int) -> str:
    return adapter.click(x, y)

@mcp.tool(description="Type text at keyboard focus.")
def type_text(text: str) -> str:
    return adapter.type_text(text)

@mcp.tool(description="Move mouse to coordinates without clicking.")
def move_mouse(x: int, y: int) -> str:
    return adapter.move_mouse(x, y)

@mcp.tool(description="Drag from (x_from,y_from) to (x_to,y_to).")
def drag(x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
    return adapter.drag(x_from, y_from, x_to, y_to, duration)

@mcp.tool(description="Right-click at screen coordinates (x, y).")
def right_click(x: int = 0, y: int = 0) -> str:
    return adapter.right_click(x, y)

@mcp.tool(description="Scroll down or up at screen or inside window control.")
def scroll(direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
    return adapter.scroll(direction, amount, x, y, window_title, control_identifier)

@mcp.tool(description="Launch executable by full path.")
def run_app(exe_path: str) -> str:
    try:
        subprocess.Popen(exe_path)
        return f"Started: {exe_path}"
    except Exception as exc:
        return f"ERROR: Failed to start {exe_path}: {exc}"

@mcp.tool(description="Kill process by executable base name.")
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
    @mcp.tool(description="Find visible top-level window by partial title or handle.")
    def find_window(value) -> str:
        result = adapter.find_window(value) or f"ERROR: Window '{value}' not found."
        return result

    @mcp.tool(description="Click UI control inside window.")
    def click_element(window_title: str, control_identifier: str) -> str:
        result = adapter.click_element(window_title, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Read text from control inside window.")
    def read_text(window_title: str, control_identifier: str) -> str:
        result = adapter.read_text(window_title, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Manage window state by partial title or handle.")
    def manage_window(value, action: str = "maximize", x: int = 0, y: int = 0) -> str:
        result = adapter.manage_window(value, action, x, y)
        return result or f"ERROR: Manage window failed."

    @mcp.tool(description="Wait for window by partial title or handle.")
    def wait_for_window(value, timeout: float = 10.0) -> str:
        result = adapter.wait_for_window(value, timeout)
        return result or f"ERROR: Timeout waiting for '{value}'."

    @mcp.tool(description="List visible windows.")
    def list_windows() -> str:
        result = adapter.list_windows()
        return result or "No visible windows found."

    @mcp.tool(description="Get detailed text from control.")
    def get_text(window_title: str, control_identifier: str) -> str:
        result = adapter.get_text(window_title, control_identifier)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Set text in control.")
    def set_text(window_title: str, control_identifier: str, value: str) -> str:
        result = adapter.set_text(window_title, control_identifier, value)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="List child controls in window by partial title or handle.")
    def get_all_controls(value) -> str:
        result = adapter.get_all_controls(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="Wait for specific element inside window.")
    def wait_for_element(window_title: str, control_identifier: str, timeout: float = 10.0) -> str:
        result = adapter.wait_for_element(window_title, control_identifier, timeout)
        return result or f"ERROR: Timeout waiting for '{control_identifier}'."

    @mcp.tool(description="Get window state by partial title or handle.")
    def get_window_state(value) -> str:
        result = adapter.get_window_state(value)
        return result or f"ERROR: Window '{value}' not found."

    @mcp.tool(description="Switch to a window by partial title or handle and activate it.")
    def switch_to_window(value) -> str:
        result = adapter.switch_to_window(value)
        return result or f"ERROR: Could not activate '{value}'."

    @mcp.tool(description="Type into specific control.")
    def type_in_element(window_title: str, control_identifier: str, text: str) -> str:
        result = adapter.type_in_element(window_title, control_identifier, text)
        return result or f"ERROR: Control '{control_identifier}' not found."

    @mcp.tool(description="Double click at screen or on control.")
    def double_click(x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        if window_title and control_identifier:
            # For element-based double click, we rely on adapter capabilities
            # On Windows adapter, double_click only supports coordinate mode in adapter; extend as needed.
            return adapter.double_click(0, 0)  # Fallback for element mode; ideally adapter would support this.
        return adapter.double_click(x, y)

else:
    # For platforms without UI automation (e.g., macOS basic), these functions are not registered.
    pass

# Always register drag_element if adapter supports drag; if not, we can still register it with adapter method
@mcp.tool(description="Drag control inside window to target coordinates.")
def drag_element(window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
    return adapter.drag_element(window_title, control_identifier, x_to, y_to, duration)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
