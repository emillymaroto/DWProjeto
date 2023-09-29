pipfrom flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask( __name__ )

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comunidade.db"
app.config['SECRET_KEY'] = "2dd1e09fe4e5058af539002a4da59b84"
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"

database = SQLAlchemy( app )

bcrypt = Bcrypt( app )
login_manager = LoginManager( app )

# usuário não logado é direcionado para a rota principal, no caso "homepage"
login_manager.login_view = "homepage"

from app_imediagram import routes