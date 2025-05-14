from app import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    job_link = db.Column(db.Text, unique=True, nullable=False)
    is_remote = db.Column(db.Boolean, default=False)
    has_visa_sponsorship = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    salary_range = db.Column(db.String(255))
    experience_level = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """
        This method returns a string representation of the Job object.
        It includes the job title and company name, providing a concise description of the job.
        """
        return f'<Job {self.job_title} at {self.company_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'location': self.location,
            'job_link': self.job_link,
            'is_remote': self.is_remote,
            'has_visa_sponsorship': self.has_visa_sponsorship,
            'description': self.description,
            'posted_date': self.posted_date.strftime('%Y-%m-%d %H:%M:%S') if self.posted_date else None,
            'salary_range': self.salary_range,
            'experience_level': self.experience_level,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } 