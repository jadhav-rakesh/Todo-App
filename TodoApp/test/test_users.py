from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status 

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'rakeshtest'
    assert response.json()['email'] == 'rakesh@gmail.com'
    assert response.json()['first_name'] == 'Rakesh'
    assert response.json()['last_name'] == 'J'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(91)-12345-6789'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={'password': 'rakeshjadhav',
                                                  'new_password': 'newpassword'})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={'password': 'wrong_password',
                                                  'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}

def test_change_phone_number_success(test_user):
    respnose = client.put("/user/phonenumber/47474747474747")
    assert respnose.status_code == status.HTTP_204_NO_CONTENT