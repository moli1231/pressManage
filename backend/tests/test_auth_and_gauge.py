from datetime import date, timedelta


def _login(client, phone, password):
    resp = client.post("/api/v1/auth/login", json={"phone": phone, "password": password})
    data = resp.get_json()
    return data["data"]["token"]


def test_login_success(client):
    resp = client.post("/api/v1/auth/login", json={"phone": "13600000000", "password": "User@123"})
    assert resp.status_code == 200
    assert resp.get_json()["data"]["token"]


def test_super_can_create_gauge(client):
    token = _login(client, "13700000000", "Super@123")
    payload = {
        "gauge_code": "G-001",
        "inspection_days": 365,
        "manufacturer": "Test",
        "serial_no": "SN001",
        "location": "A-01",
        "calibration_date": date.today().isoformat(),
        "gauge_type": "electronic",
    }
    resp = client.post("/api/v1/gauges", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    valid_until = resp.get_json()["data"]["valid_until"]
    assert valid_until == (date.today() + timedelta(days=365)).isoformat()


def test_user_cannot_create_gauge(client):
    token = _login(client, "13600000000", "User@123")
    payload = {
        "gauge_code": "G-002",
        "inspection_days": 30,
        "manufacturer": "Test",
        "serial_no": "SN002",
        "location": "A-02",
        "calibration_date": date.today().isoformat(),
        "gauge_type": "electronic",
    }
    resp = client.post("/api/v1/gauges", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403
