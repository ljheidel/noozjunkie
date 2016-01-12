from flask import g
from noozjunkie_webapp import app, db, lm, bcrypt
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.restless import APIManager, ProcessingException
from flask_jwt import JWT, jwt_required, current_identity, _jwt_required
from .models import Feed, Article, Keyword, ArticleKeyword, User
import flask.ext.restless



# @jwt.authentication_handler
def api_authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

# @jwt.user_handler
def api_identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
    
jwt = JWT(app, api_authenticate, api_identity)

#@login_required
#@jwt_required()
#def api_auth_func(**kw):
#    return True

def api_auth_func(**kw):
    if g.user.is_authenticated:
        return True
    elif _jwt_required(None):
        return True 
    else: 
        return False

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

feed_blueprint = manager.create_api(Feed, methods=['GET', 'POST', 'DELETE', 'PUT'], allow_patch_many=True, preprocessors=dict(GET_MANY=[api_auth_func], GET_SINGLE=[api_auth_func], POST=[api_auth_func]))
article_blueprint = manager.create_api(Article, methods=['GET', 'POST', 'DELETE'])
keyword_blueprint = manager.create_api(Keyword, methods=['GET', 'POST', 'DELETE'])
articlekeyword_blueprint = manager.create_api(ArticleKeyword, methods=['GET', 'POST', 'DELETE'])
