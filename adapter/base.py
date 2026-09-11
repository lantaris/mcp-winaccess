"""Base adapter interface for platform-independent automation."""
from typing import Optional, List


class BaseAdapter:
    """Agent instruction: This is the abstract interface. Each platform must implement all methods or return None for unsupported ones."""

    def click(self, x: int, y: int) -> str:
        raise NotImplementedError

    def double_click(self, x: int = 0, y: int = 0) -> str:
        raise NotImplementedError

    def right_click(self, x: int = 0, y: int = 0) -> str:
        raise NotImplementedError

    def drag(self, x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
        raise NotImplementedError

    def drag_element(self, window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        raise NotImplementedError

    def move_mouse(self, x: int, y: int) -> str:
        raise NotImplementedError

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        raise NotImplementedError

    def screenshot(self, save_path: Optional[str] = None) -> str:
        raise NotImplementedError

    def type_text(self, text: str) -> str:
        raise NotImplementedError

    def find_window(self, title: str = "") -> Optional[str]:
        return None  # Not supported by default

    def list_windows(self) -> Optional[str]:
        return None

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
        return None

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        return None

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        return None

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return None

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return None

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        return None

    def get_all_controls(self, window_title: str) -> Optional[str]:
        return None

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        return None

    def get_window_state(self, title: str = "") -> Optional[str]:
        return None

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        return None

    @property
    def supports_ui_automation(self) -> bool:
        return False
