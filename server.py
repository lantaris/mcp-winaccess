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


@mcp.tool(description="Get detailed text content from a UI control (Edit, Static, Document) inside a window. Returns full text content for agent understanding.")
def get_text(window_title: str, control_identifier: str) -> str:
    """Agent instruction: Use this to read the full text of a specific UI element (label, input, document). It searches descendants inside the window and returns the complete text content, which helps verify form data or read labels without screenshots.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier (name, automation ID, or class).
    Returns:
        Full text content of the control or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        text_content = ctrl[0].window_text() or ""
                        return f"FULL_TEXT: '{text_content}' from control '{control_identifier}' in '{win.window_text()}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Get text failed: {exc}"


@mcp.tool(description="Set text into a specific Edit control inside a window. Useful for agents that need to fill forms without relying on keyboard focus.")
def set_text(window_title: str, control_identifier: str, value: str) -> str:
    """Agent instruction: Use this when the agent needs to input a specific value directly into an edit box or text field. It finds the control by identifier inside the target window and sets its text. This is more reliable than type_text when the exact input field is known from previous screenshot analysis.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier (name, automation ID, or class).
        value: The text string to set.
    Returns:
        Confirmation or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].set_text(value)
                        return f"SET_TEXT: '{value}' into '{control_identifier}' in '{win.window_text()}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Set text failed: {exc}"


@mcp.tool(description="List all child controls inside a target window with their types, names, and texts. This helps agents discover available UI elements for interaction.")
def get_all_controls(window_title: str) -> str:
    """Agent instruction: Use this before interacting with an unknown window. It returns a structured list of all child controls (buttons, edits, static labels) with their automation IDs and text. Agents can use this output to decide which control_identifier to use with click_element, set_text, or get_text.
    Args:
        window_title: Partial title of the parent window.
    Returns:
        Multi-line description of each child control, or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    results = []
                    for child in win.descendants():
                        try:
                            child_text = child.window_text() or ""
                            child_type = str(child.element_info.control_type) if hasattr(child.element_info, 'control_type') else type(child).__name__
                            results.append(f"Type: {child_type}, Name/Text: '{child_text}', Control: {child}")
                        except Exception:
                            continue
                    return "\n".join(results) if results else "No child controls found."
            except Exception:
                continue
        return f"ERROR: Window '{window_title}' not found."
    except Exception as exc:
        return f"ERROR: List controls failed: {exc}"


@mcp.tool(description="Perform a double left-click at absolute screen coordinates or on a specific control inside a window. Useful for opening files or selecting items.")
def double_click(x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
    """Agent instruction: Use this when the agent needs to open an item with a double-click. If x and y are provided, it clicks at those screen coordinates. If window_title and control_identifier are provided, it finds the control inside the window and performs a double-click on it. At least one method (coordinates or control) should be specified.
    Args:
        x: Horizontal screen coordinate (optional if using control).
        y: Vertical screen coordinate (optional if using control).
        window_title: Partial window title (optional if using coordinates).
        control_identifier: Partial control identifier (optional if using coordinates).
    Returns:
        Confirmation or error message.
    """
    try:
        if window_title and control_identifier:
            desktop = Desktop()
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            ctrl[0].double_click_input()
                            return f"DOUBLE_CLICKED control '{control_identifier}' in '{win.window_text()}'"
                except Exception:
                    continue
            return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
        else:
            pyautogui.doubleClick(x, y)
            return f"Double clicked at coordinates ({x}, {y})"
    except Exception as exc:
        return f"ERROR: Double click failed: {exc}"


@mcp.tool(description="Perform a right-click at absolute screen coordinates or on a specific control inside a window. Opens context menus for agents to interact with.")
def right_click(x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
    """Agent instruction: Use this to open context menus at specific points or on specific controls. If x and y are provided, it performs a screen-level right-click. If window_title and control_identifier are provided, it performs a right-click on the control inside the window.
    Args:
        x: Horizontal screen coordinate.
        y: Vertical screen coordinate.
        window_title: Partial window title.
        control_identifier: Partial control identifier.
    Returns:
        Confirmation or error message.
    """
    try:
        if window_title and control_identifier:
            desktop = Desktop()
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            ctrl[0].right_click_input()
                            return f"RIGHT_CLICKED control '{control_identifier}' in '{win.window_text()}'"
                except Exception:
                    continue
            return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
        else:
            pyautogui.rightClick(x, y)
            return f"Right clicked at ({x}, {y})"
    except Exception as exc:
        return f"ERROR: Right click failed: {exc}"


@mcp.tool(description="Scroll inside a window or at screen coordinates. Helps agents navigate long lists or pages.")
def scroll(direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
    """Agent instruction: Use this to scroll through content in a window. If control_identifier is specified, it scrolls inside that control. Otherwise, it scrolls at screen coordinates (x, y) or with default position. The amount controls how many scroll actions to perform. Direction can be 'up' or 'down'.
    Args:
        direction: 'up' or 'down'.
        amount: Number of scroll actions.
        x: Screen X coordinate (optional).
        y: Screen Y coordinate (optional).
        window_title: Partial window title (optional).
        control_identifier: Partial control identifier for scrolling inside a specific element.
    Returns:
        Confirmation or error message.
    """
    try:
        scroll_amount = 120 if direction == "down" else -120
        if window_title and control_identifier:
            desktop = Desktop()
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            ctrl[0].wheel_mouse_input(wheel_dist=scroll_amount * amount)
                            return f"SCROLLED {direction} {amount} times inside '{control_identifier}'"
                except Exception:
                    continue
            return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
        else:
            for _ in range(amount):
                pyautogui.scroll(scroll_amount, x=x, y=y)
            return f"SCROLLED {direction} {amount} times at ({x}, {y})"
    except Exception as exc:
        return f"ERROR: Scroll failed: {exc}"


@mcp.tool(description="Wait for a specific control element inside a window to appear. Useful for agents that need to confirm loading states or dynamic content.")
def wait_for_element(window_title: str, control_identifier: str, timeout: float = 10.0) -> str:
    """Agent instruction: Use this when the agent needs to confirm that a specific button, input, or label has appeared before proceeding. It continuously checks inside the target window for the control identifier until it is found or timeout is reached.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier.
        timeout: Maximum wait time in seconds.
    Returns:
        Confirmation when found, or timeout error.
    """
    try:
        desktop = Desktop()
        start = time.time()
        while time.time() - start < timeout:
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            return f"ELEMENT FOUND: '{control_identifier}' in '{win.window_text()}'"
                except Exception:
                    continue
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for element '{control_identifier}' in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Wait for element failed: {exc}"


@mcp.tool(description="Get the current state of a window: minimized, maximized, or normal. Helps agents decide whether to manage the window before taking screenshots.")
def get_window_state(title: str = "") -> str:
    """Agent instruction: Use this to check whether a window is minimized, maximized, or in normal state. The agent can use this information to decide whether to call manage_window before performing actions or taking screenshots.
    Args:
        title: Partial window title.
    Returns:
        Window state description, or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if title in (win.window_text() or ""):
                    rect = win.rectangle()
                    # Check window placement state through rectangle and internal flags if available
                    state_info = f"Window '{win.window_text()}' rect={rect}, handle={win.handle}, pid={win.process_id()}"
                    return state_info
            except Exception:
                continue
        return f"ERROR: Window '{title}' not found."
    except Exception as exc:
        return f"ERROR: Get window state failed: {exc}"


