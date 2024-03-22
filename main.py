import random
from movies import movies

# 抽演员的池子，可以增添演员进池子
actor_pool = ['刘青云','吴镇宇', '古天乐', '张智霖', '黄秋生', '刘德华', '黎明', '梁朝伟', '周润发', '郑伊健','曾志伟']

# 随机选择3个演员并打印
selected_actors = []
# 修改下面range里面的数字可以控制抽几个演员刘伟强
for i in range(2):
    actor = random.choice(actor_pool)
    actor_pool.remove(actor)
    selected_actors.append(actor)
    print('抽出来第{}位是：{}'.format(i + 1, actor))

selected_movies = []
for movie, info in movies.items():
    if set(selected_actors).issubset(set(info['actors'])):
        selected_movies.append(movie + ', 导演：' + info['director'])

if selected_movies:
    print('他们共同参演的电影有: ', ', '.join(selected_movies))
else:
    print('电影库里没找到他们合作的电影呢。')
