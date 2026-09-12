"""macOS adapter using pyautogui (no window automation)."""
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
    def supports_ui_automation(self) -> bool:
        """Agent instruction: Agent uses supports_ui_automation for automation tasks."""
        return False

    def click(self, x: int, y: int) -> str:
        """Agent instruction: Agent uses click for automation tasks."""
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})"

    def double_click(self, x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses double_click for automation tasks."""
        if x == 0 and y == 0:
            pyautogui.doubleClick()
            return "Double clicked at current position"
        pyautogui.doubleClick(x, y)
        return f"Double clicked at ({x}, {y})"

    def double_click_element(self, value: str = "", control_identifier: str = "", x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses double_click for automation tasks."""
        if x == 0 and y == 0:
            pyautogui.doubleClick()
            return "Double clicked at current position"
        pyautogui.doubleClick(x, y)
        return f"Double clicked at ({x}, {y})"

    def right_click(self, x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses right_click for automation tasks."""
        if x == 0 and y == 0:
            pyautogui.rightClick()
            return "Right clicked at current position"
        pyautogui.rightClick(x, y)
        return f"Right clicked at ({x}, {y})"

    def drag(self, x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
        """Agent instruction: Agent uses drag for automation tasks."""
        pyautogui.moveTo(x_from, y_from)
        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
        return f"DRAGGED from ({x_from}, {y_from}) to ({x_to}, {y_to})"

    def drag_element(self, window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        """Agent instruction: Agent uses drag_element for automation tasks."""
        return "ERROR: drag_element is not supported on macOS (pywinauto unavailable)."

    def move_mouse(self, x: int, y: int) -> str:
        """Agent instruction: Agent uses move_mouse for automation tasks."""
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})"

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses scroll for automation tasks."""
        scroll_amount = 120 if direction == "down" else -120
        for _ in range(amount):
            pyautogui.scroll(scroll_amount, x=x, y=y)
        return f"SCROLLED {direction} {amount} at ({x}, {y})"

    def screenshot(self, save_path: Optional[str] = None) -> str:
        """Agent instruction: Agent uses screenshot for automation tasks."""
        img = pyautogui.screenshot()
        if save_path:
            img.save(save_path)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"IMAGE_BASE64:{b64_str}"

    def type_text(self, text: str) -> str:
        """Agent instruction: Agent uses type_text for automation tasks."""
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def find_window(self, title: str = "") -> Optional[str]:
        """Agent instruction: Agent uses find_window for automation tasks."""
        return "ERROR: find_window is not supported on macOS."

    def list_windows(self) -> Optional[str]:
        """Agent instruction: Agent uses list_windows for automation tasks."""
        return "ERROR: list_windows is not supported on macOS."

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: Agent uses wait_for_window for automation tasks."""
        return "ERROR: wait_for_window is not supported on macOS."

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        """Agent instruction: Agent uses manage_window for automation tasks."""
        return "ERROR: manage_window is not supported on macOS."

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses click_element for automation tasks."""
        return "ERROR: click_element is not supported on macOS."

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses read_text for automation tasks."""
        return "ERROR: read_text is not supported on macOS."

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses get_text for automation tasks."""
        return "ERROR: get_text is not supported on macOS."

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        """Agent instruction: Agent uses set_text for automation tasks."""
        return "ERROR: set_text is not supported on macOS."

    def get_all_controls(self, window_title: str) -> Optional[str]:
        """Agent instruction: Not supported on macOS. Use only on Windows with full automation backend. Returns error."""
        return "ERROR: get_all_controls is not supported on macOS."

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: Agent uses wait_for_element for automation tasks."""
        return "ERROR: wait_for_element is not supported on macOS."

    def switch_to_window(self, value) -> Optional[str]:
        """Agent instruction: Not supported on macOS. Use only on Windows with full automation backend."""
        return "ERROR: switch_to_window is not supported on macOS."

    def get_window_state(self, title: str = "") -> Optional[str]:
        """Agent instruction: Agent uses get_window_state for automation tasks."""
        return "ERROR: get_window_state is not supported on macOS."

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        """Agent instruction: Agent uses type_in_element for automation tasks."""
        return "ERROR: type_in_element is not supported on macOS."
