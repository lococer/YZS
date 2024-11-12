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
import re
from urllib.parse import urlencode
from flask_cors import CORS

# 配置文件日志处理器
file_handler = logging.FileHandler('app.log')  # 指定日志文件
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 设置格式
file_handler.setFormatter(formatter)

# 创建 Logger 对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别
logger.addHandler(file_handler)  # 添加文件处理器


app = Flask(__name__)
CORS(app)

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
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'rating': self.rating,
            'ratingsum': self.ratingsum,
            'img': self.img,
            'tags': self.tags,
           'summary': self.summary,
            'genre': self.genre
        }
    
class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    birthplace = db.Column(db.String(100))
    summary = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'sex': self.sex,
            'birthday': self.birthday,
            'birthplace': self.birthplace,
            'summary': self.summary
        }

class Relationships(db.Model):
    __tablename__ = 'relationships'

    movie_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer)
    role = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)

class Comment(db.Model):
    __tablename__ = 'comment'

    username = db.Column(db.String(100))
    movieid = db.Column(db.Integer)
    comment = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)

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
    # return jsonify(movies=[movie.serialize() for movie in movies])

# 示例 API 路由
@app.route('/api/movies', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()  # 从数据库获取所有电影 
    for movie in all_movies:
        movie.img = encode_image_url(movie.img)
    all_movies = all_movies[0:20]
    return jsonify([movie.serialize() for movie in all_movies])

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def movieinfo(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return abort(404)  # 如果没有找到电影，返回404错误
    
    movie.img = encode_image_url(movie.img)

    return jsonify(movie.serialize())

    people = get_people_by_movie_id(movie_id)

    for person in people:
        person.img = encode_image_url(person.img)
        logger.debug(f"Actor ID: {person.id}, Name: {person.name}")
    
    movie.directorName = get_people_by_movie_id(movie_id, role="director")[0].name if get_people_by_movie_id(movie_id, role="director") else None

    logger.debug(movie)

    return render_template('movieinfo.html', movie=movie, actors=people)

@app.route('/api/persons', methods=['GET'])
def get_persons():
    all_persons = Person.query.all()  # 从数据库获取所有人员信息
    all_persons = all_persons[0:20]
    for person in all_persons:
        person.img = encode_image_url(person.img)
    logger.debug(all_persons)
    return jsonify([person.serialize() for person in all_persons])

@app.route('/api/persons/<int:person_id>', methods=['GET'])
def personinfo(person_id):
    person = Person.query.get(person_id)
    if not person:
        return abort(404)  # 如果没有找到人员信息，返回404错误
    
    person.img = encode_image_url(person.img)

    return jsonify(person.serialize())


@app.route('/movies/search')
def search_movies():
    queries = request.args.getlist('q[]')
    categories = request.args.getlist('category[]')

    logger.debug(queries)
    logger.debug(categories)

    logger.debug(f"类别: {categories}，查询: {queries}")

    # 初始化查询
    query = Movie.query

    # 处理演员名称的列表以避免重复连接
    actor_ids = set()

    # 逐个添加过滤条件
    for category, query_text in zip(categories, queries):
        logger.debug(f"类别: {category}, 查询: {query_text}")
        if category == 'movieName':
            query = query.filter(Movie.name.ilike(f"%{query_text}%"))
        elif category == 'year':
            try:
                year = int(query_text)
                query = query.filter(Movie.year == year)
            except ValueError:
                logger.warning(f"无效年份: {query_text}")
                continue  # 忽略无效的年份
        elif category == 'country':
            query = query.filter(Movie.country.ilike(f"%{query_text}%"))
        elif category == 'actorName':  # 新增对演员名称的处理
            actor = Person.query.filter(Person.name.ilike(f"%{query_text}%")).first()  # 获取第一个匹配的演员
            if actor:
                actor_ids.add(actor.id)  # 加入演员 ID 集合
            else:
                logger.warning(f"未找到演员: {query_text}")
                continue  # 忽略未找到的演员
        else:
            logger.warning(f"未知类别: {category}")
            continue  # 忽略未知类别

    if actor_ids:
        # 确保从 Movie 表开始，并与 Relationships 表联接
        query = query.join(Relationships, Relationships.movie_id == Movie.id)

        # 添加过滤条件：筛选 person_id 在 actor_ids 列表中的记录
        query = query.filter(Relationships.person_id.in_(actor_ids))

    # 执行查询
    search_results = query.all()

    # 获取当前页数
    page = request.args.get('page', 1, type=int)

    # 使用分页函数
    movies, total_pages = paginate_items(search_results, page)

    # 为每个电影封面编码URL
    for movie in movies:
        movie.img = encode_image_url(movie.img)

    return render_template('movies.html', movies=movies, total_pages=total_pages, current_page=page, query=query)



# 查询特定电影的所有演员
def get_people_by_movie_id(movie_id, role=None):
    query = (
        db.session.query(Person)
        .select_from(Relationships)
        .join(Person, Relationships.person_id == Person.id)
        .filter(Relationships.movie_id == movie_id)
    )
    if( role is not None ):
        query = query.filter(Relationships.role == role)

    return query.all()

# @app.route('/movies/<int:movie_id>')
# def movieinfo(movie_id):
#     movie = Movie.query.get(movie_id)
#     if not movie:
#         return abort(404)  # 如果没有找到电影，返回404错误
    
#     movie.img = encode_image_url(movie.img)

#     people = get_people_by_movie_id(movie_id)

#     for person in people:
#         person.img = encode_image_url(person.img)
#         logger.debug(f"Actor ID: {person.id}, Name: {person.name}")
    
#     movie.directorName = get_people_by_movie_id(movie_id, role="director")[0].name if get_people_by_movie_id(movie_id, role="director") else None

#     logger.debug(movie)

#     return render_template('movieinfo.html', movie=movie, actors=people)

@app.route('/people')
def people():
    # 获取所有人员信息
    all_people = Person.query.all()
    
    # 获取当前页数，默认为1
    page = request.args.get('page', 1, type=int)
    
    # 使用分页函数
    people, total_pages = paginate_items(all_people, page)
    
    # 日志
    # logger.debug(f"Query all people, total: {len(all_people)}, page: {page}")
    # logger.debug(f"First person: {people[0].name if people else 'No people found'}")

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
            .limit(10)  # 限制返回前10个合作演员
            .all()
        )

        # logger.debug(coactors)
        
        # 将共同演员的 ID 和名称加入结果
        result["actors"] = [{"id": actor.id, "name": actor.name} for actor in coactors]
        
        # 获取共同演员之间的所有组合
        actor_list = [(actor.id, actor.name) for actor in coactors]  # 获取演员 ID 和名称的列表
        # logger.debug(str(len(actor_list)))

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
                    "value": len(common_movie_ids),  # 可以选择更有意义的值
                    # "common_movies": [Movie.query.get(movie_id) for movie_id in common_movie_ids]
                    "url": create_search_url("", ["actorName", "actorName"], [actor1_name, actor2_name]),
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

@app.route('/require/movie_relationship/<int:movie_id>')
def require_movie_relationship(movie_id):
    """返回 JSON，指定电影的所有演员和导演"""
    logger.debug(f"Query movie {movie_id} information")

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    # 查询与电影相关的演员和导演
    relationships = Relationships.query.filter_by(movie_id=movie_id).all()
    logger.debug(f"Total relationships found: {len(relationships)}")

    actors = []
    director = None

    for relationship in relationships:
        person = Person.query.get(relationship.person_id)
        logger.debug(f"Person ID: {person.id if person else 'None'}, Name: {person.name if person else 'None'}, Role: {relationship.role}")
        if relationship.role == "director":
            director = person.name if person else None
        else:
            if person:
                actors.append(person.name)
    
    # actors = actors[:5]  # 限制返回前 5 个演员

    actors = list(set(actors))[:20]  # 去重

    result = {}

    # 构建返回的数据结构以适应 ECharts graph
    result["actors"] = [{"name": movie.name, "value": "电影"}]  # 添加电影节点
    if director:
        result["actors"].append({"name": director, "value": "导演"})  # 添加导演节点
    for actor in actors:
        result["actors"].append({"name": actor, "value": "参演"})  # 添加演员节点

    # 创建链接
    links = []
    if director:
        links.append({"source": movie.name, "target": director})  # 电影到导演的链接
    for actor in actors:
        links.append({"source": movie.name, "target": actor})  # 电影到演员的链接

    # 打印调试信息以检查节点和链接
    # logger.debug(f"Nodes: {nodes}")
    # logger.debug(f"Links: {links}")

    # result = {
    #     'actors': nodes,
    #     'links': links,
    # }

    # result = {}
    # result['actors'] = nodes
    result["links"] = links
    
    logger.debug(result)

    return jsonify(result)

@app.route('/require/movie_comments/<int:movie_id>')
def require_movie_comments(movie_id):
    """返回 JSON，指定电影的所有评论"""
    logger.debug(f"Query movie {movie_id} comments")

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    # 查询与电影相关的评论
    comments = Comment.query.filter_by(movieid=movie_id).all()
    logger.debug(f"Total comments found: {len(comments)}")

    # 构建返回的数据结构
    result = []
    for comment in comments:
        result.append({
            'username': comment.username,
            'comment': comment.comment,
        })

    # 打印调试信息以检查结果
    # logger.debug(f"Comments: {result}")
    return jsonify(result)

@app.route('/people_relationship/<int:people_id>')
def people_relationship(people_id):
    logger.debug('enter people_relationship')
    return render_template("people_relationship.html", people_id=people_id)


@app.route('/people/search')
def search_people():
    queries = request.args.getlist('q[]')  # 获取所有查询参数
    categories = request.args.getlist('category[]')  # 获取所有类别参数

    logger.debug(queries)
    logger.debug(categories)

    logger.debug(f"类别: {categories}，查询: {queries}")

    # 初始化查询
    query = Person.query

    # 逐个添加过滤条件
    for category, query_text in zip(categories, queries):
        logger.debug(f"类别: {category}, 查询: {query_text}")
        if category == 'name':
            query = query.filter(Person.name.ilike(f"%{query_text}%"))
        elif category == 'sex':
            query = query.filter(Person.sex.ilike(f"%{query_text}%"))
        elif category == 'birthplace':
            query = query.filter(Person.birthplace.ilike(f"%{query_text}%"))

    # 执行查询
    search_results = query.all()

    # 获取当前页数
    page = request.args.get('page', 1, type=int)

    # 使用分页函数
    people, total_pages = paginate_items(search_results, page)

    # 为每个人物编码图片 URL
    for person in people:
        person.img = encode_image_url(person.img)

    return render_template('people.html', people=people, total_pages=total_pages, current_page=page, query=queries)


# @app.route('/people/<int:person_id>')
# def personinfo(person_id):
#     person = Person.query.get(person_id)
#     if not person:
#         return abort(404)  # 如果没有找到演员，返回404错误

#     person.img = encode_image_url(person.img)

#     # 查询与该演员相关的所有电影
#     movies = (db.session.query(Movie)
#           .join(Relationships, Relationships.movie_id == Movie.id)
#           .filter(Relationships.person_id == person_id)
#           .all())

#     for movie in movies:
#         movie.img = encode_image_url(movie.img)
#     # 日志记录
#     logger.debug(f"Actor ID: {person.id}, Name: {person.name}")
#     logger.debug(f"Movies for {person.name}: {[movie.name for movie in movies]}")

#     return render_template('personinfo.html', person=person, movies=movies)


@app.route('/index')
def index():
    return render_template("index.html")

# 代理图片的路由，接收 Base64 编码的 URL
@app.route('/proxy-image/<path:encoded_url>')
def proxy_image(encoded_url):
    # logger.debug("get picture") 
    # logger.debug(encoded_url)
    # logger.debug(base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    # print("get movie picture", encoded_url, base64.urlsafe_b64decode(encoded_url).decode('utf-8'))
    try:
        # logger.debug("OK0")
        # Base64 解码 URL
        image_url = base64.urlsafe_b64decode(encoded_url).decode('utf-8')
        
        # logger.debug("OK1")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 请求图片数据
        response = requests.get(image_url, headers=headers)

        # logger.debug("OK2")
        # logger.debug(f"Decoded image URL: {image_url}")
        # logger.debug(f"Image request status: {response.status_code}")
        
        # logger.debug("OK3")
        if response.status_code == 200:
            img = BytesIO(response.content)
            return send_file(img, mimetype='image/webp')
        else:
            return abort(404)  # 如果图片获取失败，则返回 404 错误
    except Exception as e:
        logger.debug("picture failed" + e)
        return abort(400)  # 如果解码出错，返回 400 错误

def create_search_url(base_url, categories, queries):
    # 构建查询参数
    params = []
    for category, query in zip(categories, queries):
        params.append(('category[]', category))
        params.append(('q[]', query))
    
    # 使用 urlencode 构建完整的查询字符串
    query_string = urlencode(params, doseq=True)
    return f"{base_url}?{query_string}"

def split_name(name):
    # 使用正则表达式分离中文和英文
    chinese_part = ''.join(re.findall(r'[\u4e00-\u9fa5]+', name))  # 匹配中文字符
    english_part = ''.join(re.findall(r'[A-Za-z]+', name))  # 匹配英文字符
    
    return chinese_part, english_part

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
