import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def convert_markdown(markdown_text):
    """
    将Markdown格式的文本转换为特定格式：
    - # 标题 -> [h1]标题[/h1]
    - ## 标题 -> [h2]标题[/h2]
    - ### 标题 -> [h3]标题[/h3]
    - ####及以上标题 -> 去除#后作为文本
    - **加粗** -> <strong>加粗</strong>
    - *斜体* -> <em>斜体</em>
    - 无序列表 (- 或 * 开头) -> <ul>和<li>标签
    - 有序列表 (数字. 开头) -> <ol>和<li>标签
    - 表格 -> <table>和<tr><td>标签
    """
    lines = markdown_text.split('\n')
    converted_lines = []
    in_ul = False  # 是否在无序列表中
    in_ol = False  # 是否在有序列表中
    in_table = False  # 是否在表格中

    for line in lines:
        # 处理标题
        if line.startswith('#'):
            # 先关闭可能存在的列表或表格
            if in_ul:
                converted_lines.append('</ul>')
                in_ul = False
            if in_ol:
                converted_lines.append('</ol>')
                in_ol = False
            if in_table:
                converted_lines.append('</table>')
                in_table = False

            # 计算#的数量
            hash_count = 0
            for char in line:
                if char == '#':
                    hash_count += 1
                else:
                    break

            # 提取标题内容（去除#和可能的空格）
            content = line[hash_count:].strip()

            # 处理1-3个#的标题
            if 1 <= hash_count <= 3:
                converted_line = f'[h{hash_count}]{content}[/h{hash_count}]'
                converted_lines.append(converted_line)
            else:
                # 四级及以上标题，去除#后作为普通文本处理
                converted_lines.append(content)
            continue

        # 处理表格
        if '|' in line and re.match(r'^\s*\|.*\|\s*$', line):
            # 如果是表格分隔行，跳过
            if re.match(r'^\s*\|[-\s|]+\|\s*$', line):
                continue

            # 开始表格
            if not in_table:
                converted_lines.append('<table>')
                in_table = True

            # 处理表格行
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            row = '<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>'
            converted_lines.append(row)
            continue

        # 处理无序列表 (- 或 * 开头)
        ul_match = re.match(r'^[*-]\s+(.*)$', line)
        if ul_match:
            # 关闭有序列表或表格（如果在其中）
            if in_ol:
                converted_lines.append('</ol>')
                in_ol = False
            if in_table:
                converted_lines.append('</table>')
                in_table = False

            content = ul_match.group(1)
            # 处理内容中的加粗和斜体
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)

            if not in_ul:
                converted_lines.append('<ul>')
                in_ul = True
            converted_lines.append(f'  <li>{content}</li>')
            continue

        # 处理有序列表（数字. 开头）
        ol_match = re.match(r'^\d+\.\s+(.*)$', line)
        if ol_match:
            # 关闭无序列表或表格（如果在其中）
            if in_ul:
                converted_lines.append('</ul>')
                in_ul = False
            if in_table:
                converted_lines.append('</table>')
                in_table = False

            content = ol_match.group(1)
            # 处理内容中的加粗和斜体
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)

            if not in_ol:
                converted_lines.append('<ol>')
                in_ol = True
            converted_lines.append(f'  <li>{content}</li>')
            continue

        # 如果不是列表项但在列表或表格中，需要关闭
        if in_ul:
            converted_lines.append('</ul>')
            in_ul = False
        if in_ol:
            converted_lines.append('</ol>')
            in_ol = False
        if in_table:
            converted_lines.append('</table>')
            in_table = False

        # 处理普通行中的加粗和斜体
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)

        # 添加处理后的行
        converted_lines.append(line)

    # 处理文档结束时仍在列表或表格中的情况
    if in_ul:
        converted_lines.append('</ul>')
    if in_ol:
        converted_lines.append('</ol>')
    if in_table:
        converted_lines.append('</table>')

    return '\n'.join(converted_lines)


@app.route('/convert', methods=['POST'])
def convert_text():
    data = request.get_json()
    if not data or 'markdown_text' not in data:
        return jsonify({'error': 'No markdown_text provided'}), 400

    markdown_text = data['markdown_text']
    converted_text = convert_markdown(markdown_text)
    return jsonify({'converted_text': converted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)