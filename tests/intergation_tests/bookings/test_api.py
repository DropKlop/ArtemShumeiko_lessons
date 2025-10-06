import pytest


@pytest.fixture()
async def delete_all_bookings(db):
    await db.bookings.del_()
    await db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 200)
])
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res



@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count_bookings",[
    (1, "2024-08-01", "2024-08-10", 200, 1),
    (1, "2024-08-02", "2024-08-11", 200, 2),
    (1, "2024-08-03", "2024-08-12", 200, 3)
])
async def test_add_and_get_bookings(room_id, date_from, date_to, status_code, count_bookings, authenticated_ac, delete_all_bookings):
    for _ in range(count_bookings):
        response = await authenticated_ac.post(
            "/bookings",
            json={
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
            })
        assert response.status_code == status_code
        if status_code == 200:
            res = response.json()
            assert isinstance(res, dict)
            assert res["status"] == "OK"
            assert "data" in res

    response_me = await authenticated_ac.get(
        "/bookings/me"
    )

    assert response_me.status_code == 200
    res = response_me.json()
    assert isinstance(res, dict)
    assert len(res["data"]) == count_bookings