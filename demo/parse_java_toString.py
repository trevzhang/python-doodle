import re
import json


def parse_java_toString(s):
    def parse_value(v):
        v = v.strip()
        if v == 'null':
            return None
        elif v == '':
            return ''
        elif v.startswith('{') and v.endswith('}'):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return parse_java_toString(v[1:-1])
        elif '(' in v and v.endswith(')'):
            class_name, content = v.split('(', 1)
            return {class_name: parse_java_toString(content[:-1])}
        elif v.startswith('<') and v.endswith('>'):
            return v
        else:
            try:
                return int(v)
            except ValueError:
                try:
                    return float(v)
                except ValueError:
                    return v

    result = {}
    pattern = r'(\w+)=(?:([^,(){}]+)|(\{[^{}]*\})|(\([^()]*\))|(<[^<>]*>))(?:,|$)'
    matches = re.findall(pattern, s)

    for match in matches:
        key = match[0]
        value = next(v for v in match[1:] if v)
        result[key] = parse_value(value)

    return result


def format_output(data, indent=0):
    output = ""
    for key, value in data.items():
        if isinstance(value, dict):
            if len(value) == 1 and isinstance(list(value.values())[0], dict):
                class_name = list(value.keys())[0]
                output += "  " * indent + f"{key}: {class_name}(\n"
                output += format_output(list(value.values())[0], indent + 1)
                output += "  " * indent + ")\n"
            else:
                output += "  " * indent + f"{key}:\n"
                output += format_output(value, indent + 1)
        elif isinstance(value, (list, dict)):
            output += "  " * indent + f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
        else:
            output += "  " * indent + f"{key}: {value}\n"
    return output


def to_json(data):
    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            return str(obj)

    return json.dumps(data, indent=2, ensure_ascii=False, cls=CustomEncoder)


# 测试
input_string = """name=张三, age=14"""

parsed_data = parse_java_toString(input_string)

print("格式化输出:")
formatted_output = format_output(parsed_data)
print(formatted_output)

print("\nJSON输出:")
json_output = to_json(parsed_data)
print(json_output)