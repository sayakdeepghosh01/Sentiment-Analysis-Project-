
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x08\x81\xd8\x19#2&\x07\x16\x07\x95\x0bb~\xb3\x8b\xf2\x020\xe5'
app.debug = True
from app import routes
