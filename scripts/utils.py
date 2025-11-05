from pathlib import Path
import json

def get_lines(path: str) -> list[str]:
    file_path = Path(__file__).parent / path
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    return lines

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

def load_prompt(json_path:Path) -> list[str]:
    json_text  = json_path.read_text()
    json_data = json.loads(json_text)
    final_data = []
    for data in json_data:
        if isinstance(data, dict) and data["type"] != "MultiTurn" and data['text'] != "" :
            final_data.append(data["text"])

    return final_data
    



base_script_dir = Path(__file__).parent.parent
json_path = base_script_dir / "attacks" / "attacks.json"


# role_playing_lines = get_lines("../attacks/role_play_attacks.txt")
# print(role_playing_lines)
# apply_txt([[lines] for lines in role_playing_lines],json_path,"Role-Based")
# json_data = load_prompt(Path(json_path))
# print(json_data)
# print(count_types(Path(json_path),"leet_speak"))
print(count_types(Path(json_path),"MultiTurn"))
# print(count_types(Path(json_path),"Role-Based"))