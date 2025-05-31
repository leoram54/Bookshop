from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class AuthTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login(self):
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        self.browser.find_element(By.NAME, 'password').send_keys('testpass123')
        self.browser.find_element(By.TAG_NAME, 'form').submit()
        time.sleep(1)

        # Проверим, что мы на странице со списком книг (book_list)
        self.assertIn("Книги", self.browser.page_source)
from .models import Book, CartItem, Cart

class OrderTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='securepass')
        self.book = Book.objects.create(title='1984', author='Orwell', price=100)

    def login(self):
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('buyer')
        self.browser.find_element(By.NAME, 'password').send_keys('securepass')
        self.browser.find_element(By.TAG_NAME, 'form').submit()
        time.sleep(1)

    def test_order_checkout(self):
        self.login()
        # Добавление книги в корзину
        self.browser.get(f'{self.live_server_url}/add_to_cart/{self.book.id}/')
        time.sleep(1)
        self.browser.get(f'{self.live_server_url}/cart/')
        self.assertIn('1984', self.browser.page_source)

        # Оформление заказа
        self.browser.get(f'{self.live_server_url}/checkout/')
        time.sleep(1)
        self.browser.get(f'{self.live_server_url}/order_history/')
        self.assertIn('1984', self.browser.page_source)
class ProfileTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='oldname', email='old@example.com', password='oldpass')

    def login(self):
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element(By.NAME, 'username').send_keys('oldname')
        self.browser.find_element(By.NAME, 'password').send_keys('oldpass')
        self.browser.find_element(By.TAG_NAME, 'form').submit()
        time.sleep(1)

    def test_change_profile(self):
        self.login()
        self.browser.get(f'{self.live_server_url}/profile/')
        self.browser.find_element(By.NAME, 'username').clear()
        self.browser.find_element(By.NAME, 'username').send_keys('newname')
        self.browser.find_element(By.NAME, 'email').clear()
        self.browser.find_element(By.NAME, 'email').send_keys('new@example.com')
        self.browser.find_element(By.TAG_NAME, 'form').submit()
        time.sleep(1)
        self.assertIn('Профиль успешно обновлен', self.browser.page_source)
