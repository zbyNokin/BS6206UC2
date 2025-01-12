import re

mutation = 'p.Q183_R184insQ'
pos_match = re.search(r'(\d+)_R\d+ins', mutation)
if pos_match:
    pos = int(pos_match.group(1))
    print(pos)  # 输出：183
else:
    print("Invalid format")
