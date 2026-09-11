#!/usr/bin/env python3
"""mcp-winaccess: MCP server for full Windows desktop automation using both coordinate-based (pyautogui) and UI-Automation (pywinauto) strategies, designed for vision-language models that receive text prompts and screen images."""
import base64
import subprocess
import time
from typing import Optional

import pyautogui
from PIL import Image
from mcp.server.mcpserver import MCPServer

try:
    from pywinauto import Application, Desktop
except ImportError as exc:
    raise ImportError("pywinauto is required. Install it with: pip install pywinauto") from exc

mcp = MCPServer("mcp-winaccess")


@mcp.tool(description="Capture the full desktop screen and return it as a base64-encoded JPEG string so the vision model can see the current Windows UI state. Optionally save to a file path.")
def screenshot(save_path: Optional[str] = None) -> str:
    """Capture full desktop screen and return base64 JPEG image for vision-model input.
    Args:
        save_path: Optional file path to save PNG screenshot.
    Returns:
        String starting with 'IMAGE_BASE64:' followed by base64 data, or error message.
    """
    try:
        img = pyautogui.screenshot()
        if save_path:
            img.save(save_path)
        img_bytes = img.tobytes()  # PIL Image.tobytes requires format for encode
        # Actually pyautogui.screenshot() returns PIL Image; let's encode properly
        buffer = img.tobytes()  # This is raw; we need encode via save to BytesIO
        import io
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"IMAGE_BASE64:{b64_str}"
    except Exception as exc:
        return f"ERROR: Screenshot failed: {exc}"


@mcp.tool(description="Move mouse to absolute screen coordinates (x, y) and perform a single left-click. Use this when the vision model identifies targets by pixel position on the screenshot.")
def click(x: int, y: int) -> str:
    """Click at screen coordinates. For vision models: provide (x, y) derived from the screenshot analysis.
    Args:
        x: Horizontal pixel coordinate.
        y: Vertical pixel coordinate.
    Returns:
        Confirmation string or error.
    """
    try:
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})"
    except Exception as exc:
        return f"ERROR: Click failed: {exc}"


@mcp.tool(description="Type a text string using the keyboard at the current focus. The interval between keystrokes is 0.05 seconds. Useful for entering data into focused input fields.")
def type_text(text: str) -> str:
    """Type text at current keyboard focus.
    Args:
        text: The string to type.
    Returns:
        Confirmation of typed text.
    """
    try:
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"
    except Exception as exc:
        return f"ERROR: Type text failed: {exc}"


@mcp.tool(description="Launch a Windows executable file by its full path. Starts the process asynchronously. Use this to open applications for automation.")
def run_app(exe_path: str = "C:\\Users\\user\\OpenCode\\ugame\\Build\\UGAME.exe") -> str:
    """Run a Windows executable.
    Args:
        exe_path: Full file system path to the .exe file.
    Returns:
        Confirmation or error.
    """
    try:
        subprocess.Popen(exe_path)
        return f"Started: {exe_path}"
    except Exception as exc:
        return f"ERROR: Failed to start {exe_path}: {exc}"


@mcp.tool(description="Kill a Windows process by its executable base name (without .exe). Uses Windows taskkill forcefully. Use this to close applications after automation.")
def kill_app(name: str = "UGAME") -> str:
    """Kill process by executable base name.
    Args:
        name: Base name of the executable, e.g., 'UGAME' (not 'UGAME.exe').
    Returns:
        Confirmation or error.
    """
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", f"{name}.exe"],
            capture_output=True,
            text=True
        )
        return f"Killed: {name} (exit={result.returncode}, stdout={result.stdout}, stderr={result.stderr})"
    except Exception as exc:
        return f"ERROR: Kill failed: {exc}"


