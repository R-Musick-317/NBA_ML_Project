import time
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
from nba_api.stats.static import teams

# ==========================================
# 1. INITIAL DIRECTORY & FILE SETUP
# ==========================================
CURRENT_SEASON = '2026-27'
SEASON_TYPE = 'Regular Season'

BASE_DIR = Path(r"C:\NBA_ML_Project")
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DIM_TEAM_CSV = DATA_DIR / "Dim_Team.csv"
TEAM_STATS_CSV = DATA_DIR / "nba_team_per_game_stats.csv"
PLAYER_STATS_CSV = DATA_DIR / "nba_player_per_game_stats.csv"


def get_espn_code(abbv: str) -> str:
    """Map NBA team abbreviations to ESPN 500x500 PNG logo codes."""
    mapping = {
        "GSW": "gs", "NYK": "ny", "SAS": "sa", "NOP": "no",
        "CHA": "cha", "CHO": "cha", "UTA": "uta", "PHX": "phx", "WAS": "wsh"
    }
    return mapping.get(str(abbv), str(abbv).lower())


def create_dim_team() -> pd.DataFrame:
    print("[1/3] Creating initial Dim_Team.csv with ESPN Logo URLs...")
    nba_teams = pd.DataFrame(teams.get_teams())[
        ['id', 'abbreviation', 'full_name', 'city', 'nickname']
    ].copy()
    nba_teams.rename(columns={
        'id': 'Team_ID',
        'abbreviation': 'Team_Abbv',
        'full_name': 'Team_Name',
        'city': 'City',
        'nickname': 'Nickname'
    }, inplace=True)

    nba_teams['Logo_URL'] = nba_teams['Team_Abbv'].apply(
        lambda x: f"https://a.espncdn.com/i/teamlogos/nba/500/{get_espn_code(x)}.png"
    )
    nba_teams.to_csv(DIM_TEAM_CSV, index=False)
    return nba_teams


def create_team_stats(dim_team_df: pd.DataFrame, timestamp: str) -> pd.DataFrame:
    print(f"[2/3] Creating initial {CURRENT_SEASON} Team Per-Game Stats table...")

    team_base = leaguedashteamstats.LeagueDashTeamStats(
        season=CURRENT_SEASON,
        season_type_all_star=SEASON_TYPE,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Base',
        timeout=60
    ).get_data_frames()[0]

    time.sleep(1.5)

    team_adv = leaguedashteamstats.LeagueDashTeamStats(
        season=CURRENT_SEASON,
        season_type_all_star=SEASON_TYPE,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Advanced',
        timeout=60
    ).get_data_frames()[0]

    team_adv_cols = [
        'TEAM_ID', 'OFF_RATING', 'DEF_RATING', 'NET_RATING',
        'PACE', 'TS_PCT', 'EFG_PCT', 'OREB_PCT', 'DREB_PCT', 'PIE'
    ]
    team_df = team_base.merge(team_adv[team_adv_cols], on='TEAM_ID', how='left')
    team_df = team_df.merge(
        dim_team_df[['Team_ID', 'Team_Abbv', 'Logo_URL']],
        left_on='TEAM_ID',
        right_on='Team_ID',
        how='left'
    )

    team_columns = {
        'TEAM_ID': 'Team_ID',
        'Team_Abbv': 'Team_Abbv',
        'TEAM_NAME': 'Team_Name',
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'W_PCT': 'Win_Pct',
        'MIN': 'MIN_Per_Game',
        'PTS': 'PTS_Per_Game',
        'REB': 'REB_Per_Game',
        'OREB': 'OREB_Per_Game',
        'DREB': 'DREB_Per_Game',
        'AST': 'AST_Per_Game',
        'STL': 'STL_Per_Game',
        'BLK': 'BLK_Per_Game',
        'TOV': 'TOV_Per_Game',
        'PF': 'PF_Per_Game',
        'FGM': 'FGM_Per_Game',
        'FGA': 'FGA_Per_Game',
        'FG_PCT': 'FG_Pct',
        'FG3M': 'FG3M_Per_Game',
        'FG3A': 'FG3A_Per_Game',
        'FG3_PCT': 'FG3_Pct',
        'FTM': 'FTM_Per_Game',
        'FTA': 'FTA_Per_Game',
        'FT_PCT': 'FT_Pct',
        'PLUS_MINUS': 'Net_Points_Per_Game',
        'OFF_RATING': 'Offensive_Rating',
        'DEF_RATING': 'Defensive_Rating',
        'NET_RATING': 'Net_Rating',
        'PACE': 'Pace',
        'TS_PCT': 'TS_Pct',
        'EFG_PCT': 'eFG_Pct',
        'OREB_PCT': 'OREB_Pct',
        'DREB_PCT': 'DREB_Pct',
        'PIE': 'Team_PIE',
        'Logo_URL': 'Logo_URL'
    }

    team_df = team_df[list(team_columns.keys())].rename(columns=team_columns)
    team_df['Last_Refreshed'] = timestamp
    team_df.to_csv(TEAM_STATS_CSV, index=False)
    return team_df


