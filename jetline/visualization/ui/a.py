import os

def format_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    formatted_lines = []
    for line in lines:
        formatted_line = ""
        for char in line:
            formatted_line += char
            if char == '>':
                formatted_line += '\n'
        formatted_lines.append(formatted_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(formatted_lines)

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_file_path = os.path.join(current_dir, 'index.html')
    if os.path.exists(html_file_path):
        format_html_file(html_file_path)
        print("HTML file formatted successfully.")
    else:
        print("No index.html file found in the current directory.")

if __name__ == "__main__":
    main()
