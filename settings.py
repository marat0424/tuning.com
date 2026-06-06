import os

# Путь к папке проекта
PATH = os.path.dirname(__file__) + os.sep

# Путь к базе данных
DB_NAME = 'blog.db'
PATH_DB = PATH + DB_NAME

# Секретный ключ приложения
SECRET_KEY = 'VeryStrongKey'