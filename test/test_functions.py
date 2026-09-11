#!/usr/bin/env python3
"""Verify adapter and server functions."""
import sys
sys.path.insert(0, '..')

from adapter import get_adapter
adapter = get_adapter()

print("Adapter:", type(adapter).__name__)
print("UI automation:", adapter.supports_ui_automation)

methods = [
    "click", "double_click", "right_click", "drag", "drag_element",
    "move_mouse", "scroll", "screenshot", "type_text",
    "find_window", "list_windows", "wait_for_window", "manage_window",
    "click_element", "read_text", "get_text", "set_text",
    "get_all_controls", "wait_for_element", "get_window_state", "type_in_element"
]

for m in methods:
    func = getattr(adapter, m, None)
    status = "OK" if callable(func) else "MISSING"
    print(f"  adapter.{m}: {status}")

print("\nAll adapter functions present." if all(callable(getattr(adapter, m, None)) for m in methods) else "\nSome functions missing!")
