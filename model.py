from database import db


class Model(db.Model):
    row_id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    vote =  db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Model: {self.date_created, self.vote}"