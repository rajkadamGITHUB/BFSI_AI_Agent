from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_questions():

    response = client.get("/questions")

    assert response.status_code == 200

    data = response.json()

    assert "questions" in data

    assert len(data["questions"]) > 0


def test_invalid_question():

    response = client.post(
        "/chat",
        json={
            "question_id": "random_question"
        }
    )

    assert response.status_code == 400