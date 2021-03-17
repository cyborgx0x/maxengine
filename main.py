from app import app, db
from app.models import Fiction, User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Fiction': Fiction, 'User':User}


