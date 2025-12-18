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

    # ESPN uses tables for each team; we find all tables
    tables = soup.find_all("table")

    for table in tables:
        # Team name is in previous h2 tag
        team_tag = table.find_previous("h2")
        if not team_tag:
            continue
        team_name = team_tag.text.strip()
        injuries_by_team[team_name] = []

        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            player = cols[0].text.strip()
            position = cols[1].text.strip()
            status = cols[2].text.strip()
            note = cols[3].text.strip()
            injuries_by_team[team_name].append({
                "player": player,
                "position": position,
                "status": status,
                "note": note
            })

    return injuries_by_team

# -------------------------
# TEST FETCHER
# -------------------------
if __name__ == "__main__":
    injuries = get_injuries()
    for team, players in injuries.items():
        print(f"{team}:")
        for p in players:
            print(f"  {p['player']} ({p['position']}) — {p['status']}")
