import requests


data = {
    "event_id": "01H8VC2RDR18TTZ8R4W81JX5CH",
    "event_type": "form_response",
    "form_response": {
        # ... (previous fields)
        "answers": [
            {
                "type": "choice",
                "choice": {"id": "siXDjhaKU5h1", "label": "WCT Tallinn", "ref": "778cf487-fc95-4935-8e31-009249a44137"},
                "field": {"id": "1NOefQ220T1O", "type": "dropdown", "ref": "event_name"}
            },
            {
                "type": "choice",
                "choice": {"id": "dm7mlZbnmBlu", "label": "2023/24", "ref": "1a3d3502-b7ce-4c18-a909-314515368d7e"},
                "field": {"id": "UkCaTuHQ3mY3", "type": "dropdown", "ref": "season"}
            },
            {
                "type": "date",
                "date": "2023-09-09",
                "field": {"id": "N6GSbVlHNMuS", "type": "date", "ref": "date"}
            },
            {
                "type": "text",
                "text": "miller2",
                "field": {"id": "uUfGq7t7uI7D", "type": "short_text", "ref": "opponent"}
            },
            {
                "type": "choice",
                "choice": {"id": "DSEbPWkJz49e", "label": "8", "ref": "87c4f607-ec3e-430c-87cf-8854a6d9de9e"},
                "field": {"id": "Ga4Kmv81uPxj", "type": "dropdown", "ref": "reg_ends"}
            },
            {
                "type": "choice",
                "choice": {"id": "fqVgYDdnUffQ", "label": "Round Robin", "ref": "106530e2-0065-4181-94b9-491e07836208"},
                "field": {"id": "BSX0WQoyX3Th", "type": "dropdown", "ref": "tournament_round"}
            },
            {
                "type": "choice",
                "choice": {"id": "7sGUM1wUiUJh", "label": "Sergio", "ref": "f1d88c5f-e8d0-42a6-b7bb-9486213a4cee"},
                "field": {"id": "3ivzczxMVU5I", "type": "dropdown", "ref": "lead"}
            },
            {
                "type": "choice",
                "choice": {"id": "Pzj7zkgS2GiA", "label": "Mikel", "ref": "01dc84d9-722c-4102-a4bc-d13c874c6398"},
                "field": {"id": "DYylTYdo7zEp", "type": "dropdown", "ref": "second"}
            },
            {
                "type": "choice",
                "choice": {"id": "0HQJrIRBinGD", "label": "Edu", "ref": "fc0131b4-69b7-4f31-aacd-3bb64d09e0a1"},
                "field": {"id": "knAZtsjlq1MI", "type": "dropdown", "ref": "third"}
            },
            {
                "type": "choice",
                "choice": {"id": "U99AH25K1F5F", "label": "Luis", "ref": "671c3d9b-85be-4011-b0d1-fb3b33b411f7"},
                "field": {"id": "DG4BPI314YME", "type": "dropdown", "ref": "fourth"}
            },
            {
                "type": "choice",
                "choice": {"id": "kb5pIY3cxb5w", "label": "Nico", "ref": "521aea48-c516-4e6e-8c52-5e886eabd532"},
                "field": {"id": "WwtM4gRfA3zM", "type": "dropdown", "ref": "skip"}
            },
            {
                "type": "choice",
                "choice": {"id": "4uQ1FNousmBy", "label": "None", "ref": "ac34c6ee-9cd4-4887-974c-71a840f7715f"},
                "field": {"id": "zZGCQWXU1NVJ", "type": "dropdown", "ref": "vice"}
            },
            {
                "type": "choice",
                "choice": {"id": "uzpPcQMIithh", "label": "Sergio", "ref": "3b7affa5-b9fc-4e73-9520-3dd4fcfb3d08"},
                "field": {"id": "S0zg5GJJMWiv", "type": "dropdown", "ref": "alternate"}
            },
            {
                "type": "text",
                "text": "/Users/nshaw/Code/kolasniwash/python/curling/eazystats/data/processed/ce-2023-b52-rr - ShotDataInput.csv",
                "field": {"id": "S0zg5GJJMWiv", "type": "dropdown", "ref": "stats-link"}
            }
        ],
        # "ending": {
        #     "id": "DefaultTyScreen",
        #     "ref": "default_tys"
        # }
    }
}

data2  = {
    "answers": [
            {
                "type": "choice",
                "choice": {"id": "siXDjhaKU5h1", "label": "WCT Tallinn", "ref": "778cf487-fc95-4935-8e31-009249a44137"},
                "field": {"id": "1NOefQ220T1O", "type": "dropdown", "ref": "event_name"}
            },
            {
                "type": "choice",
                "choice": {"id": "dm7mlZbnmBlu", "label": "2023/24", "ref": "1a3d3502-b7ce-4c18-a909-314515368d7e"},
                "field": {"id": "UkCaTuHQ3mY3", "type": "dropdown", "ref": "season"}
            }]
}

data3 = {
                "type": "choice",
                "choice": {"id": "siXDjhaKU5h1", "label": "WCT Tallinn", "ref": "778cf487-fc95-4935-8e31-009249a44137"},
                "field": {"id": "1NOefQ220T1O", "type": "dropdown", "ref": "event_name"}
            }

data4 = {
    "type": "choice",
    "choice": {"id": "siXDjhaKU5h1", "label": "WCT Tallinn", "ref": "778cf487-fc95-4935-8e31-009249a44137"},
    "field": {"id": "1NOefQ220T1O", "type": "dropdown", "ref": "event_name"}
}

answer = {
                "type": "choice",
                "choice": {
                    "id": "S28CLsE7T6Pd",
                    "label": "WCT Lodz",
                    "ref": "697ebba6-29db-47a1-a9c5-4a5631168cdc"
                },
                "field": {
                    "id": "1NOefQ220T1O",
                    "type": "dropdown",
                    "ref": "event_name"
                }
            }
from typeform_post_response import example_response
# @pytest.mark.usefixtures("restart_api")
def test_add_game_detail():
    url = "http://127.0.0.1:8000"
    r = requests.post(f"{url}/eazystats/v1/games/add", json=example_response)
    print(r.content)
    assert r.status_code == 200
    response = r.json()["game_details"]
    # game = json.loads(response["game"])
    # lineup = json.loads(response["lineup"])

    assert response["event_name"] == 'WCT Lodz'
    assert response["opponent"] == "miller strong"
    assert response["lead"] == 'Mikel'
    assert response["fourth"] == 'Luis'
    assert response['sheet_id'] == "1cfa8eWoapGHUpCYhgqgb4OrfagE536pQsgeh-sx9W1k"
    assert response['sheet_name'] == "ShotDataInput"



# @pytest.mark.usefixtures("restart_api")
def test_root():
    url = "http://127.0.0.1:8000"
    r = requests.get(f"{url}/")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello World"

