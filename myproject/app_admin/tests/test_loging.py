# app_home/Auto/loging.py
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
        # Đợi để đảm bảo trang đã tải xong
        time.sleep(2)

    def test_login(self):
        print("Bắt đầu test_login")
        driver = self.driver

        # Nhập username và password
        inputUsername = driver.find_element(By.NAME, value="username")
        inputUsername.send_keys("admin")
        time.sleep(2)

        inputPassword = driver.find_element(By.NAME, value="password")
        inputPassword.send_keys("1234")
        time.sleep(2)

        # Submit form
        inputPassword.send_keys(Keys.RETURN)
        time.sleep(5)

        # Kiểm tra kết quả
        # TH1: Username đúng, password sai -> Không thể đăng nhập
        # TH2: Username sai, password đúng -> Không thể đăng nhập
        # TH3: Username và password đúng -> Đăng nhập thành công
        # TH4: Không nhập gì -> Không thể đăng nhập
        # (Bạn có thể thêm các assert để kiểm tra)

    def test_unit_user_should_able_to_add_item(self):
        print("Bắt đầu test_unit_user_should_able_to_add_item")
        driver = self.driver

        # Nhập username và password
        inputUsername = driver.find_element(By.NAME, value="username")
        inputUsername.send_keys("HoangLe")
        time.sleep(2)

        inputPassword = driver.find_element(By.NAME, value="password")
        inputPassword.send_keys("1234")
        time.sleep(2)

        # Submit form
        inputPassword.send_keys(Keys.RETURN)
        time.sleep(5)

        # Kiểm tra tiêu đề trang sau khi đăng nhập
        actualTitle = driver.title
        print(f"Tiêu đề trang: {actualTitle}")
        self.assertEqual(actualTitle, "Site administration | Django site admin", "Đăng nhập thất bại")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()