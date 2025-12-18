import requests
from bs4 import BeautifulSoup

ESPN_INJURY_URL = "https://www.espn.com/nba/injuries"

def get_injuries():
    """
    Scrapes ESPN NBA injury page and returns a dictionary:
    {team_name: [ {player, position, status, note}, ... ]}
    """
    response = requests.get(ESPN_INJURY_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    injuries_by_team = {}

    # Each team section is in a div with class "Injury__Team"
    team_sections = soup.find_all("div", class_="Injury__Team")
    for team_div in team_sections:
        team_name_tag = team_div.find("h2")
        if not team_name_tag:
            continue
        team_name = team_name_tag.text.strip()
        injuries_by_team[team_name] = []

        # Players are in divs with class 'Injury__Player'
        player_divs = team_div.find_all("div", class_="Injury__Player")
        for p_div in player_divs:
            player_name_tag = p_div.find("span", class_="Injury__PlayerName")
            position_tag = p_div.find("span", class_="Injury__PlayerPosition")