def create_player_stats(team_df: pd.DataFrame, timestamp: str) -> pd.DataFrame:
    print(f"[3/3] Creating initial {CURRENT_SEASON} Player Per-Game Stats table (with PER)...")
    time.sleep(1.5)

    player_base = leaguedashplayerstats.LeagueDashPlayerStats(
        season=CURRENT_SEASON,
        season_type_all_star=SEASON_TYPE,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Base',
        timeout=60
    ).get_data_frames()[0]

    time.sleep(1.5)

    player_adv = leaguedashplayerstats.LeagueDashPlayerStats(
        season=CURRENT_SEASON,
        season_type_all_star=SEASON_TYPE,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Advanced',
        timeout=60
    ).get_data_frames()[0]

    player_adv_cols = [
        'PLAYER_ID', 'TEAM_ID', 'OFF_RATING', 'DEF_RATING',
        'NET_RATING', 'TS_PCT', 'EFG_PCT', 'USG_PCT', 'PIE'
    ]
    player_df = player_base.merge(
        player_adv[player_adv_cols], on=['PLAYER_ID', 'TEAM_ID'], how='left'
    )

    # Calculate Pace-Adjusted Hollinger PER (Normalized to 15.0 League Average)
    min_safe = player_df['MIN'].replace(0, np.nan)
    uPER = (
        player_df['FGM'] * 85.910
        + player_df['STL'] * 53.897
        + player_df['FG3M'] * 51.757
        + player_df['FTM'] * 46.845
        + player_df['BLK'] * 39.190
        + player_df['OREB'] * 39.190
        + player_df['AST'] * 34.677
        + player_df['DREB'] * 14.707
        - player_df['PF'] * 17.174
        - (player_df['FTA'] - player_df['FTM']) * 20.091
        - (player_df['FGA'] - player_df['FGM']) * 39.190
        - player_df['TOV'] * 53.897
    ) / min_safe

    league_avg_pace = team_df['Pace'].mean()
    team_pace_map = team_df.set_index('Team_ID')['Pace'].to_dict()
    player_team_pace = player_df['TEAM_ID'].map(team_pace_map).fillna(league_avg_pace)

    aPER = uPER * (league_avg_pace / player_team_pace)
    total_minutes = player_df['MIN'] * player_df['GP']
    league_avg_aPER = (aPER * total_minutes).sum() / total_minutes.sum()
    player_df['PER'] = (aPER * (15.0 / league_avg_aPER)).round(2)

    player_columns = {
        'PLAYER_ID': 'Player_ID',
        'PLAYER_NAME': 'Player_Name',
        'TEAM_ID': 'Team_ID',
        'TEAM_ABBREVIATION': 'Team_Abbv',
        'AGE': 'Age',
        'GP': 'GP',
        'W': 'W',
        'L': 'L',
        'MIN': 'MIN_Per_Game',
        'PTS': 'PTS_Per_Game',
        'REB': 'REB_Per_Game',
        'OREB': 'OREB_Per_Game',
        'DREB': 'DREB_Per_Game',
        'AST': 'AST_Per_Game',
        'STL': 'STL_Per_Game',
        'BLK': 'BLK_Per_Game',
        'TOV': 'TOV_Per_Game',
        'PF': 'PF_Per_Game',
        'FGM': 'FGM_Per_Game',
        'FGA': 'FGA_Per_Game',
        'FG_PCT': 'FG_Pct',
        'FG3M': 'FG3M_Per_Game',
        'FG3A': 'FG3A_Per_Game',
        'FG3_PCT': 'FG3_Pct',
        'FTM': 'FTM_Per_Game',
        'FTA': 'FTA_Per_Game',
        'FT_PCT': 'FT_Pct',
        'PLUS_MINUS': 'Net_Points_On_Floor_Per_Game',
        'NET_RATING': 'Net_Rating_On_Floor',
        'OFF_RATING': 'Offensive_Rating_On_Floor',
        'DEF_RATING': 'Defensive_Rating_On_Floor',
        'PER': 'PER',
        'PIE': 'NBA_PIE',
        'TS_PCT': 'TS_Pct',
        'EFG_PCT': 'eFG_Pct',
        'USG_PCT': 'Usage_Pct'
    }

    player_df = player_df[list(player_columns.keys())].rename(columns=player_columns)
    player_df['Last_Refreshed'] = timestamp
    player_df.to_csv(PLAYER_STATS_CSV, index=False)
    return player_df


if __name__ == "__main__":
    init_timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    dim_team = create_dim_team()
    team_stats = create_team_stats(dim_team, init_timestamp)
    player_stats = create_player_stats(team_stats, init_timestamp)

    print("\n" + "=" * 60)
    print(f"INITIAL SETUP COMPLETE ({init_timestamp})")
    print(f" -> Created: {DIM_TEAM_CSV} ({len(dim_team)} teams)")
    print(f" -> Created: {TEAM_STATS_CSV} ({len(team_stats)} teams)")
    print(f" -> Created: {PLAYER_STATS_CSV} ({len(player_stats)} players)")
    print("=" * 60)