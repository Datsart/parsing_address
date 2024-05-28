import pandas as pd
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from create_db import create_db
from geopy.geocoders import Nominatim
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
    region = Column(String(100), nullable=True)  # Поле может быть пустым
    area = Column(String(100), nullable=True)  # Поле может быть пустым
    town = Column(String(100), nullable=True)  # Поле может быть пустым
    settlement = Column(String(300), nullable=True)  # Поле может быть пустым
    street = Column(String(300), nullable=True)  # Поле может быть пустым
    number_house = Column(String(10), nullable=True)  # Поле может быть пустым
    number_housing = Column(String(10), nullable=True)  # Поле может быть пустым
    apartment = Column(String(10), nullable=True)  # Поле может быть пустым


BASE.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# датафрейм
df = pd.read_csv('./парсинг регистрации.csv', on_bad_lines='skip', sep='‰', engine='python')
geolocator = Nominatim(user_agent="myGeocoder")

for index in range(len(df)):
    try:
        response = requests.post(
            'http://83.239.206.206:5090/api/gpt_request/',
            data={
                'api_key': 'test',
                'text': f'распознай адрес - {df.iloc[index]["b_crm_contact__registration_address"]}. И добавь в поля region area  town  settlement  street  number_house number_housing  apartment. Овет - словарь пайтон'
            }
        )

        # Debugging output
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        # Check if the response contains valid JSON
        response_json = response.json()
        print(f"Response JSON: {response_json}")

        if 'result' in response_json:
            result_str = response_json['result']
            result = json.loads(result_str)  # Parse the string into a dictionary
            print(f"Parsed result: {result}")

            string = PassportValiPdAddress(
                index_=df.iloc[index]['index'],
                b_crm_contact__ID=df.iloc[index]["b_crm_contact__ID"],
                region=str(result.get('region', '')),
                area=str(result.get('area', '')),
                town=str(result.get('town', '')),
                settlement=str(result.get('settlement', '')),
                street=str(result.get('street', '')),
                number_house=str(result.get('number_house', '')),
                number_housing=str(result.get('number_housing', '')),
                apartment=str(result.get('apartment', '')),
            )
            session.add(string)
            session.commit()
        else:
            print("Error: 'result' not in response JSON")

    except ValueError as e:
        print(f"ValueError: {e}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
    except Exception as e:
        print(f"Exception: {e}")

