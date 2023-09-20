from app import create_app, init_celery, celery, db

app = create_app()
init_celery(celery, app)


# from app.models import User, Post

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Post': Post}
