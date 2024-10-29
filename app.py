from itertools import combinations
from flask import Flask, abort, render_template, request, send_file, jsonify
import requests
from io import BytesIO
import base64
from flask_sqlalchemy import SQLAlchemy
import logging
from jinja2 import Template
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
import getpass
if( getpass.getuser() != 'lococ' ):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leo@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lococ:lococ@localhost:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 创建连接引擎和会话
engine = create_engine('postgresql://postgres:leo@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

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
    
class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    birthplace = db.Column(db.String(100))
    summary = db.Column(db.String(100))

class Relationships(db.Model):
    __tablename__ = 'relationships'

    movie_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(100))


# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/test')
def test():
    return render_template("people_relationship.html")

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/<username>')
def greet(username):
    # return 'Hello'
    return f'Hello {username}'

def encode_image_url(image_url):
    """将数据库中的封面url转换成Base64编码"""
    if image_url:
        return base64.urlsafe_b64encode(image_url.encode('utf-8')).decode('utf-8')
    return ''

def paginate_items(items, page, items_per_page=20):
    """分页函数"""
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_items = items[start:end]
    
    return paginated_items, total_pages

@app.route('/movies')
def movies():
    # 获取所有电影
    all_movies = Movie.query.all()
    
    # 获取当前页数，默认为1
    page = request.args.get('page', 1, type=int)
    
    # 使用分页函数
    movies, total_pages = paginate_items(all_movies, page)
    
    # 为每个电影封面编码URL
    for movie in movies:
        movie.img = encode_image_url(movie.img)
    
    # 日志
    logger.debug(f"Query all movies, total: {len(all_movies)}, page: {page}")
    logger.debug(f"First movie: {movies[0].name if movies else 'No movies found'}")

    return render_template("movies.html", movies=movies, total_pages=total_pages, current_page=page)

@app.route('/movies/search')
def search_movies():
    query = request.args.get('q', '')

    logger.debug(f"查询{query}电影")
    
    # 使用模糊查询搜索电影
    search_pattern = f"%{query}%"
    search_results = Movie.query.filter(Movie.name.ilike(search_pattern)).all()

    # 获取当前页数
    page = request.args.get('page', 1, type=int)

    # 使用分页函数
    movies, total_pages = paginate_items(search_results, page)

    # 为每个电影封面编码URL
    for movie in movies:
        movie.img = encode_image_url(movie.img)

    return render_template('movies.html', movies=movies, total_pages=total_pages, current_page=page, query=query)

# 查询特定电影的所有演员
def get_people_by_movie_id(movie_id):
    query = (
        db.session.query(Person)
        .select_from(Relationships)
        .join(Person, Relationships.person_id == Person.id)
        .filter(Relationships.movie_id == movie_id)
    )
    return query.all()

