from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_injuries():
    """
    Scrapes ESPN NBA injury page using Playwright.
    Returns a dict: {team_name: [ {player, position, status, note} ]}
    """
    injuries_by_team = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.espn.com/nba/injuries")
        page.wait_for_selector("h2")  # wait for team headers to load

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        team_headers = soup.find_all("h2")
        for h2 in team_headers:
            team_name = h2.get_text(strip=True)
            injuries_by_team[team_name] = []

            table = h2.find_next("table")
            if not table:
                continue

            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) < 4:
                    continue

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

        browser.close()

    return injuries_by_team

# -------------------------
# TEST FETCHER
# -------------------------
if __name__ == "__main__":
    injuries = get_injuries()
    for team, players in injuries.items():
        if players:
            print(f"{team}:")
            for p in players:
                print(f"  - {p['player']} ({p['position']}) — {p['status']} [{p['note']}]")
