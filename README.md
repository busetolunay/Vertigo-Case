# Vertigo Games - Data Engineer Case

## Project Overview
This project contains a backend API for Clan Management and a DBT model for daily metrics .

## Part 1: Backend API
- **Tech Stack:** Python (FastAPI), PostgreSQL, Docker.
- **Architecture:** - The API is containerized using Docker.
  - It connects to a PostgreSQL database ,Cloud SQL equivalent.
  - Built with Clean Architecture principles (Separation of routers, models, and schemas).

### How to Run Locally
1. Ensure Docker is installed.
2. Run `docker-compose up --build`.
3. Access API docs at `http://localhost:8080/docs`.

## Part 2: DBT & Analytics
- **Model:** `daily_metrics.sql` aggregates user activity by date, country, and platform.
- **Logic:** Uses `SAFE_DIVIDE` to handle division by zero for ratios (Win Rate, ARPDAU).

## Visualizations
**