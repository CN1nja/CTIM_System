import json


def text_to_json(text_path):
    # 将字符串按行分割成列表
    with open(text_path, 'r') as f:
        lines = f.read().splitlines()
    # print(lines)

    # 定义空的JSON数组
    result = []

    # 遍历每一行，将其转换为JSON对象并添加到数组中
    for line in lines:
        line = line.replace('[', ' ').replace(']', '')
        # print(line)
        parts = line.strip().split(' ')
        item = {
            'status': parts[0],
            'type': parts[1],
            'size': parts[-2],
            'url': parts[-1]
        }
        result.append(item)

    # 将JSON数组打印出来
    json_data = json.dumps(result, indent=2)
    return json_data


if __name__ == '__main__':
    text_to_json()
