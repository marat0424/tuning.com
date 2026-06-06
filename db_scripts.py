import sqlite3
from settings import *

conn = None
cursor = None


# Открыть соединение с базой данных
def open_db():
    global conn, cursor
    conn = sqlite3.connect(PATH_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')


# Закрыть соединение с базой данных
def close_db():
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# Выполнить SQL-запрос
def execute(query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    conn.commit()


# Принудительное пересоздание таблиц (удаляем старые и создаем новые)
def create_tables():
    open_db()

    # Удаляем старые таблицы, чтобы сбросить структуру
    execute('DROP TABLE IF EXISTS posts')
    execute('DROP TABLE IF EXISTS users')
    execute('DROP TABLE IF EXISTS categories')

    # Создаем таблицу категорий тюнинга
    execute('''
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
    ''')

    # Создаем таблицу профиля Scooter Boom
    execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image TEXT,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            description_short TEXT,
            description TEXT
        )
    ''')

    # Создаем таблицу товаров со ВСЕМИ необходимыми колонками
    execute('''
        CREATE TABLE posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            price TEXT NOT NULL,
            item_image TEXT,
            datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
    ''')

    close_db()


# Получить данные о мастерской
def get_user():
    open_db()
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchone()
    close_db()
    return user


# Получить все категории
def get_categories():
    open_db()
    cursor.execute('SELECT * FROM categories ORDER BY category_id')
    categories = cursor.fetchall()
    close_db()
    return categories


# Добавить категорию тюнинга
def add_category(category_name):
    open_db()
    execute('INSERT INTO categories (category_name) VALUES (?)', [category_name])
    close_db()


# Получить товары конкретной категории через явный JOIN
def get_posts(category_id):
    open_db()
    cursor.execute('''
        SELECT posts.*, categories.category_name 
        FROM posts
        JOIN categories ON posts.category_id = categories.category_id
        WHERE posts.category_id = ?
        ORDER BY posts.post_id DESC
    ''', [category_id])
    posts = cursor.fetchall()
    close_db()
    return posts


# Добавить товар в каталог
def add_product(category_id, title, text, price, item_image):
    open_db()
    execute('''
        INSERT INTO posts (category_id, title, text, price, item_image) 
        VALUES (?, ?, ?, ?, ?)
    ''', [category_id, title, text, price, item_image])
    close_db()


# Настройка информации о Scooter Boom Customs
def setup_scooter_shop_info():
    open_db()
    execute('''
        INSERT INTO users (name, image, login, password, description_short, description)
        VALUES (
            'SCOOTER BOOM CUSTOMS', 
            'logo.png', 
            'admin', 
            'scooter2026', 
            'Топовый тюнинг скутеров, запчасти Stage6, Malossi, Athena в наличии.',
            'Добро пожаловать в Scooter Boom! Мы превращаем стоковые мопеды в настоящие гоночные снаряды. Занимаемся настройкой трансмиссии, увеличением кубатуры 2Т моторов (Sport/Racing) и кастомизацией внешнего вида. Твой скутер должен валить!'
        )
    ''')
    close_db()


# Вывести товары в консоль для проверки работы базы
def show_posts(category_id):
    posts = get_posts(category_id)
    for post in posts:
        print('Товар:', post['title'])
        print('Цена:', post['price'])
        print('Описание:', post['text'])
        print('Категория:', post['category_name'])
        print('-' * 50)


# Главный блок запуска
if __name__ == "__main__":
    # Сначала полностью пересоздаем чистые таблицы с правильными колонками
    create_tables()

    # 1. Заполняем новые категории тюнинга
    add_category('Двигатель и ЦПГ')
    add_category('Трансмиссия и Вариаторы')
    add_category('Выхлопные системы')
    add_category('Стайлинг и Ходовая')

    # 2. Наполняем витрину деталями (категория, Название, Описание, Цена, Картинка)
    # ЦПГ (Категория 1)
    add_product(1, 'ЦПГ Malossi Sport 70cc (Minarelli)',
                'Чугунный цилиндр, отличный ресурс и дикий подрыв с низов! Подходит на Yamaha Jog/Aerox.', '5 900 грн.',
                'malossi_sport.jpg')
    add_product(1, 'ЦПГ Athena Racing 70cc (Minarelli)',
                'Алюминий/никасиль для любителей выжать максимум оборотов. Требует карбюратор от 17.5мм.', '8 200 грн.',
                'athena_racing.jpg')

    # Трансмиссия (Категория 2)
    add_product(2, 'Вариатор Stage6 R/T Oversize',
                'Увеличенный диаметр шкивов обеспечивает ровную полку момента и убирает провалы при разгоне.',
                '4 500 грн.', 'stage6_variator.jpg')
    add_product(2, 'Пружина торкдрайвера Malossi Red',
                'Жесткая пружина для злых конфигов. Идеально для быстрого старта на заднее колесо.', '650 грн.',
                'malossi_spring.jpg')

    # Выхлоп (Категория 3)
    add_product(3, 'Выхлопная труба Yasuni R Black',
                'Легендарный саксофон для класса Sport/Mid-Race. Раскрывает весь потенциал 70cc поршневой.',
                '9 800 грн.', 'yasuni_r.jpg')
    add_product(3, 'Выхлопная труба LeoVince HandMade TT',
                'Бюджетный резонансный выхлоп для начального 50cc/70cc тюнинга.', '4 200 грн.', 'leovince_tt.jpg')

    # Стайлинг (Категория 4)
    add_product(4, 'Вынос руля Str8 (Yamaha Aerox)',
                'Качественный алюминиевый вынос под открытый руль. Незаменим для стант-конфига.', '1 200 грн.',
                'str8_stem.jpg')
    add_product(4, 'Руль Str8 Кроссовый (Хром)',
                'Широкий открытый руль для идеального контроля скутера в заносе или на заднем.', '1 500 грн.',
                'str8_bar.jpg')

    # 3. Добавляем профиль магазина
    setup_scooter_shop_info()

    print("=" * 60)
    print(" БАЗА ДАННЫХ SCOOTER BOOM ПОЛНОСТЬЮ ОБНОВЛЕНА И ПЕРЕСОЗДАНА! ")
    print("=" * 60)

    print('\nПроверка базы данных: Категория "Двигатель и ЦПГ"')
    print('-' * 50)
    show_posts(1)