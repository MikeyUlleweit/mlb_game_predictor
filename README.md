# ⚾ MLB Game Prediction Algorithm

This project uses real-time MLB team and pitcher statistics to predict the outcome of games. It scrapes daily stats using Python and calculates matchup scores using weighted metrics.

## 🔍 What It Does

- Scrapes and builds team and pitcher stats using `pybaseball`
- Generates matchups with today's scheduled games and starting pitchers
- Applies a weighted scoring model to predict winners
- Automatically falls back to team stats if pitching data is missing
- Uses fuzzy matching to resolve inconsistencies in pitcher names

## 📊 Stats Used

Weighted metrics from `weights.csv`:
- Run Differential
- OBP (On-Base Percentage)
- OPS (On-base Plus Slugging)
- FIP (Fielding Independent Pitching)
- K/BB Ratio

## 🧠 How It Works

- `MLB_scraping.py`: Scrapes current team + pitcher stats and saves to CSVs
- `predict_games.py`: Reads today's games, computes team scores, and outputs predictions
- `predictions.csv`: Stores the predicted winner and rating for each team for the game
- Data:
    - `weights.csv`: Stores the weight for each stat used in the model
    - `game_schedule.csv`: Stores the daily mlb schedule
    - `hitting_stats.csv`: Stores the season hitting stats for each mlb team
    - `pitcher_stats.csv`: Stores every individual starting pitcher stat in mlb available
    - `team_stats.csv`: Stores the weight runs allowed, runs scored, and run differential for each mlb team

## 🏁 Getting Started

```bash
git clone https://github.com/yourusername/mlb-game-prediction-algorithm.git
cd mlb-game-prediction-algorithm
pip install -r requirements.txt
python MLB_scraping.py
python predict_games.py
```

## 📦 Dependencies

- `pandas`
- `pybaseball`
- `rapidfuzz`

Install all at once with:

```bash
pip install -r requirements.txt
```

## 📂 Sample Output

```csv
date,home_team,away_team,home_pitcher,away_pitcher,home_score,away_score,predicted_winner
2025-07-21,Guardians,Orioles,Rodon,Means,5.72,4.89,Guardians
...
```

## 🛠️ Next Steps

- Add live updating
- Track model accuracy over time
- Build a Streamlit dashboard

---

## 👨‍💻 Author

Mikey Ulleweit
