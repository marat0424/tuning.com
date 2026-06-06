import os

# Шлях до папки проєкту
PATH = os.path.dirname(__file__) + os.sep

# Шлях до бази даних
DB_NAME = 'blog.db'
PATH_DB = PATH + DB_NAME

# Секретний ключ
SECRET_KEY = 'VeryStrongKey'