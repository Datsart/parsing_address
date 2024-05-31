import mysql.connector


# создаем БД
def create_db():
    try:
        # Устанавливаем соединение с MySQL сервером
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1Peaceful!!!***"
        )

        # Создаем курсор для выполнения SQL запросов
        cursor = connection.cursor()

        # Создаем базу данных, если она еще не существует
        cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")

        # Выбираем созданную базу данных
        cursor.execute("USE mydatabase")

        # Создаем таблицу, если она еще не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS passport_valid_address (
            id INT AUTO_INCREMENT PRIMARY KEY,
            index_ INT,
            b_crm_contact__ID INT,
            town VARCHAR(100) DEFAULT NULL,
            street VARCHAR(100) DEFAULT NULL,
            number_house VARCHAR(100) DEFAULT NULL,
            apartment VARCHAR(100) DEFAULT NULL
        )
        ''')

        print("База данных и таблица успешно созданы")

        # Закрываем курсор и соединение с базой данных
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")

# вызываем функцию для создания БД и таблицы
# create_db()
