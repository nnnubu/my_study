import sys

import pymysql, os
from js逆向学习.拷贝漫画逆向.functions import *

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password=os.getenv('mysql_password'),
)

try:
    with connection.cursor() as cursor:
        # 开始事务
        connection.begin()

        cursor.execute('create database if not exists Manga_Data')
        cursor.execute('use Manga_Data;')
        cursor.execute('''
            create table if not exists Mangas (
                comic_id int auto_increment primary key ,
                name varchar(255) not null ,
                cover varchar(255)
            );
        ''')
        cursor.execute('''
            ALTER TABLE Mangas AUTO_INCREMENT = 10000;
        ''')
        cursor.execute('''
            create table if not exists ImageData (
                img_id int auto_increment primary key ,
                comic_id int not null ,
                img_url varchar(255) not null ,
                name varchar(255) ,
                foreign key (comic_id) references Mangas(comic_id)
            );
        ''')
        cursor.execute('''
                    ALTER TABLE ImageData AUTO_INCREMENT = 10000;
                ''')

        name = input('请输入搜索漫画名：')
        # name = '心之程序'
        count = 1
        comic_id = 10000
        List = Search_Manga(name)
        if not List:
            print('没有搜索结果')
            sys.exit()
        for i in List:
            print(f'{count}.    {i.name}    {i.path_word}   {i.cover}')
            count += 1

        target_manga = List[int(input("请输入目标漫画序号：")) - 1]
        print(vars(target_manga))

        # 检查数据库中是否已经有了任何数据
        cursor.execute('''
            SELECT * FROM Mangas LIMIT 1
        ''')
        result_any_data = cursor.fetchone()

        # 检查数据库中是否已经存在同名的漫画
        cursor.execute('''
            SELECT * FROM Mangas WHERE name = %s
        ''', (target_manga.name,))
        result_same_name = cursor.fetchone()

        if result_any_data is None:
            # 如果数据库中没有任何数据，则使用 comic_id 为 10000
            comic_id = 10000
        else:
            # 如果数据库中已经有数据，则让数据库自动生成 comic_id
            comic_id = None

        if result_same_name is None:
            # 如果数据库中不存在同名的漫画，则插入新的漫画数据
            if comic_id is None:
                cursor.execute('''
                    insert into Mangas (name, cover)
                    values (%s, %s)
                ''', (target_manga.name, target_manga.cover))
                # 获取插入后的自动生成的主键值
                comic_id = cursor.lastrowid
            else:
                cursor.execute('''
                    insert into Mangas (comic_id, name, cover)
                    values (%s, %s, %s)
                ''', (comic_id, target_manga.name, target_manga.cover))
        else:
            # 如果数据库中已经存在同名的漫画，则不继续执行数据的录入操作
            print(f"漫画 '{target_manga.name}' 已经存在，跳过插入。")
            sys.exit()

        info = [i for i in Get_Manga(target_manga.path_word)]
        print(info)

        for i in info:
            img_list = {j + 1: value for j, value in enumerate([j['url'] for j in Download_manga(i["id"])])}
            data = json.dumps({i['name']: img_list}, ensure_ascii=False)
            url_list = list(img_list.values())
            for j in url_list:
                print(f'正在插入{j}...')
                cursor.execute('''
                    insert into ImageData (comic_id,img_url,name)
                    values (%s,%s,%s)
                ''', (comic_id, j, i['name']))
        print('已获取所有内容。')

        # 提交事务
        connection.commit()

        cursor.execute('show tables;')
        result = cursor.fetchall()
        print(result)
except pymysql.MySQLError as e:
    # 如果出现错误，回滚事务
    connection.rollback()
    print(f"Error: {e}")

finally:
    # 关闭连接
    connection.close()
