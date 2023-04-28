from flask import (Blueprint,render_template,
                   redirect,
                   url_for,
                   request,
                   flash, abort)

import html

from WebApp.auth.forms import SignupForm, LoginForm, AccountUpdateForm

from WebApp import app, db, bcrypt

from WebApp.models import User

from flask_login import login_user, current_user, logout_user, login_required

import secrets, os

from PIL import Image

from WebApp.home import home


auth = Blueprint('auth', __name__)

def image_save(image, where, size):
    random_filename = secrets.token_hex(12)
    file_name, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension

    image_path = os.path.join(app.root_path, 'static/images', where, image_filename)

    img = Image.open(image)

    img.thumbnail(size)

    img.save(image_path)

    return image_filename



@auth.route("/signup/", methods=["GET", "POST"])
def signup():

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = html.escape(form.username.data)
        email = html.escape(form.email.data)
        password = html.escape(form.password.data)
        password2 = html.escape(form.password2.data)

        encrypted_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Ο λογαριασμός για τον χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία", "success")

        return redirect(url_for('auth.login'))
    

    return render_template("auth/signup.html", form=form)




@auth.route("/auth", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home.root"))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = html.escape(form.email.data)
        password = html.escape(form.password.data)

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη με email: {email} στη σελίδα μας έγινε με επιτυχία.", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for("auth.login"))
        else:
            flash("Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλούμε δοκιμάστε ξανά με τα σωστά email/password.", "warning")

    return render_template("auth/login.html", form=form)




@auth.route("/logout")
def logout():
    logout_user()
    flash("Έγινε αποσύνδεση του χρήστη.", "success")
    return redirect(url_for("auth.login"))



@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)

    if request.method == 'POST' and form.validate_on_submit():

        current_user.username = html.escape(form.username.data)
        current_user.email = html.escape(form.email.data)

        # image_save(image, where, size)

        if form.profile_image.data:

            try:
                image_file = image_save(form.profile_image.data, 'profiles_images', (150, 150))
            except:
                abort(415)

            current_user.profile_image = image_file

        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b>{current_user.username}</b> ενημερώθηκε με επιτυχία", "success")

        return redirect(url_for('auth.login'))


    return render_template("auth/account_update.html", form=form)