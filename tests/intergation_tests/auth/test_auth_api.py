import pytest


@pytest.mark.parametrize("email, password",[
                             ("testmail@mail.ru", "test_pass")
])
async def test_auth(email, password, ac):
    if "access_token" in ac.cookies:
        await ac.post("/auth/logout")

    response_reg = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    assert response_reg.status_code == 200

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response_login.status_code == 200
    assert "access_token" in ac.cookies

    response_me = await ac.get(
        "/auth/me"
    )

    if response_me.status_code == 200:
        res = response_me.json()
        assert "email" in res
        assert res["email"] == email

    await ac.post(
        "auth/logout"
    )

    response_me = await ac.get(
        "/auth/me"
    )
    assert response_me.status_code == 401




