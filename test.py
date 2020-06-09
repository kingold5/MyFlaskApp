from datetime import datetime, timedelta
import unittest
from myflask import db, app
from myflask.models import Users, Articles


# TODO
# tweak test on mysql

class UserModelCase(unittest.TestCase):
    """Test functions in myflaskapp

    Parameters
    ----------
    unittest : [type]
        [description]
    """
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = Users(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
