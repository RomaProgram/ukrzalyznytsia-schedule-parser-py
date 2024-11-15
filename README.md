![ukrzalyznytsia parser](https://github.com/user-attachments/assets/eefcb792-057b-4f88-ab64-874330cbcc9c)


**Парсер Розкладу УкрЗалізниці** — це Python-скрипт, який використовує Playwright для автоматизованого збору інформації про розклад відправлень та прибуттів поїздів з офіційного сайту [Укрзалізниці](https://booking.uz.gov.ua/schedule). Скрипт дозволяє швидко отримувати актуальні дані про розклад у зручному форматі.

## Основні можливості

- **Автоматизований збір даних:** Використання Playwright для навігації по сайту та збору необхідної інформації.
- **Підтримка різних станцій:** Можливість вибору будь-якої залізничної станції для отримання розкладу.
- **Обробка затримок:** Виявлення та відображення інформації про затримки поїздів.
- **Структурований вивід:** Вивід даних у зручному форматі для подальшої обробки або аналізу.

## Передумови

Перед використанням скрипта необхідно встановити деякі залежності та налаштувати середовище.

### Вимоги

- **Python 3.7+**
- **Playwright**

## Встановлення

1. **Клонування репозиторію:**

    ```bash
    git clone https://github.com/RomaProgram/ukrzalyznytsia-schedule-parser-py.git
    cd ukrzalyznytsia-schedule-parser-py
    ```

2. **Створення та активація віртуального середовища (рекомендується):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. **Встановлення залежностей:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Встановлення та налаштування Playwright:**

    ```bash
    playwright install
    ```

## Використання

1. **Запуск скрипта**

    ```bash
    python uz_parser.py
    ```

2. **Введення вокзалу**

    При запуску скрипта вам буде запропоновано ввести назву станції. Наприклад:

    ```
    Enter train station: Київ-Пас
    ```

    *Нажаль не всі вокзали працюють у скрипті, так як код парсить інформацію з https://booking.uz.gov.ua/schedule*

3. **Результат**

    Після введення назви станції скрипт виведе інформацію про відправлення та прибуття поїздів у структурованому форматі:

    ```
    Departures from Київ-Пас:
    {'trainNumber': '123A', 'from': 'Київ-Пас', 'to': 'Львів', 'route': 'from Київ-Пас to Львів', 'scheduledTime': '12:30 (Delayed by 5 min)', 'platform': '3'}
    ...

    Arrivals at Київ-Пас:
    {'trainNumber': '456B', 'from': 'Львів', 'to': 'Київ-Пас', 'route': 'from Львів to Київ-Пас', 'scheduledTime': '15:45', 'platform': '1'}
    ...
    ```

# Плани на майбутнє

- Додати дату та час замість просто часу
- Додати пряму підтримку скрипта як модуля, та викласти модуль на Pypi, щоб можна було легко використовувати наприклад у Чат-ботах
- Зробити скрипт ефективнішим
- Додати можливість щоб скрипт постійно дивився, чи є зміни у таблі, якщо є то скрипт відішле запрос, наприклад до Чат-Бота, щоб той написав комусь що Табло Змінено
- Якщо можливо додати підтримку малих вокзалів яких нема у офіційному таблі


## Наш телеграм канал [TrainVector](https://t.me/trainvector)
### Якщо в вас є додаткові питання, ви можете їх задати мені: [@Romikan4ik](https://t.me/Romikan4ik)
