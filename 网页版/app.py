from flask import Flask, render_template, request, send_from_directory
import zipfile
import os
import chardet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXTRACTED_FOLDER'] = 'extracted_files'
app.config['OUTPUT_FILE'] = 'output.md'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件部分'
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件'
    if file and file.filename.endswith('.zip'):
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(zip_path)
        extract_zip(zip_path, app.config['EXTRACTED_FOLDER'])
        extensions = request.form.get('extensions', '.txt,.py').split(',')
        merge_files(app.config['EXTRACTED_FOLDER'], app.config['OUTPUT_FILE'], extensions)
        return send_from_directory(directory='.', path=app.config['OUTPUT_FILE'], as_attachment=True)
    return '无效的文件类型'

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def merge_files(folder_path, output_file, extensions):
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
                    out_file.write(f"## File: {file_path}\n```plaintext\n{content}\n```\n\n")

if __name__ == '__main__':
    app.run(debug=True)
