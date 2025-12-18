import requests
from bs4 import BeautifulSoup

SPORTSETHOS_URL = "https://sportsethos.com/live-injury-report/"

def get_injuries():
    injuries = {}
    response = requests.get(SPORTSETHOS_URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Each team section is a div with class 'injury-team' (check the page to confirm)
    team_sections = soup.select("div.injury-team")
    for team_div in team_sections:
        team_name_tag = team_div.find("h3")
        if not team_name_tag:
            continue
        team_name = team_name_tag.get_text(strip=True)
        injuries[team_name] = []

        # Each player in <li>
        player_rows = team_div.select("li")
        for row in player_rows:
            text = row.get_text(" ", strip=True)
            # Example: "Trae Young G Out Knee — questionable"
            parts = text.split(" — ")
            note = parts[1] if len(parts) > 1 else ""
            player_status = parts[0].split()
            if len(player_status) < 3:
                continue
            player_name = " ".join(player_status[:-2])
            position = player_status[-2]
            status = player_status[-1]
            injuries[team_name].append({
                "player": player_name,
                "position": position,
                "status": status,
                "note": note
            })
    return injuries

# Test locally
if __name__ == "__main__":
    data = get_injuries()
    for team, players in data.items():
        print(team)
        for p in players:
            print(f" - {p['player']} ({p['position']}) — {p['status']}: {p['note']}")
