# Chess Tournament Management System

A Flask-based web application for managing chess tournaments, matches, and players.

## Features

- User authentication (Players, Coaches, Arbiters, Admins)
- Match management
- Player assignments
- Match ratings
- Hall management
- Team management

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://user:password@localhost/chess_tournament
```

4. Set up the MySQL database:
- Create a database named `chess_tournament`
- Import the SQL schema from `code/triggers.sql`

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Database Schema

The application uses the following main tables:
- users
- teams
- coaches
- players
- player_teams
- matches
- match_assignments
- halls

## User Roles

- Player: Can view matches and their assignments
- Coach: Can manage team players and view team matches
- Arbiter: Can create matches and submit ratings
- Admin: Full access to all features

## Security Notes

- In production, ensure to use proper password hashing
- Set a strong SECRET_KEY in the .env file
- Use HTTPS in production
- Implement proper input validation and sanitization 