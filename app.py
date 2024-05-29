import pandas as pd
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from create_db import create_db
import json

# создается БД
create_db()
engine = create_engine("mysql+pymysql://user:12345@localhost/database")

# модель таблицы
BASE = declarative_base()


class PassportValiPdAddress(BASE):
    __tablename__ = 'passport_valid_address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    index_ = Column('index_', Integer)
    b_crm_contact__ID = Column(Integer)
    town = Column(String(100), nullable=True)  # Поле может быть пустым
    street = Column(String(100), nullable=True)  # Поле может быть пустым
    number_house = Column(String(100), nullable=True)  # Поле может быть пустым
    apartment = Column(String(100), nullable=True)  # Поле может быть пустым


BASE.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# датафрейм
df = pd.read_csv('./парсинг регистрации.csv', on_bad_lines='skip', sep='‰', engine='python')
error_dict = {}
for index in range(len(df)):
    response = requests.post(
        'http://83.239.206.206:5090/api/gpt_request/',
        data={
            'api_key': 'test',
            'text': f'распознай адрес - {df.iloc[index]["b_crm_contact__registration_address"]}. И добавь в поля    town    street  number_house   apartment. Овет - словарь пайтон'
        }
    )
    try:
        print(response.json()['result'])
        result = response.json()['result']
        # print(json.loads(result)['town'])
        string = PassportValiPdAddress(
            index_=df.iloc[index]['index'],
            b_crm_contact__ID=df.iloc[index]["b_crm_contact__ID"],
            town=json.loads(result)['town'],
            street=json.loads(result)['street'],
            number_house=json.loads(result)['number_house'],
            apartment=json.loads(result)['apartment'],
        )
        session.add(string)
        session.commit()
    except BaseException as e:
        error_dict[index] = e
        print(error_dict)
