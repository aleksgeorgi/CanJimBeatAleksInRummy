from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class RawScores(db.Model):
    __tablename__ = 'raw_scores'

    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer, nullable=False) # TODO find out if SERIAL/able is being left out here?
    jim_score = db.Column(db.Integer, nullable=False)
    aleks_score = db.Column(db.Integer, nullable=False)
    jim_running_sum = db.Column(db.Integer)
    aleks_running_sum = db.Column(db.Integer)
