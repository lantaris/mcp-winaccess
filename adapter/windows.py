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
        """Agent instruction: Agent uses __init__ for automation tasks."""
        if Desktop is None:
            raise ImportError("pywinauto is required for Windows adapter.")

    @property
    def supports_ui_automation(self) -> bool:
        """Agent instruction: Agent uses supports_ui_automation for automation tasks."""
        return True

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
        if value and control_identifier:
            desktop = Desktop()
            for win in desktop.windows():
                try:
                    match = False
                    if isinstance(value, int):
                        if win.handle == value:
                            match = True
                    else:
                        if value in (win.window_text() or ""):
                            match = True
                    if match:
                        ctrl_obj = self._find_control(desktop, win, control_identifier)
                        if ctrl_obj is not None:
                            rect = ctrl_obj.rectangle()
                            cx = (rect.left + rect.right) // 2
                            cy = (rect.top + rect.bottom) // 2
                            pyautogui.moveTo(cx, cy)
                            pyautogui.doubleClick(cx, cy)
                            return f"Double clicked control '{control_identifier}' at ({cx}, {cy})"
                except Exception:
                    continue
            return f"ERROR: Control '{control_identifier}' not found for double click."
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

    def drag_element(self, value, control_identifier: str, x_to: int, y_to: int, duration: float = 0.5) -> str:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    ctrl_obj = self._find_control(desktop, win, control_identifier)
                    if ctrl_obj is not None:
                        rect = ctrl_obj.rectangle()
                        start_x = (rect.left + rect.right) // 2
                        start_y = (rect.top + rect.bottom) // 2
                        pyautogui.moveTo(start_x, start_y)
                        pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
                        return f"DRAGGED '{control_identifier}' to ({x_to}, {y_to})"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found"

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

    def screenshot_base64(self) -> str:
        """Agent instruction: Captures full desktop screen. Returns base64-encoded JPEG string in format IMAGE_BASE64:{base64_string}. Call this when agent needs to see current screen content (e.g., verify button visibility, read screen state). No file saved."""
        import io
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"IMAGE_BASE64:{b64_str}"

    def screenshot_jpg(self, path: str) -> str:
        """Agent instruction: Captures full desktop screen and saves JPEG to the specified file path (str). Returns confirmation with saved path. Call this when agent needs to save screenshot for later review or reporting."""
        img = pyautogui.screenshot()
        img.save(path, "JPEG")
        return f"Saved screenshot: {path}"

    def type_text(self, text: str) -> str:
        """Agent instruction: Agent uses type_text for automation tasks."""
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def find_window(self, value) -> Optional[str]:
        """Agent instruction: Returns window info for agent context awareness before get_all_controls."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                win_text = win.window_text() or ""
                win_class = win.class_name() or ""
                if isinstance(value, int):
                    if win.handle == value:
                        rect = win.rectangle()
                        return f"Found: title={win_text}, class={win_class}, handle={win.handle}, pid={win.process_id()}, rect={rect}"
                else:
                    if value in win_text or value in win_class:
                        rect = win.rectangle()
                        return f"Found: title={win_text}, class={win_class}, handle={win.handle}, pid={win.process_id()}, rect={rect}"
            except Exception:
                continue
        return f"ERROR: Window '{value}' not found."

    def list_windows(self) -> Optional[str]:
        """Agent instruction: Agent uses list_windows for automation tasks."""
        desktop = Desktop()
        results = []
        for win in desktop.windows():
            try:
                results.append(f"Title: '{win.window_text()}', Class: '{win.class_name()}', PID: {win.process_id()}, Rect: {win.rectangle()}")
            except Exception:
                continue
        return "\n".join(results) if results else "No visible windows found."

    def wait_for_window(self, value, timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: Accepts partial title (str) or handle (int)."""
        desktop = Desktop()
        start = time.time()
        while time.time() - start < timeout:
            for win in desktop.windows():
                try:
                    win_text = win.window_text() or ""
                    win_class = win.class_name() or ""
                    if isinstance(value, int):
                        if win.handle == value:
                            return f"Window '{value}' found (title={win_text})."
                    else:
                        if value in win_text or value in win_class:
                            return f"Window '{value}' found (title={win_text})."
                except Exception:
                    continue
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{value}'."

    def manage_window(self, value, action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        """Agent instruction: Accepts partial title (str) or handle (int)."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if isinstance(value, int):
                    if win.handle == value:
                        if action == "minimize": win.minimize(); return f"Minimized: {win.window_text()}"
                        elif action == "maximize": win.maximize(); return f"Maximized: {win.window_text()}"
                        elif action == "restore": win.restore(); return f"Restored: {win.window_text()}"
                        elif action == "move": win.move_window(x=x, y=y); return f"Moved: {win.window_text()} to ({x}, {y})"
                else:
                    if value in (win.window_text() or ""):
                        if action == "minimize": win.minimize(); return f"Minimized: {win.window_text()}"
                        elif action == "maximize": win.maximize(); return f"Maximized: {win.window_text()}"
                        elif action == "restore": win.restore(); return f"Restored: {win.window_text()}"
                        elif action == "move": win.move_window(x=x, y=y); return f"Moved: {win.window_text()} to ({x}, {y})"
            except Exception:
                continue
        return f"ERROR: Window '{value}' not found or action '{action}' unknown."

    def _find_control(self, desktop, win, control_identifier: str):
        """Agent instruction: Search by title_re first, then by automation name/auto_id, then index (element_N)."""
        # Index-based ID from get_all_controls (e.g., element_0, element_5)
        if isinstance(control_identifier, str) and control_identifier.startswith("element_"):
            try:
                idx = int(control_identifier.split("_")[1])
                descendants = list(win.descendants())
                if 0 <= idx < len(descendants):
                    return descendants[idx]
            except Exception:
                pass
        ctrl = win.descendants(title_re=control_identifier)
        if ctrl and len(ctrl) > 0:
            return ctrl[0]
        try:
            ctrl = win.descendants(name=control_identifier)
            if ctrl and len(ctrl) > 0:
                return ctrl[0]
        except Exception:
            pass
        try:
            ctrl = win.descendants(auto_id=control_identifier)
            if ctrl and len(ctrl) > 0:
                return ctrl[0]
        except Exception:
            pass
        try:
            ctrl = win.descendants(title=control_identifier)
            if ctrl and len(ctrl) > 0:
                return ctrl[0]
        except Exception:
            pass
        return None

    def click_element(self, value, control_identifier: str) -> Optional[str]:
        """Agent instruction: control_identifier should be the index-based 'ID' value from get_all_controls (e.g., 'element_0', 'element_5') or AutoID/Name."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    ctrl_obj = self._find_control(desktop, win, control_identifier)
                    if ctrl_obj is not None:
                        ctrl_obj.click_input()
                        return f"Clicked control '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def read_text(self, value, control_identifier: str) -> Optional[str]:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    ctrl_obj = self._find_control(desktop, win, control_identifier)
                    if ctrl_obj is not None:
                        text_content = ctrl_obj.window_text() or ""
                        return f"Text: '{text_content}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def get_text(self, value, control_identifier: str) -> Optional[str]:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        return self.read_text(value, control_identifier)

    def set_text(self, value, control_identifier: str, text_value: str) -> Optional[str]:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    ctrl_obj = self._find_control(desktop, win, control_identifier)
                    if ctrl_obj is not None:
                        ctrl_obj.set_text(text_value)
                        return f"SET_TEXT: '{text_value}' into '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."

    def get_all_controls(self, value) -> Optional[str]:
        """Agent instruction: Call this before interacting with an unknown window. The output format is 'ID: \"element_0\" | AutoID: \"...\" | Name: \"...\" | Class: \"...\" | Type: ... | Text: \"...\" | Handle: ...'. Use the 'ID' value (e.g., 'element_0', 'element_5') as control_identifier for click_element, set_text, read_text, etc. If needed, use the 'Name' or 'AutoID' as identifier."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    results = []
                    for idx, child in enumerate(win.descendants()):
                        try:
                            child_text = child.window_text() or ""
                            control_id = f"element_{idx}"
                            automation_id = getattr(child.element_info, 'automation_id', None) or ''
                            name = getattr(child.element_info, 'name', None) or getattr(child, 'name', None) or ''
                            class_name = getattr(child.element_info, 'class_name', None) or ''
                            handle = getattr(child, 'handle', None) or ''
                            child_type = str(child.element_info.control_type) if hasattr(child.element_info, 'control_type') else type(child).__name__
                            results.append(f"ID: '{control_id}' | AutoID: '{str(automation_id).strip()}' | Name: '{str(name).strip()}' | Class: '{str(class_name).strip()}' | Type: {child_type} | Text: '{child_text}' | Handle: {handle}")
                        except Exception:
                            continue
                    return "\n".join(results) if results else "No controls found."
            except Exception:
                continue
        return f"ERROR: Window '{value}' not found."

    def wait_for_element(self, value, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        desktop = Desktop()
        start = time.time()
        while time.time() - start < timeout:
            for win in desktop.windows():
                try:
                    match = False
                    if isinstance(value, int):
                        if win.handle == value:
                            match = True
                    else:
                        if value in (win.window_text() or ""):
                            match = True
                    if match:
                        ctrl_obj = self._find_control(desktop, win, control_identifier)
                        if ctrl_obj is not None:
                            return f"ELEMENT FOUND: '{control_identifier}'"
                except Exception:
                    continue
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{control_identifier}'."

    def switch_to_window(self, value) -> Optional[str]:
        """Agent instruction: Accepts either partial title (str) or window handle (int). Restores and activates the window."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if isinstance(value, int):
                    if win.handle == value:
                        win.restore()
                        win.set_focus()
                        return f"Activated window with handle={value} (title={win.window_text()})"
                else:
                    if value in (win.window_text() or ""):
                        win.restore()
                        win.set_focus()
                        return f"Activated window '{win.window_text()}'"
            except Exception:
                continue
        return f"ERROR: Window '{value}' not found or could not be activated."

    def get_window_state(self, value) -> Optional[str]:
        """Agent instruction: Agent uses get_window_state for automation tasks. Accepts partial title (str) or handle (int)."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                if isinstance(value, int):
                    if win.handle == value:
                        rect = win.rectangle()
                        return f"Window: title={win.window_text()}, rect={rect}, handle={win.handle}, pid={win.process_id()}"
                else:
                    if value in (win.window_text() or ""):
                        rect = win.rectangle()
                        return f"Window: title={win.window_text()}, rect={rect}, handle={win.handle}, pid={win.process_id()}"
            except Exception:
                continue
        return f"ERROR: Window '{value}' not found."

    def type_in_element(self, value, control_identifier: str, text: str) -> Optional[str]:
        """Agent instruction: control_identifier is the index-based 'ID' (e.g., 'element_0') or AutoID/Name from get_all_controls."""
        desktop = Desktop()
        for win in desktop.windows():
            try:
                match = False
                if isinstance(value, int):
                    if win.handle == value:
                        match = True
                else:
                    if value in (win.window_text() or ""):
                        match = True
                if match:
                    ctrl_obj = self._find_control(desktop, win, control_identifier)
                    if ctrl_obj is not None:
                        ctrl_obj.click_input()
                        ctrl_obj.type_keys(text)
                        return f"TYPED: '{text}' into '{control_identifier}'"
            except Exception:
                continue
        return f"ERROR: Control '{control_identifier}' not found."
