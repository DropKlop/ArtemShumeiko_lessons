async def test_get_facilities(ac):
    facilities = await ac.get("/facilities")
    print(f"{facilities=}")

    assert facilities.status_code == 200


async def test_add_facilities(ac):
    facilities = await ac.post("/facilities", json={"title": "Тестовые удобства"})

    assert facilities.status_code == 200
