import requests
from bs4 import BeautifulSoup

ESPN_INJURY_URL = "https://www.espn.com/nba/injuries"

def get_injuries():
    """
    Scrapes ESPN NBA injury page and returns a dictionary:
    {team_name: [ {player, position, status, note}, ... ]}
    Always returns a dict, even if empty.
    """
    try:
        response = requests.get(ESPN_INJURY_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("Error fetching injuries:", e)
        return {}

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
            status_tag = p_div.find("span", class_="Injury__PlayerStatus")
            note_tag = p_div.find("span", class_="Injury__PlayerNote")

            if player_name_tag and status_tag:
                injuries_by_team[team_name].append({
                    "player": player_name_tag.text.strip(),
                    "position": position_tag.text.strip() if position_tag else "",
                    "status": status_tag.text.strip(),
                    "note": note_tag.text.strip() if note_tag else ""
                })

    return injuries_by_team  # will return {} even if no data

# -------------------------
# TEST FETCHER
# -------------------------
if __name__ == "__main__":
    injuries = get_injuries()
    if not injuries:
        print("No injuries found or scraper failed.")
    for team, players in injuries.items():
        print(f"{team}:
