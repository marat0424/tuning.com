from flask import Flask, redirect, url_for, session, request, render_template
from settings import *
from db_scripts import *

app = Flask(__name__)


# Главная страница (Витрина товаров)
@app.route('/')
@app.route('/index')
def index():
    user = get_user()
    categories = get_categories()

    # Получаем ID выбранной категории. Если не выбрана — ставим первую по умолчанию
    current_category = request.args.get('category_id', type=int)
    if not current_category and categories:
        current_category = categories[0]['category_id']

    posts = get_posts(current_category) if current_category else []

    return render_template(
        'index.html',
        user=user,
        categories=categories,
        posts=posts,
        current_cat=current_category
    )


# Страница подробного просмотра одной детали
@app.route('/product/<int:post_id>')
def product_page(post_id):
    user = get_user()
    post = get_single_post(post_id)  # Загружаем инфо об одной детали

    if not post:
        return "Деталь не найдена в каталоге!", 404

    return render_template('product.html', user=user, post=post)


# Страница о мастерской
@app.route('/about')
def about():
    user = get_user()
    return render_template('about.html', user=user)


app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)