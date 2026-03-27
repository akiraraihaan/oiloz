from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Prediction(db.Model):
    """
    Store prediction results for history and analysis
    """
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Input data
    input_data = db.Column(JSON, nullable=False)  # Store all 8 input features as JSON
    
    # Predictions
    predicted_oil = db.Column(db.Float, nullable=False)
    predicted_water = db.Column(db.Float, nullable=False)
    
    # Optimization results
    choke_actual = db.Column(db.Float, nullable=False)
    choke_recommended = db.Column(db.Float, nullable=False)
    
    # Potential gain
    potential_oil_gain = db.Column(db.Float, nullable=False)  # Difference between optimal and actual
    potential_water_reduction = db.Column(db.Float, nullable=False)
    
    # Metadata
    prediction_date = db.Column(db.Date, nullable=False)  # Date of operation
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prediction {self.id} - {self.prediction_date}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'input_data': self.input_data,
            'predicted_oil': round(self.predicted_oil, 2),
            'predicted_water': round(self.predicted_water, 2),
            'choke_actual': round(self.choke_actual, 3),
            'choke_recommended': round(self.choke_recommended, 3),
            'potential_oil_gain': round(self.potential_oil_gain, 2),
            'potential_water_reduction': round(self.potential_water_reduction, 2),
            'prediction_date': self.prediction_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class BatchUpload(db.Model):
    """
    Store batch upload metadata for tracking
    """
    __tablename__ = 'batch_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    total_rows = db.Column(db.Integer, nullable=False)
    processed_rows = db.Column(db.Integer, nullable=False)
    failed_rows = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'pending', 'processing', 'completed', 'failed'
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<BatchUpload {self.id} - {self.filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'total_rows': self.total_rows,
            'processed_rows': self.processed_rows,
            'failed_rows': self.failed_rows,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
