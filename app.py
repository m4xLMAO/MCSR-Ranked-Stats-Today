from flask import Flask, render_template, request
import requests
import math
import os

app = Flask(__name__)

def fetch_today_stats(username):
    response = requests.get(
        f"https://mcsr-stats.memerson.xyz/api/matches?timeframe=12 hours&username={username}"
    )
    data = response.json()
    if 'error' in data:
        return {'error': data['error']}

    total_elo_change = data['totalEloChange']
    won_matches_count = data['wonMatchesCount']
    loss_matches_count = data['lossMatchesCount']
    draw_count = data['drawCount']

    total_matches = won_matches_count + loss_matches_count
    if total_matches > 0:
        win_percentage = (won_matches_count / total_matches) * 100
        formatted_percentage = f"{math.ceil(win_percentage * 100) / 100}%"
    else:
        formatted_percentage = "0%"

    return {
        'username': username,
        'total_elo_change': total_elo_change,
        'won_matches_count': won_matches_count,
        'loss_matches_count': loss_matches_count,
        'draw_count': draw_count,
        'win_percentage': formatted_percentage
    }

@app.route("/", methods=["GET", "POST"])
def index():
    stats = None
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        stats = fetch_today_stats(username)
        if 'error' in stats:
            error = stats['error']
            stats = None
    return render_template("index.html", stats=stats, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
