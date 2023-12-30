# Eazystats

A Curling statistics application to locally compile and track team performance. Application uses Streamlit for the frontend, 
Fast API backend, and PostGres to store game data. Components are orchestrated with docker compose.

## Getting Started
Clone the repo and start the application using `make run`. By default a new database will be created. If restarting data will persist.

### Scoring games
Game scoring follows the Curlit scoring system. The front end accepts games scored using the format in [this google sheet](https://docs.google.com/spreadsheets/d/1XVg_Lm2F4MZSj9wDzj9V0WIj7Yg4PQvzi153NtvE2mQ/edit?usp=sharing)

Use the google sheet to score a game.

### Adding Games
Add a game by exporting scores from google sheets to a csv. Upload the csv using the new game form and add the relevant game details.

## Data Model
The database is split into three layers. Each layer represents different kind of data.
- Base layer are input tables from the web frontend
  - `shot_scores` records the shot scoring data as input in the game scoring csv.
  - `games` records a game event as a game_id and similar data (score, win/loss, etc)
  - `player_lineups` records positions of each player for a given game_id
- Masterdata layer are the tables that all views reference
  - `statistics` is an aggregated shot scoring data
  - `gamescores` is an aggregated fact table of game data
- View layer are queries that provide data to the front end views.

### Views
Current views available:
- Count of each point score presented as a normalized stacked bar chart
- Box plot of game averages