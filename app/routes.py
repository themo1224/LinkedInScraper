from flask import render_template, redirect, url_for, request, jsonify, flash
from app import app, db
from app.models import Job
from app.scrapers.linkedin import LinkedInScraper
import threading

@app.route('/')
def index():
    # Get the jobs from the database 
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('index.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Find similar jobs
    similar_jobs = Job.query.filter(
        (Job.job_title.ilike(f'%{job.job_title.split()[0]}%')) | 
        (Job.company_name == job.company_name)
    ).filter(Job.id != job.id).limit(5).all()
    
    return render_template('job_details.html', job=job, similar_jobs=similar_jobs)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        keywords = request.form.get('keywords', 'Laravel developer')
        location = request.form.get('location', 'Remote')
        visa_sponsorship = request.form.get('visa_sponsorship') == 'on'
        
        # Start the scraping in a background thread
        def run_scraper():
            scraper = LinkedInScraper()
            if scraper.login():
                scraper.search_jobs(keywords, location, check_visa_sponsorship=visa_sponsorship)
            scraper.close()
        
        thread = threading.Thread(target=run_scraper)
        thread.daemon = True
        thread.start()
        
        flash('Scraping started in the background. Check back soon for results.', 'success')
        return redirect(url_for('index'))
    
    return render_template('scrape.html')

@app.route('/api/jobs')
def api_jobs():
    # Optional filtering
    is_remote = request.args.get('is_remote', type=bool)
    keyword = request.args.get('keyword', type=str)
    has_visa_sponsorship = request.args.get('visa_sponsorship', type=bool)
    
    query = Job.query
    
    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)
    
    if keyword:
        query = query.filter(Job.job_title.ilike(f'%{keyword}%') | 
                            Job.description.ilike(f'%{keyword}%'))
    
    if has_visa_sponsorship is not None:
        query = query.filter(Job.has_visa_sponsorship == has_visa_sponsorship)
    
    jobs = query.order_by(Job.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/job/<int:job_id>')
def api_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())
