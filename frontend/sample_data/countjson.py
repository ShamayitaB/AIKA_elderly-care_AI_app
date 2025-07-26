import json
with open("frontend/sample_data/sample_fall_input.json") as f:
    data = json.load(f)
input_data = data.get("input", [])[0] if data.get("input") else []
print(len(input_data))