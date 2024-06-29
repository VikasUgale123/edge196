import pytest
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def load_test_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Paths to the CSV files
valid_data_file = os.path.join(os.path.dirname(__file__), "C:\\Users\\vikas\\PycharmProjects\\pythonProjects\\edge196\\test_data\\valid_data.csv")
invalid_data_file = os.path.join(os.path.dirname(__file__), "C:\\Users\\vikas\\PycharmProjects\\pythonProjects\edge196\\test_data\\invalid_data.csv")

# Test for valid data
@pytest.mark.parametrize("data", load_test_data(valid_data_file))
def test_valid_form_submission(driver, data):
    driver.get("https://www.edge196.com/contact-us")

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'name')))

    driver.find_element(By.NAME, 'name').send_keys(data['name'])
    driver.find_element(By.NAME, 'email').send_keys(data['email'])
    driver.find_element(By.NAME, 'message').send_keys(data['message'])
    driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()

    confirmation_message = driver.find_element(By.XPATH, '//*[contains(text(),"Thank you for contacting us!")]').text
    assert "Thank you for contacting us!" in confirmation_message

# Test for invalid data
@pytest.mark.parametrize("data", load_test_data(invalid_data_file))
def test_invalid_form_submission(driver, data):
    driver.get("https://www.edge196.com/contact-us")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'name')))

    driver.find_element(By.NAME, 'name').send_keys(data['name'])
    driver.find_element(By.NAME, 'email').send_keys(data['email'])
    driver.find_element(By.NAME, 'message').send_keys(data['message'])
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    error_message_elements = driver.find_elements(By.XPATH, '//*[contains(@class, "error")]')
    assert any("Please fill out this field" in elem.text or "Please enter a valid email address" in elem.text for elem in error_message_elements)


