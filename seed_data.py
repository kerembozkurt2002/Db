from app import app, db, User, Team, Player, Coach, Hall, Sponsor
from datetime import date, timedelta

def seed_database():
    try:
        # Create test users
        users = [
            User(username='admin1', password='admin123', role='admin'),
            User(username='arbiter1', password='arbiter123', role='arbiter'),
            User(username='coach1', password='coach123', role='coach'),
            User(username='player1', password='player123', role='player'),
            User(username='player2', password='player123', role='player'),
            User(username='player3', password='player123', role='player'),
            User(username='player4', password='player123', role='player'),
        ]

        # Create sponsors
        sponsors = [
            Sponsor(sponsor_id=1, sponsor_name='ChessVision'),
            Sponsor(sponsor_id=2, sponsor_name='Grandmaster Corp'),
        ]

        # Create teams
        teams = [
            Team(team_name='Team Alpha', sponsor_id=1),
            Team(team_name='Team Beta', sponsor_id=2),
        ]

        # Create players
        players = [
            Player(username='player1', elorating=1800),
            Player(username='player2', elorating=1900),
            Player(username='player3', elorating=2000),
            Player(username='player4', elorating=2100),
        ]

        # Create coaches
        coaches = [
            Coach(username='coach1', team_id=1, 
                  contract_start=date.today(), 
                  contract_finish=date.today() + timedelta(days=365)),
        ]

        # Create halls
        halls = [
            Hall(hall_name='Main Hall', hall_country='USA', hall_capacity=20),
            Hall(hall_name='Grand Hall', hall_country='UK', hall_capacity=30),
        ]

        # Add all objects to the session
        for user in users:
            db.session.add(user)
        
        for sponsor in sponsors:
            db.session.add(sponsor)
        
        for team in teams:
            db.session.add(team)
        
        for player in players:
            db.session.add(player)
        
        for coach in coaches:
            db.session.add(coach)
        
        for hall in halls:
            db.session.add(hall)

        # Commit the changes
        db.session.commit()
        print("Test data added successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"Error adding test data: {e}")

if __name__ == "__main__":
    with app.app_context():
        seed_database() 