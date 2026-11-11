# 🏀 NBA Machine Learning & Power BI Analytics Project

An end-to-end NBA analytics and machine learning repository designed to track team and player efficiency in **Power BI** and predict **Against the Spread (ATS)** game outcomes using Python and `nba_api`.

---

## 📌 Project Overview & Architecture

Modeled after our production NFL betting pipeline, this project adapts possession-based efficiency metrics and rolling form windows to the 82-game NBA regular season:

1. **Data Extraction & Efficiency Metrics:** Pulls official NBA box score and advanced per-game splits via `nba_api`, anchoring on pace-independent **Net Rating** (`Offensive_Rating` / `Defensive_Rating`), **True Shooting Percentage (`TS_Pct`)**, **Effective Field Goal Percentage (`eFG_Pct`)**, **Pace**, **Rebound Percentages (`OREB_Pct` / `DREB_Pct`)**, and **Pace-Adjusted Hollinger Player Efficiency Rating (`PER`)**.
2. **Feature Engineering (In Progress):** Applies shifted rolling averages (`.rolling(window).mean().shift(1)` across 5-game and 10-game windows) alongside rest-day and back-to-back indicators inside `notebooks/NBA_ML_Notebook.ipynb` to capture current team form without data leakage.
3. **ATS Target Creation (Planned):** Maps historical closing spreads to binary cover outcomes (`1 = Home Covers`, `0 = Away Covers`), excluding exact pushes.
4. **Model Training & Evaluation (Planned):** Uses chronological train/test splits with Logistic Regression and Random Forest / XGBoost classifiers saved to `models/`, aiming to clear the standard `-110` juice breakeven threshold of **52.38%**.

---

## 📂 Repository Structure

```text
NBA_ML_Project/
├── .vscode/
│   └── settings.json                    # Workspace configuration
├── data/
│   ├── Dim_Team.csv                     # 30 NBA teams with IDs, abbreviations, and ESPN 500x500 PNG Logo URLs
│   ├── nba_player_per_game_stats.csv    # 2026-27 Per-Game & Advanced Player Stats (with Hollinger PER)
│   └── nba_team_per_game_stats.csv      # 2026-27 Per-Game & Advanced Team Stats
├── models/                              # Saved ML model artifacts (.pkl / .joblib)
├── notebooks/
│   └── NBA_ML_Notebook.ipynb            # Main Jupyter notebook for data exploration & ML pipeline
├── power bi/                            # Power BI dashboard (.pbix) files and custom Deneb templates
├── src/
│   ├── create_initial_pbi_tables.py     # One-time baseline initializer for Power BI static CSV tables
│   └── update_pbi_tables.py             # Twice-weekly refresh script that overwrites static CSVs in data/
├── .gitignore                           # Excludes nba_env/, __pycache__/, .vscode/, and Power BI lock files
├── requirements.txt                     # Python package dependencies
└── README.md                            # Project documentation