async def test_get_hotels(ac):
    hotels = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10"
        }
    )
    print(f"{hotels=}")

    assert hotels.status_code == 200