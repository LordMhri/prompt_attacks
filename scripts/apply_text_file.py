from pathlib import Path
import json
import base64
def get_lines(path: str) -> list[str]:
    file_path = Path(__file__).parent / path
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines

lines = (get_lines("../attacks/override_attack.txt"))

base_64_lines = get_lines("../attacks/base64_original_strings.txt")

base64_strings = [base64.b64encode(line.encode('utf-8')).decode('ascii') for line in base_64_lines]

# print(base64_strings)
def apply_txt(lines:list[str],json_path:Path,type:str) -> None:
    json_text  = json_path.read_text()
    json_data = json.loads(json_text)
    line_index = 0
    for obj in json_data:
        if isinstance(obj, dict) and obj.get("type") == type:
            obj["text"] = lines[line_index]
            line_index += 1

    json_path.write_text(
        json.dumps(json_data, indent=4, ensure_ascii=False) + "\n",
        encoding='utf-8'
    )

def count_types(json_path:Path,type:str) -> int:
    json_text  = json_path.read_text()
    json_data = json.loads(json_text)
    type_count = 0
    for obj in json_data:
        if isinstance(obj, dict) and obj.get("type") == type:
            type_count += 1
    
    return type_count

base_script_dir = Path(__file__).parent.parent
json_path = Path(base_script_dir / "attacks" / "attacks.json")
# print(count_types(json_path,"base_64"))
# print(count_types(json_path,"leet_speak"))
# print(count_types(json_path,"Role-Based"))
# print(count_types(json_path,"MultiTurn"))

apply_txt(base64_strings, json_path,"base_64")
