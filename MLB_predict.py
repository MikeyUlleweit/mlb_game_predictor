#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 14:19:32 2025

@author: mikeyulleweit
"""

import pandas as pd

# === Load your data ===
games = pd.read_csv("game_schedule.csv")
team_stats = pd.read_csv("team_stats.csv")
hitting_stats = pd.read_csv("hitting_stats.csv")
pitcher_stats = pd.read_csv("pitcher_stats.csv")
weights_df = pd.read_csv("weights.csv")
weights = dict(zip(weights_df['stat'], weights_df['weight']))

# === Scoring Function ===
def compute_score(team, pitcher, team_stats, hitting_stats, pitcher_stats, weights, use_pitching=True):
    t_stats = team_stats[team_stats['team'] == team].sort_values('date').iloc[-1]
    h_stats = hitting_stats[hitting_stats['team'] == team].sort_values('date').iloc[-1]

    score = 0
    score += weights.get('run_differential', 0) * t_stats['run_differential']
    score += weights.get('obp', 0) * h_stats['obp']
    score += weights.get('ops', 0) * h_stats['ops']

    if use_pitching:
        p_stats = pitcher_stats[pitcher_stats['pitcher_name'] == pitcher]
        if not p_stats.empty:
            p_stats = p_stats.sort_values('date').iloc[-1]
            score += weights.get('k_per_bb', 0) * p_stats['k_per_bb']
            score += -weights.get('fip', 0) * p_stats['fip']

    return score

from rapidfuzz import process

def match_pitcher_name(name, pitcher_names, threshold=90):
    if not isinstance(name, str) or not name.strip():
        return None
    match = process.extractOne(name, pitcher_names, score_cutoff=threshold)
    return match[0] if match else None


# === Generate Predictions ===
predictions = []
for _, row in games.iterrows():
    home = row['home_team']
    away = row['away_team']
    p_home = row['home_pitcher']
    p_away = row['away_pitcher']

    pitcher_name_list = pitcher_stats['pitcher_name'].dropna().unique()

    matched_home_pitcher = match_pitcher_name(p_home, pitcher_name_list)
    matched_away_pitcher = match_pitcher_name(p_away, pitcher_name_list)

    has_home_pitching = matched_home_pitcher is not None
    has_away_pitching = matched_away_pitcher is not None
    use_pitching = has_home_pitching and has_away_pitching

    home_score = compute_score(home, matched_home_pitcher or "", team_stats, hitting_stats, pitcher_stats, weights, use_pitching)
    away_score = compute_score(away, matched_away_pitcher or "", team_stats, hitting_stats, pitcher_stats, weights, use_pitching)

    predicted_winner = home if home_score > away_score else away
    missing_info = ""
    if not use_pitching:
        missing_info = "partial"  # pitching removed for fairness

    predictions.append({
        'date': row['date'],
        'home_team': home,
        'away_team': away,
        'home_pitcher': p_home,
        'away_pitcher': p_away,
        'home_score': round(home_score, 3),
        'away_score': round(away_score, 3),
        'predicted_winner': predicted_winner,
        'pitching_stats_used': use_pitching,
        'note': missing_info
    })

# === Save to CSV ===
predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv("predictions.csv", index=False)
print("✅ Predictions saved to predictions.csv")

