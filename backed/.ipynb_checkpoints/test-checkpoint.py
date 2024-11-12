from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import Movie
import matplotlib.pyplot as plt

engine = create_engine('postgresql://postgres:leo@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

years = list(range(1970, 2020))
average_ratings = []

# 查询每年的平均评分
for year in years:
    avg_rating = session.query(func.avg(Movie.rating)).filter(Movie.year == year).scalar()
    average_ratings.append(avg_rating if avg_rating is not None else 0)  # 如果没有数据则使用0

# 关闭会话
session.close()

# 绘制折线图
plt.figure(figsize=(10, 5))
plt.plot(years, average_ratings, marker='o', linestyle='-', color='b')
plt.title('Average Movie Rating from 1970 to 2019')
plt.xlabel('Year')
plt.ylabel('Average Rating')
plt.xticks(years, rotation=45)  # 旋转年份标签以便更好地显示
plt.grid()
plt.tight_layout()  # 调整布局以避免标签被遮挡
plt.show()