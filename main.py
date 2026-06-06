from flask import Flask, redirect, url_for, session, request, render_template
from settings import *
from db_scripts import *

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = get_user()
    categories = get_categories()

    # 1. Смотрим, какую категорию выбрал пользователь (через GET-запрос)
    # Если клика не было, по умолчанию берем первую категорию (id = 1)
    current_category = request.args.get('category_id', type=int)
    if not current_category and categories:
        current_category = categories[0]['category_id']

    # 2. Вытягиваем товары только для этой категории
    posts = get_posts(current_category) if current_category else []

    # 3. Передаем ВСЁ это в шаблон
    return render_template(
        'index.html',
        user=user,
        categories=categories,
        posts=posts,
        current_cat=current_category
    )


@app.route('/about')
def about():
    user = get_user()
    return render_template('about.html', user=user)


app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)