@mcp.tool(description="Read the last 20 lines of a text file (e.g., application log). Returns the lines as a single string. If the file does not exist or cannot be read, an error message is returned.")
def read_log(path: str = "C:\\Users\\user\\AppData\\LocalLow\\DefaultCompany\\ugame\\ugame_log.txt") -> str:
    """Read the last 20 lines of a text log file.
    Args:
        path: Full file system path to the log file.
    Returns:
        Last 20 lines joined by newline, or error message.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()
        return "\n".join(lines[-20:])
    except Exception as exc:
        return f"ERROR: Reading log failed: {exc}"


@mcp.tool(description="Execute the Unity build automation batch script (BuildProject.bat) and return stdout/stderr. The model should call this when a build step is required.")
def build_project() -> str:
    """Run Unity build automation by invoking the batch script.
    Args: None.
    Returns:
        Combined stdout and stderr from the build process.
    """
    try:
        result = subprocess.run(
            ["cmd", "/c", "C:\\Users\\user\\OpenCode\\ugame\\BuildProject.bat"],
            capture_output=True,
            text=True
        )
        return f"Build output:\n{result.stdout}\n{result.stderr}"
    except Exception as exc:
        return f"ERROR: Build failed: {exc}"


@mcp.tool(description="Find a visible top-level window by partial title or class name using pywinauto. Returns window details (handle, PID, rectangle, title) or an error if not found.")
def find_window(title: str = "") -> str:
    """Find top-level window by partial title or class name.
    Args:
        title: Substring of the window title or class name.
    Returns:
        JSON-like string with handle, PID, rectangle, title.
    """
    try:
        desktop = Desktop()
        windows = desktop.windows()
        for win in windows:
            try:
                win_text = win.window_text() or ""
                win_class = win.class_name() or ""
                if title in win_text or title in win_class:
                    rect = win.rectangle()
                    return f"Found window: title={win_text}, class={win_class}, handle={win.handle}, pid={win.process_id()}, rect={rect}"
            except Exception:
                continue
        return f"ERROR: Window with '{title}' not found."
    except Exception as exc:
        return f"ERROR: Window search failed: {exc}"


@mcp.tool(description="Click a UI control inside a target window by automation identifier (title, name, or automation ID). This is more robust than coordinate clicking when the UI layout changes.")
def click_element(window_title: str, control_identifier: str) -> str:
    """Click a control inside a window using pywinauto UI Automation.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control name, automation ID, or class name.
    Returns:
        Confirmation or error.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.child_window(control_type="Button", title_re=control_identifier)
                    # More general approach: try to find by any property
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].click_input()
                        return f"Clicked control '{control_identifier}' in '{win.window_text()}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Click element failed: {exc}"


@mcp.tool(description="Read text content from a UI control (Edit, Static, Document) inside a target window. Useful for verifying form input or reading labels without screenshots.")
def read_text(window_title: str, control_identifier: str) -> str:
    """Read text from a UI control inside a window.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier.
    Returns:
        Extracted text or error.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        text_content = ctrl[0].window_text()
                        return f"Text from control '{control_identifier}' in '{win.window_text()}': {text_content}"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Read text failed: {exc}"


@mcp.tool(description="Manage a top-level window by title: actions include 'minimize', 'maximize', 'restore', 'move' (with x, y). This helps prepare the UI for vision-model observation.")
def manage_window(title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> str:
    """Manage window state (minimize, maximize, restore, move).
    Args:
        title: Partial window title.
        action: One of minimize, maximize, restore, move.
        x: Target X coordinate for move (ignored otherwise).
        y: Target Y coordinate for move (ignored otherwise).
    Returns:
        Confirmation or error.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if title in (win.window_text() or ""):
                    if action == "minimize":
                        win.minimize()
                        return f"Minimized window: {win.window_text()}"
                    elif action == "maximize":
                        win.maximize()
                        return f"Maximized window: {win.window_text()}"
                    elif action == "restore":
                        win.restore()
                        return f"Restored window: {win.window_text()}"
                    elif action == "move":
                        rect = win.rectangle()
                        win.move_window(x=x, y=y)
                        return f"Moved window '{win.window_text()}' to ({x}, {y})"
                    else:
                        return f"ERROR: Unknown action '{action}'."
            except Exception:
                continue
        return f"ERROR: Window '{title}' not found."
    except Exception as exc:
        return f"ERROR: Manage window failed: {exc}"


@mcp.tool(description="Wait for a window with the given partial title or class name to appear, with an optional timeout in seconds. Default timeout is 10 seconds. Returns confirmation when found or timeout error.")
def wait_for_window(title: str = "", timeout: float = 10.0) -> str:
    """Wait until a window with given criteria appears.
    Args:
        title: Partial window title or class name.
        timeout: Maximum wait time in seconds.
    Returns:
        Confirmation string or timeout error.
    """
    try:
        desktop = Desktop()
        start = time.time()
        while time.time() - start < timeout:
            for win in desktop.windows():
                try:
                    win_text = win.window_text() or ""
                    win_class = win.class_name() or ""
                    if title in win_text or title in win_class:
                        return f"Window '{title}' found (title={win_text})."
                except Exception:
                    continue
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{title}'."
    except Exception as exc:
        return f"ERROR: Wait for window failed: {exc}"


@mcp.tool(description="List all visible top-level windows with their titles, class names, PIDs, and screen rectangles. This gives the vision model awareness of available UI contexts.")
def list_windows() -> str:
    """List visible top-level windows for vision-model context awareness.
    Args: None.
    Returns:
        Multi-line description of each visible window.
    """
    try:
        desktop = Desktop()
        results = []
        for win in desktop.windows():
            try:
                results.append(f"Title: '{win.window_text()}', Class: '{win.class_name()}', PID: {win.process_id()}, Rect: {win.rectangle()}")
            except Exception:
                continue
        return "\n".join(results) if results else "No visible windows found."
    except Exception as exc:
        return f"ERROR: List windows failed: {exc}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
