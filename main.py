from app import app, db
from app.models import Fiction, User, Author

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Fiction': Fiction, 'User':User,  'Author': Author}

if __name__=="__main__":
    print("starting flask")
    app.run()