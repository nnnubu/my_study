import requests, time, os
from flask import Flask, jsonify, render_template, abort, send_from_directory, request, Response, render_template_string

from js逆向学习.抖音逆向.博主主页信息获取 import get_info
app = Flask(__name__)


def safe_join(directory, filename):
    base_path = os.path.abspath(directory)
    target_path = os.path.join(base_path, filename)
    if not target_path.startswith(base_path):
        abort(403)
    return target_path


@app.route('/')
def home():
    return "Welcome to the Flask app!"

@app.route('/data', methods=['GET'])
def get_data():
    timestamp = int(time.time())
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
    url = f'https://captcha1.scrape.center/api/init?t={timestamp}'
    resp = requests.get(url, headers)
    data = resp.text
    resp.close()
    return data

@app.route('/douyin',methods=['GET','POST'])
def get_douyin():
    if request.method == 'POST':
        id = request.form.get('id')
    return get_info(id)

@app.route('/get_music_url')
def get_music_url():
    filename = request.args.get('filename')
    # 这里可以根据filename生成音频文件的URL
    # 假设的音频文件位于C:/爬虫战果/音乐目录下
    url = f'/music?filename={filename}'
    return jsonify({'url': url})


@app.route('/music')
def audio():
    filename = request.args.get('filename')
    directory = "C:/爬虫战果/音乐"
    # directory = ""
    file_path = safe_join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(directory, filename)


@app.route('/source/<path:filename>')
def source(filename):
    directory = 'C:/前端学习'
    file_path = safe_join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(directory, filename)


@app.route('/myhtml')
def web():
    # return render_template('前端学习.html')

    with open('C:/前端学习/前端学习.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    rendered_content = render_template_string(html_content)
    return Response(rendered_content, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)
