from src.services.auth import AuthService


def test_create_access_token():
    user = {"user_1": 1}
    jwt_token = AuthService().create_access_token(user)

    assert jwt_token
    assert isinstance(jwt_token, str)
