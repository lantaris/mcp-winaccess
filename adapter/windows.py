"""Windows adapter using pyautogui + pywinauto."""
import base64
import subprocess
import time
from typing import Optional

import pyautogui
from PIL import Image

from adapter.base import BaseAdapter

try:
    from pywinauto import Desktop
except ImportError:
    Desktop = None


class WindowsAdapter(BaseAdapter):
    """Agent instruction: This adapter uses pywinauto for window automation (find_window, click_element, etc.) and pyautogui for coordinate-based actions (click, drag, screenshot). It supports all functions."""

    def __init__(self):
        if Desktop is None:
            raise ImportError("pywinauto is required for Windows adapter.")

    @property
    def supports_ui_automation(self) -> bool:
        return True

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
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        rect = ctrl[0].rectangle()
                        start_x = (rect.left + rect.right) // 2
                        start_y = (rect.top + rect.bottom) // 2
                        pyautogui.moveTo(start_x, start_y)
                        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
                        return f"DRAGGED '{control_identifier}' to ({x_to}, {y_to})"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found"

    def move_mouse(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})"

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0, window_title: str = "", control_identifier: str = "") -> str:
        scroll_amount = 120 if direction == "down" else -120
        if window_title and control_identifier:
            desktop = Desktop()
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            ctrl[0].wheel_mouse_input(wheel_dist=scroll_amount * amount)
                            return f"SCROLLED {direction} {amount} inside '{control_identifier}'"
                except Exception:
                    continue
            return f"ERROR: Control '{control_identifier}' not found"
        for _ in range(amount):
            pyautogui.scroll(scroll_amount, x=x, y=y)
        return f"SCROLLED {direction} {amount} at ({x}, {y})"

    def screenshot(self, save_path: Optional[str] = None) -> str:
        import io
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
        desktop = Desktop()
        for win in desktop.windows():
            try:
                win_text = win.window_text() or ""
                win_class = win.class_name() or ""
                if title in win_text or title in win_class:
                    rect = win.rectangle()
                    return f"Found: title={win_text}, class={win_class}, handle={win.handle}, pid={win.process_id()}, rect={rect}"
            except Exception:
                continue
        return f"ERROR: Window '{title}' not found."

    def list_windows(self) -> Optional[str]:
        desktop = Desktop()
        results = []
        for win in desktop.windows():
            try:
                results.append(f"Title: '{win.window_text()}', Class: '{win.class_name()}', PID: {win.process_id()}, Rect: {win.rectangle()}")
            except Exception:
                continue
        return "\n".join(results) if results else "No visible windows found."

    def wait_for_window(self, title: str = "", timeout: float = 10.0) -> Optional[str]:
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

    def manage_window(self, title: str = "", action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if title in (win.window_text() or ""):
                    if action == "minimize": win.minimize(); return f"Minimized: {win.window_text()}"
                    elif action == "maximize": win.maximize(); return f"Maximized: {win.window_text()}"
                    elif action == "restore": win.restore(); return f"Restored: {win.window_text()}"
                    elif action == "move": win.move_window(x=x, y=y); return f"Moved: {win.window_text()} to ({x}, {y})"
            except Exception:
                continue
        return f"ERROR: Window '{title}' not found or action '{action}' unknown."

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].click_input()
                        return f"Clicked control '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        text_content = ctrl[0].window_text() or ""
                        return f"Text: '{text_content}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return self.read_text(window_title, control_identifier)

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].set_text(value)
                        return f"SET_TEXT: '{value}' into '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def get_all_controls(self, window_title: str) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    results = []
                    for child in win.descendants():
                        try:
                            child_text = child.window_text() or ""
                            child_type = str(child.element_info.control_type) if hasattr(child.element_info, 'control_type') else type(child).__name__
                            results.append(f"Type: {child_type}, Text: '{child_text}'")
                        except Exception:
                            continue
                    return "\n".join(results) if results else "No controls found."
            except Exception:
                continue
        return f"ERROR: Window '{window_title}' not found."

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        desktop = Desktop()
        start = time.time()
        while time.time() - start < timeout:
            for win in desktop.windows():
                try:
                    if window_title in (win.window_text() or ""):
                        ctrl = win.descendants(title_re=control_identifier)
                        if ctrl and len(ctrl) > 0:
                            return f"ELEMENT FOUND: '{control_identifier}'"
                except Exception:
                    continue
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{control_identifier}'."

    def get_window_state(self, title: str = "") -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if title in (win.window_text() or ""):
                    rect = win.rectangle()
                    return f"Window: title={win.window_text()}, rect={rect}, handle={win.handle}, pid={win.process_id()}"
            except Exception:
                continue
        return f"ERROR: Window '{title}' not found."

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if window_title in (win.window_text() or ""):
                    ctrl = win.descendants(title_re=control_identifier)
                    if ctrl and len(ctrl) > 0:
                        ctrl[0].click_input()
                        ctrl[0].type_keys(text)
                        return f"TYPED: '{text}' into '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."
