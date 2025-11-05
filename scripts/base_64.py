from pathlib import Path
import base64
from utils import get_lines,apply_txt

lines = (get_lines("../attacks/override_attack.txt"))

base_64_lines = get_lines("../attacks/obfuscated_attacks.txt")

base64_strings = [[base64.b64encode(line.encode('utf-8')).decode('ascii')] for line in base_64_lines]

print(base64_strings)





base_script_dir = Path(__file__).parent.parent
json_path = Path(base_script_dir / "attacks" / "attacks.json")
# print(count_types(json_path,"base_64"))
apply_txt([[line] for line in lines],json_path,"override")
# print(count_types(json_path,"leet_speak"))
# print(count_types(json_path,"Role-Based"))
# print(count_types(json_path,"MultiTurn"))

# apply_txt(base64_strings, json_path,"base_64")
