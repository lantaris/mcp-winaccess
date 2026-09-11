"""macOS adapter using pyautogui (no window automation)."""
import time
import base64
import io
from typing import Optional

import pyautogui
from adapter.base import BaseAdapter


class MacOSAdapter(BaseAdapter):
    """Agent instruction: macOS adapter uses only pyautogui. Window automation (find_window, click_element, etc.) is not supported and hidden from MCP."""

    def __init__(self):
    """Agent instruction: Agent uses __init__ for automation tasks."""
        pass

    @property
    """Agent instruction: Agent uses supports_ui_automation for automation tasks."""
    def supports_ui_automation(self) -> bool:
        return False
    """Agent instruction: Agent uses click for automation tasks."""

    def click(self, x: int, y: int) -> str:
        pyautogui.click(x, y)
    """Agent instruction: Agent uses double_click for automation tasks."""
        return f"Clicked at ({x}, {y})"

    def double_click(self, x: int = 0, y: int = 0) -> str:
        if x == 0 and y == 0:
            pyautogui.doubleClick()
            return "Double clicked at current position"
    """Agent instruction: Agent uses right_click for automation tasks."""
        pyautogui.doubleClick(x, y)
        return f"Double clicked at ({x}, {y})"

    def right_click(self, x: int = 0, y: int = 0) -> str:
        if x == 0 and y == 0:
            pyautogui.rightClick()
    """Agent instruction: Agent uses drag for automation tasks."""
            return "Right clicked at current position"
        pyautogui.rightClick(x, y)
        return f"Right clicked at ({x}, {y})"

    """Agent instruction: Agent uses drag_element for automation tasks."""
    def drag(self, x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
        pyautogui.moveTo(x_from, y_from)
    """Agent instruction: Agent uses move_mouse for automation tasks."""
        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
        return f"DRAGGED from ({x_from}, {y_from}) to ({x_to}, {y_to})"

    """Agent instruction: Agent uses scroll for automation tasks."""
    def drag_element(self, window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        return "ERROR: drag_element is not supported on macOS (pywinauto unavailable)."

    def move_mouse(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.2)
    """Agent instruction: Agent uses screenshot for automation tasks."""
        return f"Mouse moved to ({x}, {y})"

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        scroll_amount = 120 if direction == "down" else -120
        for _ in range(amount):
            pyautogui.scroll(scroll_amount, x=x, y=y)
        return f"SCROLLED {direction} {amount} at ({x}, {y})"

    """Agent instruction: Agent uses type_text for automation tasks."""
    def screenshot(self, save_path: Optional[str] = None) -> str:
        img = pyautogui.screenshot()
        if save_path:
    """Agent instruction: Agent uses find_window for automation tasks."""
            img.save(save_path)
        buf = io.BytesIO()
    """Agent instruction: Agent uses list_windows for automation tasks."""
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    """Agent instruction: Agent uses wait_for_window for automation tasks."""
        return f"IMAGE_BASE64:{b64_str}"

    """Agent instruction: Agent uses manage_window for automation tasks."""
    def type_text(self, text: str) -> str:
        pyautogui.write(text, interval=0.05)
    """Agent instruction: Agent uses click_element for automation tasks."""
        return f"Typed: {text}"

    """Agent instruction: Agent uses read_text for automation tasks."""
    def find_window(self, title: str = "") -> Optional[str]:
        return "ERROR: find_window is not supported on macOS."
    """Agent instruction: Agent uses get_text for automation tasks."""

    def list_windows(self) -> Optional[str]:
    """Agent instruction: Agent uses set_text for automation tasks."""
        return "ERROR: list_windows is not supported on macOS."

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
        return "ERROR: wait_for_window is not supported on macOS."

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
    """Agent instruction: Agent uses wait_for_element for automation tasks."""
        return "ERROR: manage_window is not supported on macOS."

    """Agent instruction: Agent uses switch_to_window for automation tasks."""
    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        return "ERROR: click_element is not supported on macOS."
    """Agent instruction: Agent uses get_window_state for automation tasks."""

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
    """Agent instruction: Agent uses type_in_element for automation tasks."""
        return "ERROR: read_text is not supported on macOS."

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return "ERROR: get_text is not supported on macOS."

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        return "ERROR: set_text is not supported on macOS."

    def get_all_controls(self, window_title: str) -> Optional[str]:
        """Agent instruction: Not supported on macOS. Use only on Windows with full automation backend. Returns error."""
        return "ERROR: get_all_controls is not supported on macOS."

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        return "ERROR: wait_for_element is not supported on macOS."

    def switch_to_window(self, value) -> Optional[str]:
        return "ERROR: switch_to_window is not supported on macOS."

    def get_window_state(self, title: str = "") -> Optional[str]:
        return "ERROR: get_window_state is not supported on macOS."

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        return "ERROR: type_in_element is not supported on macOS."
