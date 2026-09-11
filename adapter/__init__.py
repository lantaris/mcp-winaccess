"""Adapter loader: selects platform-specific adapter."""
import sys
from adapter.base import BaseAdapter

if sys.platform == "win32":
    from adapter.windows import WindowsAdapter as AdapterImpl
elif sys.platform == "darwin":
    from adapter.macos import MacOSAdapter as AdapterImpl
else:
    # Linux or other Unix
    from adapter.linux import LinuxAdapter as AdapterImpl

_default_adapter: BaseAdapter | None = None


def get_adapter() -> BaseAdapter:
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = AdapterImpl()
    return _default_adapter
