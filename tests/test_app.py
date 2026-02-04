from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_unregister():
    activity = "Art Club"
    encoded = quote(activity, safe="")
    email = "test.user@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    res = client.post(f"/activities/{encoded}/signup?email={email}")
    assert res.status_code == 200
    body = res.json()
    assert "Signed up" in body.get("message", "")

    # Verify participant present
    res2 = client.get("/activities")
    assert res2.status_code == 200
    assert email in res2.json()[activity]["participants"]

    # Unregister
    res3 = client.post(f"/activities/{encoded}/unregister?email={email}")
    assert res3.status_code == 200
    body3 = res3.json()
    assert "Unregistered" in body3.get("message", "")

    # Verify participant removed
    res4 = client.get("/activities")
    assert email not in res4.json()[activity]["participants"]
