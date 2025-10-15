# 🏝️ Catan Championship Dashboard

An interactive dashboard to track your Settlers of Catan game wins with cool stats, charts, and insights!

## Features

- 🏆 **Live Leaderboard** - See who's dominating the competition
- 📊 **Interactive Charts** - Win distributions, performance timelines, and day-of-week analysis
- 🔥 **Streak Tracking** - Longest and current winning streaks
- 💡 **Epic Insights** - Fun facts like "Nash dominates on Fridays!"
- 📈 **Performance Timeline** - Watch wins accumulate over time
- 📅 **Day Analysis** - Find out which days each player performs best

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
streamlit run catan_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### 3. Expose via ngrok (Optional)

To share the dashboard with friends:

```bash
# Install ngrok if you haven't already
# Download from https://ngrok.com/download

# Start ngrok tunnel
ngrok http 8501
```

Copy the `https://` forwarding URL from ngrok and share it with your friends!

## Dashboard Sections

### 📊 Season Overview
- Total games played
- Current champion
- Longest winning streak
- Active streak tracker

### 💡 Epic Insights
- Best day for each player
- Longest streaks achieved
- Recent dominance (last 10 games)

### 🏆 Leaderboard
Complete standings with:
- Rank (with medals for top 3!)
- Total wins
- Win rate percentage
- Best streak
- Current streak

### 📈 Charts
1. **Win Distribution Pie Chart** - Visual breakdown of all wins
2. **Performance Timeline** - Cumulative wins over all games
3. **Victory by Day of Week** - Grouped bar chart showing wins by day

## Updating the Data

To update with new games, edit the `data` dictionary in the `load_data()` function in `catan_dashboard.py`:

```python
data = {
    'Date': ['09/21/2025', '09/21/2025', ...],  # Add new dates
    'Winner': ['Brandon', 'Brandon', ...]        # Add new winners
}
```

The dashboard will automatically recalculate all stats and insights!

## Tech Stack

- **Streamlit** - Interactive web app framework
- **Plotly** - Beautiful, interactive charts
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

## Tips

- Dashboard auto-refreshes when you save changes to the file
- Use ngrok for temporary public URLs (resets on restart)
- For permanent hosting, consider Streamlit Cloud (it's free!)

---

*May the dice be ever in your favor!* 🎲
