from config import Config
from extensions import db, login_manager, bcrypt
from database.models import User
from plotter import load_data, get_categories, plot_category_multi_location
from database.user_queries import create_user, get_user_by_username, check_user_password

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        if not get_user_by_username("admin"):
            hashed_password = bcrypt.generate_password_hash("password123"
                                                            ).decode('utf-8')
            new_user = User(username="admin", password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

    return app


app = create_app()

CSV_PATH = "data/data.csv"
PLOT_PATH = "static/diagrams/plot.png"

df = load_data(CSV_PATH)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Hasła muszą być identyczne!', 'incorrect')
            return redirect(url_for('register'))

        if get_user_by_username(username):
            flash('Ta nazwa uzytkownika jest już zajęta', 'incorrect')
            return redirect(url_for('register'))
        else:
            create_user(username, password)
            flash('Zarejestrowano pomyślnie', 'correct')
            return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_username(username)

        if check_user_password(user, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Niepoprawny login lub hasło')

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    locations = sorted(df["Nazwa"].unique())
    categories = get_categories(df)

    selected_locations = []
    selected_category = None

    if request.method == "POST":
        selected_locations = request.form.getlist("locations")
        selected_category = request.form["category"]

        if not (1 <= len(selected_locations) <= 3):
            flash("Wybierz od 1 do 3 lokacji", "incorrect")
        else:
            plot_category_multi_location(
                df,
                selected_locations,
                selected_category,
                PLOT_PATH
            )

    return render_template(
        "dashboard.html",
        locations=locations,
        categories=categories,
        selected_locations=selected_locations,
        selected_category=selected_category
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
