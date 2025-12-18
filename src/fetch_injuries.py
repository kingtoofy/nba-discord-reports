import requests
from bs4 import BeautifulSoup

ESPN_INJURY_URL = "https://www.espn.com/nba/injuries"

def get_injuries():
    """
    Scrapes ESPN NBA injury page (current HTML) and returns:
    {team_name: [ {player, position, status, note}, ... ]}
    """
    try:
        response = requests.get(ESPN_INJURY_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("Error fetching injuries:", e)
        return {}

    injuries_by_team = {}

    # Find all team headers (h2 tags)
    team_headers = soup.find_all("h2")
    for h2 in team_headers:
        team_name = h2.get_text(strip=True)
        injuries_by_team[team_name] = []

        # The table immediately after the h2 contains injured players
        table = h2.find_next("table")
        if not table:
            continue

        # Loop through table rows
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 4:
                continue  # skip header or malformed rows

            player_name = cols[0].get_text(strip=True)
            position = cols[1].get_text(strip=True)
            est_return = cols[2].get_text(strip=True)
            status = cols[3].get_text(strip=True)
            note = cols[4].get_text(strip=True) if len(cols) > 4 else ""

            injuries_by_team[team_name].append({
                "player": player_name,
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
    if not injuries:
        print("No injuries found or scraper failed.")
    for team, players in injuries.items():
        print(f"{team}:")
        for p in players:
            print(f"  - {p['player']} ({p['position']}) — {p['status']} [{p['note']}]")
