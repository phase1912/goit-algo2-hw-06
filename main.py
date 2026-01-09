# This is a sample Python script.
from bloom_filter import BloomFilter
import json
import time

from hyper_log_log import HyperLogLog


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
    log_entries = deserialize_log_file('lms-stage-access.log')

    print("\n=== Порівняння методів підрахунку унікальних IP ===\n")

    # Точний підрахунок (set)
    start_time = time.time()
    unique_ips_count_by_set = get_unique_ips_count_using_set(log_entries)
    set_time = time.time() - start_time

    # Наближений підрахунок (HyperLogLog)
    start_time = time.time()
    unique_ips_count_by_hll = get_unique_ips_count_using_hyper_log_log(log_entries)
    hll_time = time.time() - start_time

    # Виведення результатів у вигляді таблиці
    print("Результати порівняння:")
    print(f"{'':25} {'Точний підрахунок':>20} {'HyperLogLog':>20}")
    print(f"{'Унікальні елементи':25} {unique_ips_count_by_set:>20.1f} {unique_ips_count_by_hll:>20.1f}")
    print(f"{'Час виконання (сек.)':25} {set_time:>20.2f} {hll_time:>20.2f}")

    # Розрахунок похибки
    if unique_ips_count_by_set > 0:
        error_percent = abs(unique_ips_count_by_set - unique_ips_count_by_hll) / unique_ips_count_by_set * 100
        print(f"{'Похибка (%)':25} {'-':>20} {error_percent:>20.2f}")

    print()


def deserialize_log_file(filename):
    log_entries = []
    unique_ips = set()
    ip_counts = {}
    errors = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        log_entries.append(log_entry)
                        ip = log_entry.get('remote_addr')

                        if ip:
                            unique_ips.add(ip)
                            ip_counts[ip] = ip_counts.get(ip, 0) + 1
                    except json.JSONDecodeError as e:
                        print(f"Помилка парсингу JSON в рядку {line_number}: {e}")
                        errors += 1
                        continue

        print("\n" + "=" * 70)
        print("LOG FILE ANALYSIS RESULTS")
        print("=" * 70)
        print(f"Total log entries parsed: {len(log_entries)}")
        print(f"Parse errors: {errors}")
        print(f"Unique IP addresses found: {len(unique_ips)}")
        print("=" * 70)
        print("\nALL UNIQUE IP ADDRESSES (sorted):")
        print("=" * 70)

        for i, ip in enumerate(sorted(unique_ips), 1):
            count = ip_counts.get(ip, 0)
            print(f"{i:3}. {ip:20} (appears {count} times)")

        print("=" * 70)
        print(f"\nSUMMARY: Found {len(unique_ips)} unique IP addresses")
        print("=" * 70)
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено!")
        return []
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return []

    return log_entries

def get_unique_ips_count_using_set(log_entries) -> int:
    unique_ips = set()

    for entry in log_entries:
        ip = entry.get('remote_addr')
        if ip:
            unique_ips.add(ip)

    return len(unique_ips)

def get_unique_ips_count_using_hyper_log_log(log_entries) -> float:
    hll = HyperLogLog(p=14)

    for entry in log_entries:
        ip = entry.get('remote_addr')
        if ip: hll.add(ip)

    return hll.count()

def check_password_uniqueness(bloom: BloomFilter, new_passwords_to_check: list):
    results = {}
    for password in new_passwords_to_check:
        results[password] = "вже використаний" if bloom.contains(password) else "унікальний"

    return results

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("=== Завдання 1: Перевірка унікальності паролів ===")
    task1()

    print("\n=== Завдання 2: Десеріалізація логів ===")
    task2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
