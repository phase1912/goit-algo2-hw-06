# This is a sample Python script.
from bloom_filter import BloomFilter

def task1():
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")

def task2():
    pass

def check_password_uniqueness(bloom: BloomFilter, new_passwords_to_check: list):
    results = {}
    for password in new_passwords_to_check:
        results[password] = "вже використаний" if bloom.contains(password) else "унікальний"

    return results

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    task1()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
