from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import and_, or_

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1:3306/chessdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'init_command': "SET sql_mode='STRICT_ALL_TABLES'"
    }
}

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models matching the SQL schema exactly
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum('manager','player','coach','arbiter'), nullable=False)

    def get_id(self):
        return self.username

class Manager(db.Model):
    __tablename__ = 'managers'
    username = db.Column(db.String(50), db.ForeignKey('users.username'), primary_key=True)
    password = db.Column(db.String(256), nullable=False)

class Arbiter(db.Model):
    __tablename__ = 'arbiters'
    username = db.Column(db.String(50), db.ForeignKey('users.username'), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.Enum('beginner','intermediate','advanced','expert'), nullable=False)

class ArbiterCertification(db.Model):
    __tablename__ = 'arbiter_certifications'
    username = db.Column(db.String(50), db.ForeignKey('arbiters.username'), primary_key=True)
    certification = db.Column(db.String(50), primary_key=True)

class Title(db.Model):
    __tablename__ = 'title'
    title_id = db.Column(db.Integer, primary_key=True)
    title_name = db.Column(db.String(50), nullable=False)

class Player(db.Model):
    __tablename__ = 'players'
    username = db.Column(db.String(50), db.ForeignKey('users.username'), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    dateofbirth = db.Column(db.Date, nullable=False)
    elorating = db.Column(db.Integer, nullable=False)
    fideid = db.Column(db.String(100), nullable=False)
    titleid = db.Column(db.Integer, db.ForeignKey('title.title_id'), nullable=False)
    team_list = db.Column(db.String(50), nullable=False)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    sponsor_id = db.Column(db.Integer, primary_key=True)
    sponsor_name = db.Column(db.String(100), nullable=False, unique=True)

class Team(db.Model):
    __tablename__ = 'teams'
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.sponsor_id'), nullable=False)

class Coach(db.Model):
    __tablename__ = 'coaches'
    username = db.Column(db.String(50), db.ForeignKey('users.username'), primary_key=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    nationality = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), primary_key=True)
    contract_start = db.Column(db.Date, primary_key=True)
    contract_finish = db.Column(db.Date, nullable=False)

class CoachCertification(db.Model):
    __tablename__ = 'coach_certifications'
    coach_username = db.Column(db.String(50), db.ForeignKey('coaches.username'), primary_key=True)
    certification = db.Column(db.String(50), primary_key=True)

class Hall(db.Model):
    __tablename__ = 'halls'
    hall_id = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(100), nullable=False)
    hall_country = db.Column(db.String(50), nullable=False)
    hall_capacity = db.Column(db.Integer, nullable=False)

class MatchTable(db.Model):
    __tablename__ = 'match_tables'
    table_id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('halls.hall_id'), nullable=False)

class PlayerTeam(db.Model):
    __tablename__ = 'player_teams'
    username = db.Column(db.String(50), db.ForeignKey('players.username'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), primary_key=True)

class Match(db.Model):
    __tablename__ = 'matches'
    match_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.Time, nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('halls.hall_id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('match_tables.table_id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    arbiter_username = db.Column(db.String(50), db.ForeignKey('arbiters.username'), nullable=False)
    ratings = db.Column(db.Integer)

class MatchAssignment(db.Model):
    __tablename__ = 'match_assignments'
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), primary_key=True)
    white_player = db.Column(db.String(50), db.ForeignKey('players.username'), nullable=False)
    black_player = db.Column(db.String(50), db.ForeignKey('players.username'), nullable=False)
    result = db.Column(db.Enum('black wins','white wins','draw'), nullable=False)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.get(username)
        
        if user and user.password == password:  # In production, use proper password hashing
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Match management routes
@app.route('/matches')
@login_required
def matches():
    Team1 = db.aliased(Team)
    Team2 = db.aliased(Team)
    matches = db.session.query(Match, Team1.team_name.label('team1_name'), Team2.team_name.label('team2_name'), Hall.hall_name, MatchTable.table_id).join(Team1, Match.team1_id == Team1.team_id).join(Team2, Match.team2_id == Team2.team_id).join(Hall, Match.hall_id == Hall.hall_id).join(MatchTable, Match.table_id == MatchTable.table_id).all()
    return render_template('matches.html', matches=[{'match': m[0], 'team1_name': m[1], 'team2_name': m[2], 'hall_name': m[3], 'table_id': m[4]} for m in matches])

