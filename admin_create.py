#!flask/bin/python3
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys
from flask.ext.bcrypt import Bcrypt

from noozjunkie_webapp import app, db
from noozjunkie_webapp.models import User

bcrypt = Bcrypt(app)

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print('A user already exists! Create another? (y/n):')
            create = input()
            if create == 'n':
                return

        print('Enter username: ')
        username = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(username=username, password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')



if __name__ == '__main__':
    sys.exit(main())
