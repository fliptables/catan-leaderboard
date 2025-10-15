import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from collections import Counter
import numpy as np

# Page config
st.set_page_config(
    page_title="🏝️ Catan Championship Dashboard",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        text-align: center;
    }
    .trophy {
        font-size: 80px;
        text-align: center;
    }
    h1 {
        text-align: center;
        color: #ff6b6b;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
        font-size: 18px;
        font-weight: 500;
    }
    .player-nash { color: #ff6b6b; font-weight: bold; }
    .player-brandon { color: #4ecdc4; font-weight: bold; }
    .player-jason { color: #ffe66d; font-weight: bold; }
    .player-vich { color: #95e1d3; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    data = {
        'Date': ['09/21/2025', '09/21/2025', '09/23/2025', '09/23/2025', '09/25/2025',
                 '09/27/2025', '09/27/2025', '09/27/2025', '09/29/2025', '09/29/2025',
                 '09/30/2025', '09/30/2025', '10/04/2025', '10/04/2025', '10/04/2025',
                 '10/06/2025', '10/06/2025', '10/06/2025', '10/07/2025', '10/07/2025',
                 '10/10/2025', '10/10/2025', '10/10/2025', '10/10/2025', '10/13/2025',
                 '10/13/2025', '10/13/2025', '10/15/2025', '10/15/2025', '10/15/2025'],
        'Winner': ['Brandon', 'Brandon', 'Nash', 'Jason', 'Nash', 'Vich', 'Nash', 'Nash',
                   'Brandon', 'Jason', 'Nash', 'Nash', 'Nash', 'Nash', 'Vich', 'Nash',
                   'Brandon', 'Nash', 'Brandon', 'Nash', 'Nash', 'Nash', 'Brandon', 'Nash',
                   'Brandon', 'Nash', 'Brandon', 'Vich', 'Brandon', 'Jason']
    }
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['GameNumber'] = range(1, len(df) + 1)
    
    return df

df = load_data()

# Calculate statistics
def calculate_stats(df):
    total_games = len(df)
    win_counts = df['Winner'].value_counts()
    
    # Win rates
    win_rates = (win_counts / total_games * 100).round(1)
    
    # Streaks
    def get_streaks(df, player):
        wins = (df['Winner'] == player).astype(int)
        streaks = []
        current_streak = 0
        
        for win in wins:
            if win:
                current_streak += 1
            else:
                if current_streak > 0:
                    streaks.append(current_streak)
                current_streak = 0
        if current_streak > 0:
            streaks.append(current_streak)
        
        return max(streaks) if streaks else 0, current_streak
    
    streak_data = {}
    for player in win_counts.index:
        longest, current = get_streaks(df, player)
        streak_data[player] = {'longest': longest, 'current': current}
    
    # Day of week analysis
    day_winners = df.groupby(['DayOfWeek', 'Winner']).size().reset_index(name='Wins')
    
    # Best day for each player
    best_days = {}
    for player in win_counts.index:
        player_days = df[df['Winner'] == player]['DayOfWeek'].value_counts()
        if len(player_days) > 0:
            best_days[player] = player_days.index[0]
    
    return {
        'total_games': total_games,
        'win_counts': win_counts,
        'win_rates': win_rates,
        'streaks': streak_data,
        'day_winners': day_winners,
        'best_days': best_days
    }

stats = calculate_stats(df)

# Header
st.markdown("# 🏝️ Catan Championship Dashboard")
st.markdown("### 🎲 *Where legends are made and friendships are tested*")
st.markdown("---")

# Top section - Champion and key stats
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 🏆 Current Champion")
    champion = stats['win_counts'].index[0]
    champion_wins = stats['win_counts'].iloc[0]
    
    player_colors = {
        'Nash': '🔴',
        'Brandon': '🔵', 
        'Jason': '🟡',
        'Vich': '🟢'
    }
    
    st.markdown(f"<div class='trophy'>{player_colors.get(champion, '👑')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font' style='color: #ff6b6b;'>{champion}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 24px; color: #888;'>{champion_wins} victories</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 Season Overview")
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric("Total Games", stats['total_games'])
    
    with metric_cols[1]:
        longest_streak_player = max(stats['streaks'].items(), key=lambda x: x[1]['longest'])
        st.metric("Longest Streak", f"{longest_streak_player[1]['longest']}", 
                  f"{longest_streak_player[0]}")
    
    with metric_cols[2]:
        most_recent_winner = df.iloc[-1]['Winner']
        st.metric("Last Winner", most_recent_winner)
    
    with metric_cols[3]:
        active_players = len(stats['win_counts'])
        st.metric("Active Players", active_players)

with col3:
    st.markdown("### 🔥 Hot Streak")
    current_streaks = [(p, s['current']) for p, s in stats['streaks'].items() if s['current'] > 0]
    
    if current_streaks:
        current_streaks.sort(key=lambda x: x[1], reverse=True)
        streak_player, streak_count = current_streaks[0]
        st.markdown(f"<div style='text-align: center; font-size: 60px;'>{player_colors.get(streak_player, '🔥')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-font' style='font-size: 30px; color: #ffd93d;'>{streak_player}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 20px; color: #888;'>{streak_count} game streak!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; color: #888;'>No active streaks</div>", unsafe_allow_html=True)

st.markdown("---")

# Cool Facts Section
st.markdown("## 💡 Epic Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    # Best day analysis
    for player, day in stats['best_days'].items():
        player_day_count = len(df[(df['Winner'] == player) & (df['DayOfWeek'] == day)])
        total_player_wins = stats['win_counts'][player]
        percentage = (player_day_count / total_player_wins * 100)
        
        if percentage >= 30:  # Only show if significant
            st.markdown(f"""
                <div class='insight-box'>
                    🗓️ <strong>{player}</strong> dominates on <strong>{day}s</strong><br>
                    {player_day_count} of {total_player_wins} wins ({percentage:.0f}%)
                </div>
            """, unsafe_allow_html=True)

with insights_col2:
    # Longest streak insight
    for player, streak_info in stats['streaks'].items():
        if streak_info['longest'] >= 3:
            st.markdown(f"""
                <div class='insight-box'>
                    🔥 <strong>{player}</strong> had an epic {streak_info['longest']}-game winning streak!
                </div>
            """, unsafe_allow_html=True)

# Recent dominance
recent_10 = df.tail(10)
recent_winner_counts = recent_10['Winner'].value_counts()
if len(recent_winner_counts) > 0:
    recent_leader = recent_winner_counts.index[0]
    recent_leader_wins = recent_winner_counts.iloc[0]
    if recent_leader_wins >= 5:
        st.markdown(f"""
            <div class='insight-box'>
                ⚡ <strong>{recent_leader}</strong> is on fire! {recent_leader_wins} wins in the last 10 games!
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Charts section
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### 🏆 Leaderboard")
    
    # Create leaderboard dataframe
    leaderboard_data = []
    for i, (player, wins) in enumerate(stats['win_counts'].items(), 1):
        rank_emoji = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, f'{i}.')
        
        leaderboard_data.append({
            'Rank': rank_emoji,
            'Player': player,
            'Wins': wins,
            'Win Rate': f"{stats['win_rates'][player]}%",
            'Best Streak': stats['streaks'][player]['longest'],
            'Current': stats['streaks'][player]['current'] if stats['streaks'][player]['current'] > 0 else '-'
        })
    
    leaderboard_df = pd.DataFrame(leaderboard_data)
    
    # Display as HTML table for better styling
    st.dataframe(
        leaderboard_df,
        hide_index=True,
        use_container_width=True,
        height=250
    )

with chart_col2:
    st.markdown("### 📈 Win Distribution")
    
    # Pie chart
    colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3']
    fig_pie = px.pie(
        values=stats['win_counts'].values,
        names=stats['win_counts'].index,
        color_discrete_sequence=colors,
        hole=0.4
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
    fig_pie.update_layout(
        showlegend=False,
        height=300,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Performance over time
st.markdown("### 📊 Performance Timeline")

# Cumulative wins chart
cumulative_data = []
for player in stats['win_counts'].index:
    player_df = df[df['Winner'] == player].copy()
    player_df['CumulativeWins'] = range(1, len(player_df) + 1)
    player_df['Player'] = player
    cumulative_data.append(player_df[['GameNumber', 'CumulativeWins', 'Player', 'Date']])

cumulative_df = pd.concat(cumulative_data)

fig_timeline = px.line(
    cumulative_df,
    x='GameNumber',
    y='CumulativeWins',
    color='Player',
    markers=True,
    color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3']
)

fig_timeline.update_layout(
    xaxis_title="Game Number",
    yaxis_title="Total Wins",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Day of week analysis
st.markdown("### 📅 Victory by Day of Week")

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_winners_pivot = stats['day_winners'].pivot(index='DayOfWeek', columns='Winner', values='Wins').fillna(0)
day_winners_pivot = day_winners_pivot.reindex([d for d in day_order if d in day_winners_pivot.index])

fig_days = go.Figure()

colors_map = {'Nash': '#ff6b6b', 'Brandon': '#4ecdc4', 'Jason': '#ffe66d', 'Vich': '#95e1d3'}

for player in day_winners_pivot.columns:
    fig_days.add_trace(go.Bar(
        name=player,
        x=day_winners_pivot.index,
        y=day_winners_pivot[player],
        marker_color=colors_map.get(player, '#888888')
    ))

fig_days.update_layout(
    barmode='group',
    xaxis_title="Day of Week",
    yaxis_title="Number of Wins",
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_days, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        🎲 May the dice be ever in your favor 🎲<br>
        <small>Built with ❤️ and Streamlit | Data updates in real-time</small>
    </div>
""", unsafe_allow_html=True)
