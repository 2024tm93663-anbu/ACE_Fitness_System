import pytest
import app   # ✅ import full module, not just app object

@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    app.app.config["PROPAGATE_EXCEPTIONS"] = False

    # ✅ Override programs INSIDE app module
    app.programs = {
        "weight_loss": {
            "calorie_factor": 10,
            "workout": "Cardio",
            "diet": "Low carb",
            "color": "red"
        }
    }

    with app.app.test_client() as client:
        yield client


#  1. Success Case
def test_program_success(client):
    response = client.post("/program", json={
        "program": "weight_loss",
        "weight": 70
    })

    assert response.status_code == 200
    data = response.get_json()

    assert data["calories"] == 700
    assert data["workout"] == "Cardio"
    assert data["diet"] == "Low carb"
    assert data["color"] == "red"


#  2. Missing Program
def test_program_missing_program(client):
    response = client.post("/program", json={
        "weight": 70
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Program required"


#  3. Missing Weight
def test_program_missing_weight(client):
    response = client.post("/program", json={
        "program": "weight_loss"
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Weight required"


#  4. Invalid Program
def test_program_invalid_program(client):
    response = client.post("/program", json={
        "program": "invalid_program",
        "weight": 70
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid program"


#  5. Invalid Weight Type (Exception Case)
def test_program_invalid_weight_type(client):
    response = client.post("/program", json={
        "program": "weight_loss",
        "weight": "abc"
    })

    assert response.status_code == 500
    data = response.get_json()
    assert data["status"] == "error"