# ipl_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style for better aesthetics
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100 # Higher resolution images

def load_data():
    """Loads match and delivery data from CSV files."""
    try:
        matches = pd.read_csv('matches_2008-2024.csv')
        deliveries = pd.read_csv('deliveries_2008-2024.csv')
        print("Data loaded successfully!")
        return matches, deliveries
    except FileNotFoundError:
        print("Error: Make sure 'matches_2008-2024.csv' and 'deliveries_2008-2024.csv' are in the correct directory.")
        return None, None

def analyze_team_wins(matches):
    """Analyzes and visualizes the number of matches won by each team."""
    print("\n--- Analysis 1: Most Successful Teams ---")
    
    # Correcting old team names to new ones for consistency
    # This is a crucial data cleaning step
    matches.replace('Deccan Chargers', 'Sunrisers Hyderabad', inplace=True)
    matches.replace('Rising Pune Supergiant', 'Rising Pune Supergiants', inplace=True)
    matches.replace('Delhi Daredevils', 'Delhi Capitals', inplace=True)
    matches.replace('Punjab Kings', 'Kings XI Punjab', inplace=True) # Standardizing to one name

    plt.figure()
    ax = sns.countplot(y='winner', data=matches, order=matches['winner'].value_counts().index, palette='viridis')
    ax.set_title('Number of Matches Won by Each Team in IPL (2008-2024)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Wins', fontsize=12)
    ax.set_ylabel('Team', fontsize=12)
    
    # Add data labels to the bars
    for container in ax.containers:
        ax.bar_label(container, padding=3)
        
    plt.tight_layout()
    plt.savefig('team_wins.png')
    print("Saved 'team_wins.png'")

def analyze_toss_impact(matches):
    """Analyzes the impact of winning the toss on the match outcome."""
    print("\n--- Analysis 2: Toss Impact ---")
    toss_winner_is_match_winner = matches['toss_winner'] == matches['winner']
    toss_impact_counts = toss_winner_is_match_winner.value_counts()
    
    plt.figure()
    plt.pie(toss_impact_counts, labels=['Toss Winner Wins', 'Toss Winner Loses'], autopct='%1.1f%%',
            startangle=140, colors=['skyblue', 'lightcoral'], wedgeprops={'edgecolor': 'black'},
            textprops={'fontsize': 12})
    plt.title('Impact of Winning the Toss on Match Outcome', fontsize=16, fontweight='bold')
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('toss_wins_pie_chart.png')
    print("Saved 'toss_wins_pie_chart.png'")

def analyze_top_run_scorers(deliveries):
    """Analyzes and visualizes the top 10 run scorers in IPL history."""
    print("\n--- Analysis 3: Top Run Scorers ---")
    batsman_runs = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    
    plt.figure()
    ax = sns.barplot(x=batsman_runs.values, y=batsman_runs.index, palette='plasma')
    ax.set_title('Top 10 Run Scorers in IPL History', fontsize=16, fontweight='bold')
    ax.set_xlabel('Total Runs', fontsize=12)
    ax.set_ylabel('Batsman', fontsize=12)
    
    for container in ax.containers:
        ax.bar_label(container, padding=3)

    plt.tight_layout()
    plt.savefig('top_run_scorers.png')
    print("Saved 'top_run_scorers.png'")

def analyze_top_wicket_takers(deliveries):
    """Analyzes and visualizes the top 10 wicket takers."""
    print("\n--- Analysis 4: Top Wicket Takers ---")
    # We consider dismissals that credit the bowler
    valid_dismissals = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    wicket_data = deliveries[deliveries['dismissal_kind'].isin(valid_dismissals)]
    top_bowlers = wicket_data['bowler'].value_counts().head(10)

    plt.figure()
    ax = sns.barplot(x=top_bowlers.values, y=top_bowlers.index, palette='mako')
    ax.set_title('Top 10 Wicket Takers in IPL History', fontsize=16, fontweight='bold')
    ax.set_xlabel('Total Wickets', fontsize=12)
    ax.set_ylabel('Bowler', fontsize=12)
    
    for container in ax.containers:
        ax.bar_label(container, padding=3)

    plt.tight_layout()
    plt.savefig('top_wicket_takers.png')
    print("Saved 'top_wicket_takers.png'")

def analyze_mom_awards(matches):
    """Analyzes and visualizes the players with the most Player of the Match awards."""
    print("\n--- Analysis 5: Top Player of the Match Awards ---")
    # Drop rows where player_of_match is NaN, as it can't be analyzed
    mom_data = matches.dropna(subset=['player_of_match'])
    top_mom = mom_data['player_of_match'].value_counts().head(10)
    
    plt.figure()
    ax = sns.barplot(x=top_mom.values, y=top_mom.index, palette='rocket')
    ax.set_title('Most Player of the Match (MoM) Awards', fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Awards', fontsize=12)
    ax.set_ylabel('Player', fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, padding=3)

    plt.tight_layout()
    plt.savefig('top_mom_awards.png')
    print("Saved 'top_mom_awards.png'")

def main():
    """Main function to run the entire analysis."""
    matches, deliveries = load_data()
    
    if matches is not None and deliveries is not None:
        analyze_team_wins(matches)
        analyze_toss_impact(matches)
        analyze_top_run_scorers(deliveries)
        analyze_top_wicket_takers(deliveries)
        analyze_mom_awards(matches)
        print("\nAnalysis complete! All 5 charts have been saved as PNG files.")

if __name__ == '__main__':
    main()