@app.route('/movies/<int:movie_id>')
def movieinfo(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return abort(404)  # 如果没有找到电影，返回404错误
    
    movie.img = encode_image_url(movie.img)

    people = get_people_by_movie_id(movie_id)

    for person in people:
        person.img = encode_image_url(person.img)
        logger.debug(f"Actor ID: {person.id}, Name: {person.name}")

    return render_template('movieinfo.html', movie=movie, actors=people)

@app.route('/people')
def people():
    # 获取所有人员信息
    all_people = Person.query.all()
    
    # 获取当前页数，默认为1
    page = request.args.get('page', 1, type=int)
    
    # 使用分页函数
    people, total_pages = paginate_items(all_people, page)
    
    # 日志
    logger.debug(f"Query all people, total: {len(all_people)}, page: {page}")
    logger.debug(f"First person: {people[0].name if people else 'No people found'}")

    for person in people:
        person.img = encode_image_url(person.img)

    return render_template("people.html", people=people, total_pages=total_pages, current_page=page)

def find_coactors(person_id):
    result = {}
    try:
        logger.debug("start query coactors")
        
        # 查询该演员参与过的所有电影，包括自己
        actor_movies = db.session.query(Relationships.movie_id).filter_by(person_id=person_id).subquery()

        # 查询这些电影的所有演员，并计算与指定演员的合作次数
        coactors = (
            db.session.query(
                Person.id,
                Person.name,
                func.count(Relationships.movie_id).label('coactor_count')
            )
            .join(Relationships, Relationships.person_id == Person.id)
            .filter(Relationships.movie_id.in_(actor_movies))
            .group_by(Person.id, Person.name)
            .order_by(func.count(Relationships.movie_id).desc())
            .limit(15)  # 限制返回前10个合作演员
            .all()
        )

        logger.debug(coactors)
        
        # 将共同演员的 ID 和名称加入结果
        result["actors"] = [{"id": actor.id, "name": actor.name} for actor in coactors]
        
        # 获取共同演员之间的所有组合
        actor_list = [(actor.id, actor.name) for actor in coactors]  # 获取演员 ID 和名称的列表
        logger.debug(str(len(actor_list)))

        # 查询所有共同电影 ID
        coactor_pairs = [(actor1.id, actor2.id) for actor1, actor2 in combinations(coactors, 2)]
        movie_relations = (
            db.session.query(Relationships.movie_id, Relationships.person_id)
            .filter(Relationships.person_id.in_([actor_id for actor_id, _ in coactor_pairs]))
            .all()
        )

        # 将电影关系整理到字典中
        movie_dict = {}
        for movie_id, person_id in movie_relations:
            if movie_id not in movie_dict:
                movie_dict[movie_id] = set()
            movie_dict[movie_id].add(person_id)

        # 组装每对演员的共同电影
        relationships = []
        for actor1_id, actor2_id in coactor_pairs:
            common_movie_ids = [
                movie_id for movie_id, ids in movie_dict.items()
                if actor1_id in ids and actor2_id in ids
            ]

            if common_movie_ids:
                actor1_name = next(actor.name for actor in coactors if actor.id == actor1_id)
                actor2_name = next(actor.name for actor in coactors if actor.id == actor2_id)
                relationships.append({
                    "source": actor1_name,
                    "target": actor2_name,
                    "common_movie_ids": common_movie_ids,
                    "value": len(common_movie_ids)  # 可以选择更有意义的值
                })

        result["links"] = relationships
        logger.debug("end query coactors")

    except Exception as err:
        logger.error("query coactors error: " + str(err))
    
    logger.debug(result)
    return jsonify(result)

@app.route('/require/people_relationship/<int:people_id>')
def require_people_relationship(people_id):
    """返回json,指定演员合作过的演员,以及合作过的次数
    """
    coactors = find_coactors(person_id=people_id)

    return coactors

@app.route('/people_relationship/<int:people_id>')
def people_relationship(people_id):
    logger.debug('enter people_relationship')
    return render_template("people_relationship.html", people_id=people_id)


@app.route('/people/search')
def search_people():
    query = request.args.get('q', '')

    logger.debug(f"查询{query}影人")
    
    # 使用模糊查询搜索电影
    search_pattern = f"%{query}%"
    search_results = Person.query.filter(Person.name.ilike(search_pattern)).all()

    # 获取当前页数
    page = request.args.get('page', 1, type=int)

    # 使用分页函数
    people, total_pages = paginate_items(search_results, page)

    # 为每个电影封面编码URL
    for person in people:
        person.img = encode_image_url(person.img)

    return render_template('people.html', people=people, total_pages=total_pages, current_page=page, query=query)

@app.route('/people/<int:person_id>')
def personinfo(person_id):
    person = Person.query.get(person_id)
    if not person:
        return abort(404)  # 如果没有找到演员，返回404错误

    person.img = encode_image_url(person.img)

    # 查询与该演员相关的所有电影
    movies = (db.session.query(Movie)
          .join(Relationships, Relationships.movie_id == Movie.id)
          .filter(Relationships.person_id == person_id)
          .all())

    for movie in movies:
        movie.img = encode_image_url(movie.img)
    # 日志记录
    logger.debug(f"Actor ID: {person.id}, Name: {person.name}")
    logger.debug(f"Movies for {person.name}: {[movie.name for movie in movies]}")

    return render_template('personinfo.html', person=person, movies=movies)


@app.route('/index')
def index():
    return render_template("index.html")

# 代理图片的路由，接收 Base64 编码的 URL
@app.route('/proxy-image/<path:encoded_url>')
def proxy_image(encoded_url):
    logger.debug("get picture") 
    logger.debug(encoded_url)
    logger.debug(base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    # print("get movie picture", encoded_url, base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    try:
        logger.debug("OK0")
        # Base64 解码 URL
        image_url = base64.urlsafe_b64decode(encoded_url).decode('utf-8')
        
        logger.debug("OK1")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 请求图片数据
        response = requests.get(image_url, headers=headers)

        logger.debug("OK2")
        logger.debug(f"Decoded image URL: {image_url}")
        logger.debug(f"Image request status: {response.status_code}")
        
        logger.debug("OK3")
        if response.status_code == 200:
            img = BytesIO(response.content)
            return send_file(img, mimetype='image/webp')
        else:
            return abort(404)  # 如果图片获取失败，则返回 404 错误
    except Exception as e:
        logger.debug("picture failed" + e)
        return abort(400)  # 如果解码出错，返回 400 错误

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
