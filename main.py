import sqlite3
import pytest
import allure

@pytest.fixture(scope='session')
def start_db():
    conn = sqlite3.connect('dogs.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Dogs(
    id INTEGER PRIMARY KEY,
    name TEXT,
    image BLOB,
    breed TEXT,
    subbreed TEXT     
    )""")
    yield conn

    conn.close()

def test_dog_insert(start_db):
    with allure.step("INSERT-запрос к таблице Dogs"):
        cursor = start_db.cursor()
        cursor.execute("INSERT INTO Dogs (name, breed) VALUES (?, ?)", ("Haggi", "Chihuahua"))
        start_db.commit()
        cursor.execute("SELECT * FROM Dogs WHERE name = 'Haggi'")
        dog = cursor.fetchone()
        assert dog is not None


def test_dog_select(start_db):
    with allure.step("SELECT-запрос к таблице Dogs"):
        cursor = start_db.cursor()
        cursor.execute("SELECT * FROM Dogs")
        dogs = cursor.fetchall()
        assert len(dogs) == 1


def test_dog_update(start_db):
    with allure.step("UPDATE-запрос к таблице Dogs"):
        cursor = start_db.cursor()
        cursor.execute("UPDATE Dogs SET name = ? WHERE breed = ?", ("Waggi", "Chihuahua"))
        start_db.commit()
        cursor.execute("SELECT * FROM Dogs WHERE name = 'Waggi'")
        dog = cursor.fetchone()
        assert dog is not None

def test_dog_delete(start_db):
    with allure.step("DELETE-запрос к таблице Dogs"):
        cursor = start_db.cursor()
        cursor.execute("DELETE FROM Dogs WHERE name = 'Waggi'")
        start_db.commit()
        cursor.execute("SELECT * FROM Dogs WHERE name = 'Waggi'")
        dog = cursor.fetchone()
        assert dog is None



if __name__ == '__main__':
    pytest.main(args=["-s", __file__])