@app.route('/matches/create', methods=['GET', 'POST'])
@login_required
def create_match():
    if current_user.role not in ['admin', 'arbiter']:
        flash('You do not have permission to create matches')
        return redirect(url_for('matches'))

    if request.method == 'POST':
        try:
            # Get form data
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            time = datetime.strptime(request.form['time'], '%H:%M').time()
            hall_id = int(request.form['hall_id'])
            table_id = int(request.form['table_id'])
            team1_id = int(request.form['team1_id'])
            team2_id = int(request.form['team2_id'])
            arbiter_username = request.form['arbiter_username']

            # Validate teams are different
            if team1_id == team2_id:
                flash('Teams must be different')
                return redirect(url_for('create_match'))

            # Check hall/table availability
            existing_match = Match.query.filter(
                and_(
                    Match.date == date,
                    Match.hall_id == hall_id,
                    Match.table_id == table_id,
                    or_(
                        and_(Match.time_slot <= time, time < db.func.addtime(Match.time_slot, '02:00:00')),
                        and_(time <= Match.time_slot, Match.time_slot < db.func.addtime(time, '02:00:00'))
                    )
                )
            ).first()

            if existing_match:
                flash('The selected hall/table is already booked for this time slot')
                return redirect(url_for('create_match'))

            # Create new match
            new_match = Match(
                date=date,
                time_slot=time,
                hall_id=hall_id,
                table_id=table_id,
                team1_id=team1_id,
                team2_id=team2_id,
                arbiter_username=arbiter_username
            )

            db.session.add(new_match)
            db.session.commit()
            flash('Match created successfully')
            return redirect(url_for('matches'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating match: {str(e)}')
            return redirect(url_for('create_match'))

    # GET request - show form
    halls = Hall.query.all()
    teams = Team.query.all()
    arbiters = User.query.filter_by(role='arbiter').all()
    return render_template('create_match.html', halls=halls, teams=teams, arbiters=arbiters)

@app.route('/matches/<int:match_id>/assign', methods=['GET', 'POST'])
@login_required
def assign_players(match_id):
    if current_user.role not in ['admin', 'arbiter']:
        flash('You do not have permission to assign players')
        return redirect(url_for('matches'))

    match = Match.query.get_or_404(match_id)
    
    if request.method == 'POST':
        try:
            white_player = request.form['white_player']
            black_player = request.form['black_player']
            result = request.form['result']

            # Validate players belong to correct teams
            if not PlayerTeam.query.filter_by(username=white_player, team_id=match.team1_id).first():
                flash('White player must be from Team 1')
                return redirect(url_for('assign_players', match_id=match_id))

            if not PlayerTeam.query.filter_by(username=black_player, team_id=match.team2_id).first():
                flash('Black player must be from Team 2')
                return redirect(url_for('assign_players', match_id=match_id))

            # Check for player schedule conflicts
            existing_assignments = MatchAssignment.query.join(Match).filter(
                and_(
                    Match.date == match.date,
                    or_(
                        MatchAssignment.white_player == white_player,
                        MatchAssignment.black_player == white_player,
                        MatchAssignment.white_player == black_player,
                        MatchAssignment.black_player == black_player
                    ),
                    or_(
                        and_(Match.time_slot <= match.time_slot, match.time_slot < db.func.addtime(Match.time_slot, '02:00:00')),
                        and_(match.time_slot <= Match.time_slot, Match.time_slot < db.func.addtime(match.time_slot, '02:00:00'))
                    )
                )
            ).first()

            if existing_assignments:
                flash('One or both players are already assigned to a match at this time')
                return redirect(url_for('assign_players', match_id=match_id))

            # Create assignment
            assignment = MatchAssignment(
                match_id=match_id,
                white_player=white_player,
                black_player=black_player,
                result=result
            )

            db.session.add(assignment)
            db.session.commit()
            flash('Players assigned successfully')
            return redirect(url_for('matches'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error assigning players: {str(e)}')
            return redirect(url_for('assign_players', match_id=match_id))

    # GET request - show form
    team1_players = Player.query.join(PlayerTeam).filter(PlayerTeam.team_id == match.team1_id).all()
    team2_players = Player.query.join(PlayerTeam).filter(PlayerTeam.team_id == match.team2_id).all()
    return render_template('assign_players.html', match_id=match_id, team1_players=team1_players, team2_players=team2_players)

if __name__ == '__main__':
    app.run(debug=True) 