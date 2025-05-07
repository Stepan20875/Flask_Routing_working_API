from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Используем SQLite для простоты
app.config['SECRET_KEY'] = 'your_secret_key'  # Важно для безопасности сессий
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Словарь для хранения записей (заменится БД)
notes = {}

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')  # Хешируем пароль

        new_user = Users(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Перенаправляем на страницу логина после регистрации
        except:
            return "Ошибка при регистрации"  # Обработка ошибок (например, если имя пользователя или email уже существуют)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # TODO: Реализовать систему сессий для поддержания авторизации
            return redirect(url_for('notes_page'))  # Перенаправляем на страницу дневника после успешного входа
        else:
            return "Неверный логин или пароль"  # Сообщение об ошибке

    return render_template('login.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes_page():
    global notes # Делаем notes глобальной переменной

    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']
        notes[title] = {'subtitle': subtitle, 'text': text} # Сохраняем подзаголовок

    return render_template('notes.html', notes=notes) # Передаем notes в шаблон

if __name__ == '__main__':
    app.run(debug=True)