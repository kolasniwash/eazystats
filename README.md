# Eazystats

A Curling statistics application to locally compile and track team performance. Application uses Streamlit for the frontend, 
Fast API backend, and PostGres to store game data. Components are orchestrated with docker compose.


## Getting Started
Clone the repo and start the application. By default a new database will be created. If restarting data will persist.

### Scoring games
Game scoring follows the Curlit scoring system. The front end accepts games scored using the format in this google sheet.

Use hte google sheet to score a game.

### Adding Games
Add a game by exporting scores to a csv from the google sheet. Upload the csv using the new game form and add the relevant game details.

### Adding Views

## Data Model

### Masterdata

### Views

Basic views available:
- Count of each point score
- Box plot of game averages