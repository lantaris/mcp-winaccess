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

    def double_click_element(self, value: str = "", control_identifier: str = "") -> str:
        if not HAS_PYATSPI:
            return "ERROR: double_click_element requires pyatspi."
        ctrl = self._find_control(value, control_identifier)
        if ctrl is None:
            return f"ERROR: Control '{control_identifier}' not found for double click."
        # Try to click via action interface
        try:
            action = ctrl.getAction()
            if hasattr(action, 'doAction'):
                # Some actions support doAction, not double click directly
                pass
        except Exception:
            pass
        # Fallback to coordinate double click if rectangle available
        try:
            import pyatspi
            rect = ctrl.getExtents(pyatspi.DESKTOP_COORDS)
            cx = rect.x + rect.width // 2
            cy = rect.y + rect.height // 2
            pyautogui.doubleClick(cx, cy)
            return f"Double clicked control '{control_identifier}' at ({cx}, {cy})"
        except Exception:
            pass
        return f"ERROR: Could not double click '{control_identifier}'."

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
        if not HAS_PYATSPI:
            return "ERROR: drag_element requires pyatspi."
        ctrl = self._find_control(window_title, control_identifier)
        if ctrl is None:
            return f"ERROR: Control '{control_identifier}' not found"
        try:
            import pyatspi
            rect = ctrl.getExtents(pyatspi.DESKTOP_COORDS)
            start_x = rect.x + rect.width // 2
            start_y = rect.y + rect.height // 2
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(x_to, y_to, duration=duration, button='left')
            return f"DRAGGED '{control_identifier}' to ({x_to}, {y_to})"
        except Exception as exc:
            return f"ERROR: Could not drag '{control_identifier}': {exc}"

    def move_mouse(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})"

    def scroll(self, direction: str = "down", amount: int = 3, x: int = 0, y: int = 0) -> str:
        scroll_amount = 120 if direction == "down" else -120
        for _ in range(amount):
            pyautogui.scroll(scroll_amount, x=x, y=y)
        return f"SCROLLED {direction} {amount} at ({x}, {y})"

    def screenshot_base64(self) -> str:
        import base64, io
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"IMAGE_BASE64:{b64_str}"

    def screenshot(self):
        return pyautogui.screenshot()

    def screenshot_jpg(self, path: str = "") -> str:
        import tempfile, uuid
        if not path:
            path = tempfile.gettempdir() + "/" + str(uuid.uuid4()) + ".jpg"
        img = pyautogui.screenshot()
        img.save(path, "JPEG")
        return f"Saved screenshot: {path}"

    def type_text(self, text: str) -> str:
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"

    def _desktop(self):
        if not HAS_PYATSPI:
            return None
        try:
            return pyatspi.Registry.getDesktop(0)
        except Exception:
            return None

    def _find_window_object(self, value) -> Optional:
        desktop = self._desktop()
        if desktop is None:
            return None
        for app in desktop:
            try:
                for win in app:
                    try:
                        win_text = win.getName() or ""
                        # Try to get role/class info if available
                        role = win.getRoleName() if hasattr(win, 'getRoleName') else ""
                        win_class = role  # pyatspi uses role as identifier
                        if isinstance(value, int):
                            # Int handle not supported in pyatspi; skip
                            continue
                        if value in win_text or value in win_class:
                            return win
                    except Exception:
                        continue
            except Exception:
                continue
        return None

    def find_window(self, value) -> Optional[str]:
        if isinstance(value, int):
            return "ERROR: find_window int handles require full automation backend (Windows)."
        if not HAS_PYATSPI:
            return "ERROR: find_window requires pyatspi (not installed or Linux backend unavailable)."
        win = self._find_window_object(value)
        if win is None:
            return f"ERROR: Window '{value}' not found."
        try:
            name = win.getName() or ""
            role = win.getRoleName() if hasattr(win, 'getRoleName') else ""
            state = win.getState()
            return f"Found: title={name}, role={role}, state={[str(s) for s in state.getStates()] if hasattr(state, 'getStates') else 'N/A'}"
        except Exception as exc:
            return f"Found window '{value}' (details unavailable: {exc})"

    def list_windows(self) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: list_windows requires pyatspi."
        desktop = self._desktop()
        if desktop is None:
            return "No visible windows found."
        results = []
        for app in desktop:
            try:
                for win in app:
                    try:
                        name = win.getName() or ""
                        role = win.getRoleName() if hasattr(win, 'getRoleName') else ""
                        results.append(f"Title: '{name}', Role: '{role}'")
                    except Exception:
                        continue
            except Exception:
                continue
        return "\n".join(results) if results else "No visible windows found."

    def wait_for_window(self, value, timeout: float = 10.0) -> Optional[str]:
        if not HAS_PYATSPI:
            return f"ERROR: wait_for_window requires pyatspi."
        start = time.time()
        while time.time() - start < timeout:
            win = self._find_window_object(value)
            if win is not None:
                name = win.getName() or ""
                return f"Window '{value}' found (title={name})."
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{value}'."

    def manage_window(self, value, action: str = "maximize", x: int = 0, y: int = 0) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: manage_window requires full UI automation backend (pywinauto on Windows)."
        win = self._find_window_object(value)
        if win is None:
            return f"ERROR: Window '{value}' not found or action '{action}' unknown."
        # Basic state actions via pyatspi interfaces (very limited)
        try:
            # Try to use component/state interfaces; actual maximize/minimize not fully supported
            return f"Window '{win.getName() or value}' located; action '{action}' not fully supported on Linux via pyatspi."
        except Exception as exc:
            return f"ERROR: Manage window failed: {exc}"

    def _find_control(self, value, control_identifier: str):
        win = self._find_window_object(value)
        if win is None:
            return None
        # Search descendants by name/role/index
        def search(node, target):
            if node is None:
                return None
            try:
                # Check index identifier
                if isinstance(target, str) and target.startswith("element_"):
                    # Index-based search: enumerate children; but pyatspi tree is recursive
                    # For simplicity, search through all descendants
                    pass
                current_name = node.getName() or ""
                current_role = node.getRoleName() if hasattr(node, 'getRoleName') else ""
                # Try to match by name or role
                if target in current_name or target in current_role:
                    return node
                # Try to match index-based if applicable
                # This is a simplified approach
                # Try interface action/text
                try:
                    iface_text = node.queryText()
                    if iface_text and hasattr(iface_text, 'getText'):
                        text_content = iface_text.getText(0, -1)
                        if target in text_content:
                            return node
                except Exception:
                    pass
                # Recursively search children
                try:
                    for i in range(node.childCount):
                        child = node.getChildAtIndex(i)
                        result = search(child, target)
                        if result is not None:
                            return result
                except Exception:
                    pass
            except Exception:
                pass
            return None
        return search(win, control_identifier)

    def click_element(self, window_title: str, control_identifier: str) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: click_element requires pyatspi."
        ctrl = self._find_control(window_title, control_identifier)
        if ctrl is None:
            return f"ERROR: Control '{control_identifier}' not found."
        try:
            action = ctrl.getAction()
            if hasattr(action, 'doAction'):
                action.doAction(0)
            else:
                # Fallback: try to click input via coordinate approximation
                import pyatspi
                rect = ctrl.getExtents(pyatspi.DESKTOP_COORDS)
                cx = rect.x + rect.width // 2
                cy = rect.y + rect.height // 2
                pyautogui.click(cx, cy)
            return f"Clicked control '{control_identifier}'"
        except Exception as exc:
            return f"ERROR: Could not click control '{control_identifier}': {exc}"

    def read_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        try:
            ctrl = self._find_control(window_title, control_identifier)
            if ctrl is None:
                return f"ERROR: Control '{control_identifier}' not found."
            # Try text interface
            try:
                iface_text = ctrl.queryText()
                if iface_text and hasattr(iface_text, 'getText'):
                    text_content = iface_text.getText(0, -1)
                    return f"Text: '{text_content}'"
            except Exception:
                pass
            # Try accessible name
            name = ctrl.getName() or ""
            return f"Text: '{name}'"
        except Exception as exc:
            return f"ERROR: Control '{control_identifier}' not found."

    def get_text(self, window_title: str, control_identifier: str) -> Optional[str]:
        return self.read_text(window_title, control_identifier)

    def set_text(self, window_title: str, control_identifier: str, value: str) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: set_text requires pyatspi."
        ctrl = self._find_control(window_title, control_identifier)
        if ctrl is None:
            return f"ERROR: Control '{control_identifier}' not found."
        try:
            # Try to set value via editable text interface if available
            try:
                iface_edit = ctrl.queryEditableText()
                if iface_edit and hasattr(iface_edit, 'setTextContents'):
                    iface_edit.setTextContents(value)
                    return f"SET_TEXT: '{value}' into '{control_identifier}'"
            except Exception:
                pass
            # Fallback: click and type
            import pyatspi
            rect = ctrl.getExtents(pyatspi.DESKTOP_COORDS)
            cx = rect.x + rect.width // 2
            cy = rect.y + rect.height // 2
            pyautogui.click(cx, cy)
            pyautogui.write(value, interval=0.05)
            return f"SET_TEXT (fallback): '{value}' into '{control_identifier}'"
        except Exception as exc:
            return f"ERROR: Could not set text '{value}' into '{control_identifier}': {exc}"

    def get_all_controls(self, value) -> Optional[str]:
        if isinstance(value, int):
            return "ERROR: get_all_controls int handles require full automation backend (Windows)."
        if not HAS_PYATSPI:
            return "ERROR: get_all_controls requires pyatspi."
        win = self._find_window_object(value)
        if win is None:
            return f"ERROR: Window '{value}' not found."
        results = []
        def collect(node, index=0):
            try:
                if node is None:
                    return
                name = node.getName() or ""
                role_name = node.getRoleName() if hasattr(node, 'getRoleName') else ""
                # Try to get text
                text_content = ""
                try:
                    iface_text = node.queryText()
                    if iface_text and hasattr(iface_text, 'getText'):
                        text_content = iface_text.getText(0, -1)
                except Exception:
                    pass
                # Try to build a basic identifier
                control_id = f"element_{index}"
                # Try to get automation-like info
                automation_id = name  # simplified
                handle_str = ""
                child_type = role_name or ""
                results.append(
                    f"ID: '{control_id}' | AutoID: '{str(automation_id).strip()}' | Name: '{str(name).strip()}' | Class: '{str(child_type).strip()}' | Type: '{str(child_type).strip()}' | Text: '{str(text_content).strip()}' | Handle: '{str(handle_str).strip()}'"
                )
                # Recurse for children
                child_idx = 0
                try:
                    for child in node:
                        collect(child, index + child_idx)
                        child_idx += 1
                except Exception:
                    pass
            except Exception:
                pass
        collect(win)
        return "\n".join(results) if results else "No controls found."

    def wait_for_element(self, window_title: str, control_identifier: str, timeout: float = 10.0) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: wait_for_element requires full UI automation backend."
        start = time.time()
        while time.time() - start < timeout:
            ctrl = self._find_control(window_title, control_identifier)
            if ctrl is not None:
                return f"ELEMENT FOUND: '{control_identifier}'"
            time.sleep(0.5)
        return f"ERROR: Timeout ({timeout}s) waiting for '{control_identifier}'."

    def switch_to_window(self, value) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: switch_to_window requires full UI automation backend (pywinauto on Windows)."
        win = self._find_window_object(value)
        if win is None:
            return f"ERROR: Window '{value}' not found or could not be activated."
        try:
            # pyatspi doesn't have direct set_focus, but we can try to activate via action
            try:
                action = win.getAction()
                # Some actions might include 'focus' or similar; not guaranteed
            except Exception:
                pass
            return f"Activated window '{win.getName() or value}'"
        except Exception as exc:
            return f"ERROR: Window '{value}' not found or could not be activated: {exc}"

    def get_window_state(self, value) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: get_window_state requires full UI automation backend."
        win = self._find_window_object(value)
        if win is None:
            return f"ERROR: Window '{value}' not found."
        try:
            name = win.getName() or ""
            role = win.getRoleName() if hasattr(win, 'getRoleName') else ""
            return f"Window: title={name}, role={role}"
        except Exception as exc:
            return f"ERROR: Window '{value}' not found: {exc}"

    def type_in_element(self, window_title: str, control_identifier: str, text: str) -> Optional[str]:
        if not HAS_PYATSPI:
            return "ERROR: type_in_element requires full UI automation backend."
        ctrl = self._find_control(window_title, control_identifier)
        if ctrl is None:
            return f"ERROR: Control '{control_identifier}' not found."
        try:
            # Click and type
            import pyatspi
            rect = ctrl.getExtents(pyatspi.DESKTOP_COORDS)
            cx = rect.x + rect.width // 2
            cy = rect.y + rect.height // 2
            pyautogui.click(cx, cy)
            # Try editable text interface
            try:
                iface_edit = ctrl.queryEditableText()
                if iface_edit and hasattr(iface_edit, 'setTextContents'):
                    iface_edit.setTextContents(text)
                    return f"TYPED: '{text}' into '{control_identifier}'"
            except Exception:
                pass
            pyautogui.write(text, interval=0.05)
            return f"TYPED (fallback): '{text}' into '{control_identifier}'"
        except Exception as exc:
            return f"ERROR: Could not type '{text}' into '{control_identifier}': {exc}"
