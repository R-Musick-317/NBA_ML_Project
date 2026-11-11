import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Reuse the core builder functions from Script 1 to guarantee identical schemas
from create_initial_pbi_tables import (
    DIM_TEAM_CSV,
    TEAM_STATS_CSV,
    PLAYER_STATS_CSV,
    create_dim_team,
    create_team_stats,
    create_player_stats
)


def run_twice_weekly_update():
    print("=" * 60)
    print("STARTING TWICE-WEEKLY NBA POWER BI DATA UPDATE...")
    print("=" * 60)

    # Check previous refresh status before overwriting
    prev_refresh = "None (First Run)"
    prev_avg_gp = 0.0
    if TEAM_STATS_CSV.exists():
        old_team_df = pd.read_csv(TEAM_STATS_CSV)
        if 'Last_Refreshed' in old_team_df.columns and not old_team_df.empty:
            prev_refresh = old_team_df['Last_Refreshed'].iloc[0]
        if 'GP' in old_team_df.columns and not old_team_df.empty:
            prev_avg_gp = old_team_df['GP'].mean()

    # Ensure Dim_Team.csv exists; if not, create it
    if DIM_TEAM_CSV.exists():
        dim_team_df = pd.read_csv(DIM_TEAM_CSV)
    else:
        dim_team_df = create_dim_team()

    new_timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')

    try:
        # Fetch fresh stats and overwrite existing CSVs in data/
        updated_teams = create_team_stats(dim_team_df, new_timestamp)
        updated_players = create_player_stats(updated_teams, new_timestamp)
        new_avg_gp = updated_teams['GP'].mean()

        print("\n" + "=" * 60)
        print("UPDATE SUCCESSFUL!")
        print(f" -> Previous Refresh : {prev_refresh} (Avg Team GP: {prev_avg_gp:.1f})")
        print(f" -> Current Refresh  : {new_timestamp} (Avg Team GP: {new_avg_gp:.1f})")
        print(f" -> Overwrote        : {TEAM_STATS_CSV.name} ({len(updated_teams)} rows)")
        print(f" -> Overwrote        : {PLAYER_STATS_CSV.name} ({len(updated_players)} rows)")
        print("Next Step: Open Power BI Desktop and click 'Refresh' on the Home ribbon.")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Update failed: {e}", file=sys.stderr)
        print("Your existing CSV files in 'data/' were kept intact.")
        sys.exit(1)


if __name__ == "__main__":
    run_twice_weekly_update()