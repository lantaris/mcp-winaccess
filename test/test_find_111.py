#!/usr/bin/env python3
"""Find element with 111 and set to 999."""
import sys, re
sys.path.insert(0, '.')
from adapter import get_adapter
adapter = get_adapter()
controls = adapter.get_all_controls('Калькулятор')
print('=== CONTROLS ===')
print(controls)
found = False
for line in controls.split('\n'):
    if '111' in line:
        match = re.search(r"ID: '([^']+)'", line)
        if match:
            cid = match.group(1)
            print('Found 111 control ID:', cid)
            result = adapter.set_text('Калькулятор', cid, '999')
            print('set_text result:', result)
            found = True
            break
if not found:
    print('No 111 found.')
    for line in controls.split('\n'):
        if "'9'" in line or "'1'" in line or "'9123'" in line:
            match = re.search(r"ID: '([^']+)'", line)
            if match:
                cid = match.group(1)
                print('First numeric ID:', cid)
                result = adapter.set_text('Калькулятор', cid, '999')
                print('set_text result:', result)
                break
