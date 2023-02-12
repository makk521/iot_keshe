from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Flask内部会自动打开这个文件，并读取内容，将内容给用户返回。
    # 默认：去当前项目目录的templates文件夹中找。
    return('hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0')