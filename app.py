from flask import Flask, abort, render_template, request, send_file
import requests
from io import BytesIO
import base64
from flask_sqlalchemy import SQLAlchemy
import logging
from jinja2 import Template

# 配置文件日志处理器
file_handler = logging.FileHandler('app.log')  # 指定日志文件
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 设置格式
file_handler.setFormatter(formatter)

# 创建 Logger 对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别
logger.addHandler(file_handler)  # 添加文件处理器


app = Flask(__name__)

# 注册 max 和 min 函数
app.jinja_env.globals.update({
    'max': max,
    'min': min,
    'range': range,
})

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leo@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建数据库实例
db = SQLAlchemy(app)

# 定义模型
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ratingsum = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text, nullable=False)
    tags = db.Column(db.ARRAY(db.String), nullable=True)  # 使用数组类型
    summary = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Movie {self.name}>'

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/test')
def test():
    return render_template("hello.html")

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/<username>')
def greet(username):
    # return 'Hello'
    return f'Hello {username}'

@app.route('/movies')
def movies():
    # 自定义函数
    def get_encode_url(image_url):
        """ 将数据库中的封面url转换成Base64编码 """
        encoded_url = base64.urlsafe_b64encode(image_url.encode('utf-8')).decode('utf-8')
        return encoded_url

    # 获取所有电影
    all_movies = Movie.query.all()
    
    # 设置每页电影数量
    movies_per_page = 20
    # 获取当前页数，默认为1
    page = request.args.get('page', 1, type=int)
    
    # 计算总页数
    total_movies = len(all_movies)
    total_pages = (total_movies + movies_per_page - 1) // movies_per_page

    # 计算当前页的电影
    start = (page - 1) * movies_per_page
    end = start + movies_per_page
    movies = all_movies[start:end]

    # 日志
    logger.debug("Query all movies and size is " + str(total_movies))
    logger.debug("The first movie " + str(movies[0]) if movies else "No movies found")

    for movie in movies:
        movie.img = get_encode_url(movie.img)

    return render_template("movies.html", movies=movies, total_pages=total_pages, current_page=page)

@app.route('/index')
def index():
    return render_template("index.html")

# 代理图片的路由，接收 Base64 编码的 URL
@app.route('/proxy-image/<path:encoded_url>')
def proxy_image(encoded_url):
    logger.debug("get movie picture") 
    # logger.debug(encoded_url)
    # logger.debug(base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    # print("get movie picture", encoded_url, base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    try:
        # Base64 解码 URL
        image_url = base64.urlsafe_b64decode(encoded_url).decode('utf-8')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 请求图片数据
        response = requests.get(image_url, headers=headers)

        logger.debug(f"Decoded image URL: {image_url}")
        logger.debug(f"Image request status: {response.status_code}")
        
        if response.status_code == 200:
            img = BytesIO(response.content)
            return send_file(img, mimetype='image/webp')
        else:
            return abort(404)  # 如果图片获取失败，则返回 404 错误
    except Exception as e:
        return abort(400)  # 如果解码出错，返回 400 错误

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)




"""
电影模块：列出所有 查询电影 查看电影详情
演员关系图
电影评分预测

"""