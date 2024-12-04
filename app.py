from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Создание класса пользователя
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Хранение пользователей (в реальном приложении используйте базу данных)
users = {'admin': generate_password_hash('admin1')}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Главная страница
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Страница продукта
@app.route('/product/<int:product_id>')
@login_required
def product(product_id):
    return render_template('product.html', product_id=product_id)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.')
    
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
