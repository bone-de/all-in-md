import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import zipfile
import os
import chardet


def extract_zip(zip_path, extract_to):
    """
    解压 ZIP 文件到指定目录
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to


def merge_files(folder_path, output_file, extensions):
    """
    将符合扩展名的文件内容合并到一个 Markdown 格式的 txt 文件中
    """
    count = 0
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as content_file:
                            content = content_file.read()
                    except UnicodeDecodeError:
                        encoding = chardet.detect(open(file_path, 'rb').read())['encoding']
                        with open(file_path, 'r', encoding=encoding) as content_file:
                            content = content_file.read()
                    # Markdown 格式输出
                    out_file.write(f"## File: {file_path}\n```plaintext\n{content}\n```\n\n")
                    count += 1
    return count


def upload_and_process():
    """
    上传和处理 ZIP 文件
    """
    zip_path = filedialog.askopenfilename(filetypes=[("ZIP 文件", "*.zip")])
    if not zip_path:
        return

    output_dir = "extracted_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extract_zip(zip_path, output_dir)

    extensions = simpledialog.askstring("文件类型", "请输入需要处理文件扩展名，用逗号分隔（例如：.py,.txt）:")
    if extensions:
        extensions = extensions.split(',')
    else:
        extensions = ['.txt', '.py']  # 默认值

    output_file = "output.md"
    count = merge_files(output_dir, output_file, extensions)

    messagebox.showinfo("完成", f"处理完成，共合并 {count} 个文件。输出文件位于 {output_file}")


def main():
    root = tk.Tk()
    root.title("ZIP 文件处理器")
    root.geometry("400x200")

    # 设置字体
    app_font = font.Font(family="Arial", size=12)

    btn_upload = tk.Button(root, text="上传并处理 ZIP 文件", command=upload_and_process, font=app_font)
    btn_upload.pack(expand=True, pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
