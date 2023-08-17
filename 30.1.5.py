import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def stat_num_pets():
    """Количество питомцев из блока статистики """

    # Явное ожидание
    pets_stat = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]')))
    pets = pets_stat.text.splitlines()

    return int(pets[1][10:])


def test_have_any_pets():
    """Проверка наличия питомцев"""

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    assert stat_num_pets() > 0, "Нет питомцев"


def test_have_all_pets():
    """Проверка соответствия количества питомцев в статистике и на странице"""

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Получаем количество питомцев во вкладке мои питомцы
    pet = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr')
    quantity_pets = len(pet)

    assert quantity_pets == stat_num_pets(), "Не все питомцы присутствуют на странице"


def test_pets_foto():
    """Проверка, что хотя бы у половины питомцев есть фото"""

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Явное ожидание
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))

    # Получаем количество фотографий питомцев во вкладке мои питомцы
    pets_photos = []
    pets_without_photos = 0
    for pets_foto in pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img'):
        pets_photos.append(pets_foto.get_attribute("src"))
        pets_without_photos = pets_photos.count('')

    assert stat_num_pets()/2 >= pets_without_photos, "Больше чем у половины питомцев нет фото"


def test_availability_of_pet_data():
    """Проверка, что у всех питомцев есть имя, возраст и порода"""

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Неявное ожидание
    pytest.driver.implicitly_wait(5)

    pets_names = []
    pets_breeds = []
    pets_ages = []
    for _ in pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'):
        pets_names.append(_.get_attribute("textContent"))
    for _ in pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]'):
        pets_breeds.append(_.get_attribute("textContent"))
    for _ in pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]'):
        pets_ages.append(_.get_attribute("textContent"))

    for _ in pets_names:
        assert _ != '', 'Питомец не имеет имени'
    for _ in pets_breeds:
        assert _ != '', 'Питомец не имеет породы'
    for _ in pets_ages:
        assert _ != '', 'Питомец не имеет возраста'


def test_identical_pets_names():
    """Проверка, что у всех питомцев разные имена """

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Явное ожидание
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))

    # Берем данные из колонки Имя
    pets_names = []
    for _ in pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'):
        pets_names.append(_.get_attribute("textContent"))

    # Проверка, есть ли у питомцев одинаковые имена
    assert len(pets_names) == len(set(pets_names)), 'У питомцев одинаковые имена'


def test_identical_pets():
    """Проверка наличия одинаковых питомцев"""

    # переходим во вкладку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, "//a[@href='/my_pets']").click()

    # Явное ожидание
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))

    # Берем данные из тела таблицы
    pets_data = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody')

    # Берем построчно текст из колонок и обрезаем лишнее
    pets_list = []
    for row in pets_data.find_elements(By.XPATH, ".//tr"):
        pets_list.append(row.text[:-2])

    assert len(pets_list) == len(set(pets_list)), 'Присутствуют питомцы с повторяющимися именами'