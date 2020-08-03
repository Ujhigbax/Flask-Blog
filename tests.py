from router import app, db
import unittest
from flask_testing import TestCase
from models import User, BlogPost

class BaseTestCase(TestCase):
    
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app
    
    def setUp(self):
        db.create_all()
        db.session.add(BlogPost('Test post','This is a test. Only a test.',1))
        db.session.add(User('admin','admin@email.com','password'))
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class FlaskTestCase(BaseTestCase):

    #Ensure that the requested file was served by the app.
    def test_index(self):
        response=self.client.get('/login',content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #Ensure that the file served has the correct text.
    def test_login_page_loads(self):
        response=self.client.get('/login',content_type='html/text')
        self.assertTrue(b'Please Login' in response.data)

    #Ensure login behaves correctly with the correct credentials.
    def test_correct_login(self):
        response=self.client.post('/login',data=dict(username='admin',password='admin'),follow_redirects=True)
        self.assertIn(b'You were just logged in!',response.data)
    
    #Ensure login behaves correctly with the incorrect credentials.
    def test_incorrect_login(self):
        response=self.client.post('/login',data=dict(username='wrong',password='admin'),follow_redirects=True)
        self.assertIn(b'Invalid credentials. Please try again.',response.data)

    #Ensure the logout behaves correctly.
    def test_logout(self):
        self.client.post('/login',data=dict(username='admin',password='admin'),follow_redirects=True)
        response = self.client.get('/logout',follow_redirects=True)
        self.assertIn(b'You were just logged out',response.data)
    
    #Ensure that the main page requires login
    def test_main_route_requires_login(self):
        response=self.client.get('/', follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)

    #Ensure that the logout page required login
    def test_logout_route_requires_login(self):
        response=self.client.get('/logout',follow_redirects=True)
        self.assertTrue(b'Please log in to access this page.' in response.data)
    
    #Ensure that the post shows up on the main page
    def test_post_show_up(self):
        self.client.post('/login',data=dict(username='admin',password='password'),follow_redirects=True)
        response=self.client.get('/',follow_redirects=True)
        self.assertIn(b'This is a test. Only a test.',response.data)
    
    #Ensure use can register.
    def test_user_registration(self):
        self.client.post('/register',data=dict(username='username',email='username@email.com',password='password',confirm='password'),follow_redirects=True)
        response=self.client.post('/login',data=dict(username='username',password='password'),follow_redirects=True)
        self.assertIn(b'Welcome to Flask!',response.data)
    
if __name__ == '__main__':
    unittest.main()