'''
request, session, redirect, url_for
from forms import SignupForm, LoginForm

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if "email" in session:
  	return redirect(url_for("home"))
  
  form = SignupForm()
  
  if request.method == "POST":
  	if form.validate() == False:
  	  return render_template("signup.html", form=form)
  	else:
  	  new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
  	  db.session.add(new_user)
  	  db.session.commit()
  		
  	  session["email"] = new_user.email
  	  return redirect(url_for("home"))

  elif request.method == "GET":
  	return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if "email" in session:
  	return redirect(url_for("home"))
  
  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data 
      password = form.password.data 

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session["email"] = form.email.data 
        return redirect(url_for("home"))
      else:
        return redirect(url_for("login"))

  elif request.method == "GET":
  	return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  session.pop("email", None)
  return redirect(url_for("index"))

@app.route("/home", methods=["GET", "POST"])
def home():
  if "email" not in session:
  	return redirect(url_for("login"))

  return render_template("home.html")
  '''