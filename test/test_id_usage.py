import sys, re
sys.path.insert(0, '.')
from adapter import get_adapter
adapter = get_adapter()
controls = adapter.get_all_controls('Калькулятор')
print('=== ID test ===')
for line in controls.split('\n'):
    if 'ID:' in line:
        print(line)
print('=== set_text test ===')
for line in controls.split('\n'):
    match = re.search(r"ID: 'element_(\d+)'", line)
    if match:
        cid = 'element_' + match.group(1)
        print('Using ID:', cid)
        print(adapter.set_text('Калькулятор', cid, '999'))
        break
