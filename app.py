from app import app, db
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add template filter for current year
@app.template_filter('now')
def _now(format_string='%Y'):
    return datetime.now().strftime(format_string)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    
    # In Docker, we need to listen on 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true') 