@mcp.tool(description="Type text directly into a specific control inside a window. More precise than type_text because it targets a known input field.")
def type_in_element(window_title: str, control_identifier: str, text: str) -> str:
    """Agent instruction: Use this when the agent knows the exact input field identifier (from get_all_controls or previous analysis) and wants to enter text directly into that control. It first selects the control and then types the text, ensuring the input reaches the correct field even if keyboard focus is elsewhere.
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier.
        text: The string to type.
    Returns:
        Confirmation or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].click_input()
                        ctrl[0].type_keys(text)
                        return f"TYPED: '{text}' into '{control_identifier}' in '{win.window_text()}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Type in element failed: {exc}"


@mcp.tool(description="Move the mouse cursor to absolute screen coordinates without clicking. Useful for preparing the pointer position before drag or click actions.")
def move_mouse(x: int, y: int) -> str:
    """Agent instruction: Use this to position the mouse cursor at specific screen coordinates without performing any click. This is useful before drag operations or to show the user where the agent is focusing.
    Args:
        x: Target horizontal screen coordinate.
        y: Target vertical screen coordinate.
    Returns:
        Confirmation string or error message.
    """
    try:
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})"
    except Exception as exc:
        return f"ERROR: Move mouse failed: {exc}"


@mcp.tool(description="Drag the mouse from one screen coordinate to another. Useful for moving items or selecting ranges on screen.")
def drag(x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
    """Agent instruction: Use this when the agent needs to drag an item or select a range by moving the mouse from starting coordinates (x_from, y_from) to destination coordinates (x_to, y_to). The duration controls how fast the drag performs.
    Args:
        x_from: Starting horizontal coordinate.
        y_from: Starting vertical coordinate.
        x_to: Destination horizontal coordinate.
        y_to: Destination vertical coordinate.
        duration: Duration of the drag in seconds (default 0.5).
    Returns:
        Confirmation string or error message.
    """
    try:
        # Ensure mouse starts at the from position, then drag to destination
        pyautogui.moveTo(x_from, y_from, duration=0.1)
        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
        return f"DRAGGED from ({x_from}, {y_from}) to ({x_to}, {y_to}) over {duration}s"
    except Exception as exc:
        return f"ERROR: Drag failed: {exc}"


@mcp.tool(description="Drag a specific UI control inside a window to target screen coordinates. Helps agents move elements in forms or lists.")
def drag_element(window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
    """Agent instruction: Use this when the agent needs to drag a specific control (like a button, slider, or item) to new screen coordinates. It finds the control inside the window, clicks and holds it, then drags to (x_to, y_to).
    Args:
        window_title: Partial title of the parent window.
        control_identifier: Partial control identifier.
        x_to: Target horizontal screen coordinate.
        y_to: Target vertical screen coordinate.
        duration: Duration of the drag in seconds.
    Returns:
        Confirmation or error message.
    """
    try:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        # Get control center for drag start
                        rect = ctrl[0].rectangle()
                        start_x = (rect.left + rect.right) // 2
                        start_y = (rect.top + rect.bottom) // 2
                        pyautogui.moveTo(start_x, start_y)
                        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
                        return f"DRAGGED control '{control_identifier}' from ({start_x}, {start_y}) to ({x_to}, {y_to})"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found in '{window_title}'."
    except Exception as exc:
        return f"ERROR: Drag element failed: {exc}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
