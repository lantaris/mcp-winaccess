"""Base adapter interface for platform-independent automation."""
from typing import Optional


class BaseAdapter:
    """Agent instruction: This is the abstract interface. Each platform must implement all methods or return None for unsupported ones."""

    def click(self, x: int, y: int) -> str:
        """Agent instruction: Agent uses click for automation tasks."""
        raise NotImplementedError

    def double_click(self, x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses double_click for automation tasks."""
        raise NotImplementedError

    def right_click(self, x: int = 0, y: int = 0) -> str:
        """Agent instruction: Agent uses right_click for automation tasks."""
        raise NotImplementedError

    def drag(self, x_from: int, y_from: int, x_to: int, y_to: int, duration: float = 0.5) -> str:
        """Agent instruction: Agent uses drag for automation tasks."""
        raise NotImplementedError

    def drag_element(self, window_title: str, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        """Agent instruction: Agent uses drag_element for automation tasks."""
        raise NotImplementedError

    def move_mouse(self, x: int, y: int) -> str:
        """Agent instruction: Agent uses move_mouse for automation tasks."""
        raise NotImplementedError

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        """Agent instruction: Agent uses scroll for automation tasks."""
        raise NotImplementedError

    def screenshot(self, save_path: Optional[str] = None) -> str:
        """Agent instruction: Agent uses screenshot for automation tasks."""
        raise NotImplementedError

    def type_text(self, text: str) -> str:
        """Agent instruction: Agent uses type_text for automation tasks."""
        raise NotImplementedError

    def find_window(self, title: str = "") -> Optional[str]:
        """Agent instruction: Agent uses find_window for automation tasks."""
        return None

    def list_windows(self) -> Optional[str]:
        """Agent instruction: Agent uses list_windows for automation tasks."""
        return None

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: Agent uses wait_for_window for automation tasks."""
        return None

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        """Agent instruction: Agent uses manage_window for automation tasks."""
        return None

    def switch_to_window(self, value) -> Optional[str]:
        """Agent instruction: Accepts partial title (str) or window handle (int). Restores and activates the window."""
        return None

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses click_element for automation tasks."""
        return None

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses read_text for automation tasks."""
        return None

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        """Agent instruction: Agent uses get_text for automation tasks."""
        return None

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        """Agent instruction: Agent uses set_text for automation tasks."""
        return None

    def get_all_controls(self, window_title: str) -> Optional[str]:
        """Agent instruction: Agent uses get_all_controls for automation tasks."""
        return None

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: Agent uses wait_for_element for automation tasks."""
        return None

    def get_window_state(self, title: str = "") -> Optional[str]:
        """Agent instruction: Agent uses get_window_state for automation tasks."""
        return None

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        """Agent instruction: Agent uses type_in_element for automation tasks."""
        return None

    @property
    def supports_ui_automation(self) -> bool:
        """Agent instruction: Agent uses supports_ui_automation for automation tasks."""
        return False
