import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

def test_authenticate_user_success(setup_database, connection):
    """Başarılı kullanıcı doğrulamasını test eder."""
    add_user('authuser', 'auth@example.com', 'authpassword')
    assert authenticate_user('authuser', 'authpassword')

def test_add_existing_user(setup_database, connection):
    """Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test eder."""
    add_user('existinguser', 'existing@example.com', 'password123')
    assert not add_user('existinguser', 'another@example.com', 'newpassword')

def test_authenticate_non_existent_user(setup_database, connection):
    """Var olmayan bir kullanıcıyla doğrulama yapmayı test eder."""
    assert not authenticate_user('nonexistent', 'anypassword')

def test_authenticate_wrong_password(setup_database, connection):
    """Yanlış şifreyle doğrulama yapmayı test eder."""
    add_user('wrongpassuser', 'wrongpass@example.com', 'correctpassword')
    assert not authenticate_user('wrongpassuser', 'wrongpassword')

def test_display_users(setup_database, connection, capfd):
    """Kullanıcı listesinin doğru şekilde görüntülenmesini test eder."""
    add_user('displayuser1', 'display1@example.com', 'pass1')
    add_user('displayuser2', 'display2@example.com', 'pass2')
    display_users()
    out, err = capfd.readouterr()
    assert "Kullanıcı adı: displayuser1, E-posta: display1@example.com" in out
    assert "Kullanıcı adı: displayuser2, E-posta: display2@example.com" in out

# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
Başarılı kullanıcı doğrulamasını test etme.
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""
