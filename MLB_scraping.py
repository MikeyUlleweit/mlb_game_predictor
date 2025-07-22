#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 22:29:57 2025

@author: mikeyulleweit
"""


import pandas as pd
import requests
from datetime import date, datetime

from pybaseball import team_batting, team_pitching, pitching_stats, schedule_and_record

team_name_map = {
    "ARI": "Arizona Diamondbacks", "ATL": "Atlanta Braves", "BAL": "Baltimore Orioles", "BOS": "Boston Red Sox",
    "CHC": "Chicago Cubs", "CHW": "Chicago White Sox", "CIN": "Cincinnati Reds", "CLE": "Cleveland Guardians",
    "COL": "Colorado Rockies", "DET": "Detroit Tigers", "HOU": "Houston Astros", "KCR": "Kansas City Royals",
    "LAA": "Los Angeles Angels", "LAD": "Los Angeles Dodgers", "MIA": "Miami Marlins", "MIL": "Milwaukee Brewers",
    "MIN": "Minnesota Twins", "NYM": "New York Mets", "NYY": "New York Yankees", "OAK": "Athletics",
    "PHI": "Philadelphia Phillies", "PIT": "Pittsburgh Pirates", "SDP": "San Diego Padres", "SEA": "Seattle Mariners",
    "SFG": "San Francisco Giants", "STL": "St. Louis Cardinals", "TBR": "Tampa Bay Rays", "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays", "WSN": "Washington Nationals", "ATH": "Athletics"  # fallback for OAK
}

def build_hitting_stats_csv(season: int, output_path: str):
    date_str = datetime.today().strftime('%Y-%m-%d')
    batting_df = team_batting(season)
    batting_df['Team'] = batting_df['Team'].map(team_name_map)  # Convert abbreviation
    trimmed_df = batting_df[['Team', 'OBP', 'OPS']].copy()
    trimmed_df.columns = ['team', 'obp', 'ops']
    trimmed_df['date'] = date_str
    trimmed_df.to_csv(output_path, index=False)
    return trimmed_df.head()

def build_team_stats_csv(season: int, output_path: str):
    batting = team_batting(season)
    pitching = team_pitching(season)

    batting['Team'] = batting['Team'].map(team_name_map)
    pitching['Team'] = pitching['Team'].map(team_name_map)

    batting = batting[['Team', 'R']].rename(columns={'Team': 'team', 'R': 'runs_scored'})
    pitching = pitching[['Team', 'R']].rename(columns={'Team': 'team', 'R': 'runs_allowed'})

    df = pd.merge(batting, pitching, on='team')
    df['run_differential'] = df['runs_scored'] - df['runs_allowed']
    df['date'] = datetime.today().strftime('%Y-%m-%d')
    df = df[['team', 'date', 'runs_scored', 'runs_allowed', 'run_differential']]
    df.to_csv(output_path, index=False)



def build_pitcher_stats_csv(season: int, output_path: str):
    df = pitching_stats(season)
    df = df[['Name', 'Team', 'FIP', 'SO', 'BB', 'G']].copy()
    df.columns = ['pitcher_name', 'team', 'fip', 'SO', 'BB', 'gs_number']
    df['k_per_bb'] = df['SO'] / df['BB']
    df['opponent'] = 'TBD'  # optional placeholder
    df['date'] = datetime.today().strftime('%Y-%m-%d')
    df = df[['pitcher_name', 'team', 'date', 'opponent', 'fip', 'k_per_bb', 'gs_number']]
    df.to_csv(output_path, index=False)
    

def get_today_matchups(output_path: str):
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=probablePitcher"

    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    games = data.get('dates', [])[0].get('games', []) if data.get('dates') else []
    matchups = []

    for game in games:
        game_date = game['gameDate'][:10]
        home_team = game['teams']['home']['team']['name']  # Fix here
        away_team = game['teams']['away']['team']['name']  # Fix here
        home_pitcher = game['teams']['home'].get('probablePitcher', {}).get('fullName', 'TBD')
        away_pitcher = game['teams']['away'].get('probablePitcher', {}).get('fullName', 'TBD')

        matchups.append({
            'date': game_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_pitcher': home_pitcher,
            'away_pitcher': away_pitcher
        })

        df = pd.DataFrame(matchups)
        df.to_csv(output_path, index=False)
      

# Example usage:
get_today_matchups("game_schedule.csv")



    
if __name__ == "__main__":
    build_hitting_stats_csv(2025, 'hitting_stats.csv')
    build_team_stats_csv(2025, 'team_stats.csv')
    build_pitcher_stats_csv(2025, 'pitcher_stats.csv')
    get_today_matchups("game_schedule.csv")

     


     


