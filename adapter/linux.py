"""Linux adapter using pyatspi (when available) + pyautogui."""
import time
from typing import Optional

import pyautogui

from adapter.base import BaseAdapter

try:
    import pyatspi
    HAS_PYATSPI = True
except ImportError:
    HAS_PYATSPI = False


class LinuxAdapter(BaseAdapter):
    """Agent instruction: Uses pyautogui for coordinate actions and pyatspi for window/element discovery when available."""

    def __init__(self):
        pass

    @property
    def supports_ui_automation(self) -> bool:
        return HAS_PYATSPI

    def click(self, x: int, y: int) -> str:
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})"

    def double_click(self, x: int = 0, y: int = 0) -> str:
        if x == 0 and y == 0:
            pyautogui.doubleClick()
            return "Double clicked at current position"
        pyautogui.doubleClick(x, y)
        return f"Double clicked at ({x}, {y})"

    def right_click(self, x: int = 0, y: int = 0) -> str:
        if x == 0 and y == 0:
            pyautogui.rightClick()
            return "Right clicked at current position"
        pyautogui.rightClick(x, y)
        return f"Right clicked at ({x}, {y})"

    def drag(self, x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
        pyautogui.moveTo(x_from, y_from)
        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
        return f"DRAGGED from ({x_from}, {y_from}) to ({x_to}, {y_to})"

    def drag_element(self, window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        return f"ERROR: drag_element requires pyatspi (not fully implemented on Linux adapter)"

    def move_mouse(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})"

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        scroll_amount = 120 if direction == "down" else -120
        for _ in range(amount):
            pyautogui.scroll(scroll_amount, x=x, y=y)
        return f"SCROLLED {direction} {amount} at ({x}, {y})"

    def screenshot(self, save_path: Optional[str] = None) -> str:
        import base64, io
        img = pyautogui.screenshot()
        if save_path:
            img.save(save_path)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"IMAGE_BASE64:{b64_str}"

    def type_text(self, text: str) -> str:
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def find_window(self, title: str = "") -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: find_window requires pyatspi (not installed or Linux backend unavailable)."
        return "ERROR: Linux adapter find_window is basic; use pyatspi directly for full automation."

    def list_windows(self) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: list_windows requires pyatspi."
        return "Linux list_windows: basic support (use desktop enumeration via AT-SPI if needed)."

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
        if not HAS_PYATSPI:
            return f"ERROR: wait_for_window requires pyatspi."
        return f"ERROR: Linux adapter does not fully implement wait_for_window."

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        return "ERROR: manage_window requires full UI automation backend (pywinauto on Windows)."

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: click_element requires pyatspi."
        return f"ERROR: Linux adapter click_element is basic; pyatspi required."

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return "ERROR: read_text requires full UI automation backend."

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return "ERROR: get_text requires full UI automation backend."

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        return "ERROR: set_text requires full UI automation backend."

    def get_all_controls(self, window_title: str) -> Optional[str]:
        return "ERROR: get_all_controls requires full UI automation backend."

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        return "ERROR: wait_for_element requires full UI automation backend."

    def get_window_state(self, title: str = "") -> Optional[str]:
        return "ERROR: get_window_state requires full UI automation backend."

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        return "ERROR: type_in_element requires full UI automation backend."
