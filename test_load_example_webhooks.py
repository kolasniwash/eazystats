import requests
from app.load_game_webhook_responses import (
    test_game_1,
    test_game_2,
    test_game_3,
)
from app.tallin_webhook_responses import (
    game_1,
    game_2,
    game_3,
    game_4
)
from app.bern_webhook_responses import game_1_bern


def test_hello_world():
    url = "http://127.0.0.1:8000"
    r = requests.get(f"{url}/")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello World"

def test_load_test_webhooks():
    url = "http://127.0.0.1:8000"
    for test_game in [game_1, game_2, game_3, game_4]:
    # for test_game in [game_1_bern]:
        r = requests.post(f"{url}/eazystats/v1/games/add", json=test_game)

        assert r.status_code == 200

    print("All test requests loaded!")
