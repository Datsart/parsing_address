import mysql.connector


# создаем БД
def create_db():
    dataBase = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="12345",
        database="database"

    )

    mycursor = dataBase.cursor()

    mycursor.execute('''
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


create_db()
