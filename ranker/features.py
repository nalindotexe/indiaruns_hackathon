import math
from datetime import datetime
from ranker.constants import EMBEDDING_KEYWORDS, VECTOR_DB_KEYWORDS, EVAL_KEYWORDS, FINETUNING_KEYWORDS, PRODUCTION_SIGNALS, CONSULTING_FIRMS

def extract_features(candidate):
    f = {}
    skills = candidate.get('skills', [])
    career = candidate.get('career_history', [])
    signals = candidate.get('redrob_signals', {})
    profile = candidate.get('profile', {})
    
    # Helper to calculate weighted skill score based on endorsements and duration
    def keyword_match(skill_list, keywords):
        score = 0
        for skill in skill_list:
            name = skill.get('name', '').lower()
            if any(k in name for k in keywords):
                prof_mult = {'beginner': 0.5, 'intermediate': 1.0, 'advanced': 1.5, 'expert': 2.0}.get(skill.get('proficiency', '').lower(), 1.0)
                dur = min(skill.get('duration_months', 0) / 12.0, 5.0) # max 5 years impact
                endorses = min(skill.get('endorsements', 0) / 10.0, 2.0) # max 2.0 impact
                score += prof_mult * (1 + dur) * (1 + endorses)
        return min(score / 10.0, 1.0) # normalize roughly to 0-1
        
    # --- TECHNICAL ---
    f['embedding_score'] = keyword_match(skills, EMBEDDING_KEYWORDS)
    f['vector_db_score'] = keyword_match(skills, VECTOR_DB_KEYWORDS)
    f['eval_framework_score'] = keyword_match(skills, EVAL_KEYWORDS)
    f['finetuning_score'] = keyword_match(skills, FINETUNING_KEYWORDS)
    
    # Technical bonus from descriptions
    desc_text = " ".join([role.get('description', '').lower() for role in career])
    if any(k in desc_text for k in VECTOR_DB_KEYWORDS): f['vector_db_score'] = min(1.0, f['vector_db_score'] + 0.5)
    if any(k in desc_text for k in EMBEDDING_KEYWORDS): f['embedding_score'] = min(1.0, f['embedding_score'] + 0.5)
    
    # --- EXPERIENCE QUALITY ---
    total_years = profile.get('years_of_experience', 0)
    # Score range: ideal 6-8 years
    if 6 <= total_years <= 8:
        f['total_exp_score'] = 1.0
    elif 4 <= total_years < 6:
        f['total_exp_score'] = 0.8
    elif 8 < total_years <= 10:
        f['total_exp_score'] = 0.9
    elif 3 <= total_years < 4:
        f['total_exp_score'] = 0.5
    else:
        f['total_exp_score'] = 0.3
        
    # Product company ratio
    total_months = 1 # avoid div zero
    product_months = 0
    for role in career:
        dur = role.get('duration_months', 0)
        total_months += dur
        company = role.get('company', '').lower()
        if not any(cf in company for cf in CONSULTING_FIRMS):
            product_months += dur
    f['product_co_ratio'] = product_months / total_months
    
    # AI Experience
    f['ai_exp_score'] = min(product_months / 60.0, 1.0) # Assume some ratio of their product exp is relevant if skills match
    
    # --- SHIPPER SIGNALS ---
    f['production_signal'] = 1.0 if any(k in desc_text for k in PRODUCTION_SIGNALS) else 0.0
    github_score = signals.get('github_activity_score', -1)
    f['github_signal'] = 1.0 if github_score > 10 else 0.0
    
    sizes = [role.get('company_size', '') for role in career]
    f['startup_bonus'] = 1.0 if any(s in ['1-10', '11-50', '51-200'] for s in sizes) else 0.0
    
    # --- BEHAVIORAL SIGNALS ---
    f['response_rate'] = signals.get('recruiter_response_rate', 0.0)
    
    last_active = signals.get('last_active_date')
    days_ago = 180
    if last_active:
        try:
            active_dt = datetime.strptime(last_active, "%Y-%m-%d")
            days_ago = (datetime(2026, 6, 1) - active_dt).days
        except ValueError:
            pass
    f['activity_score'] = 1.0 / math.log(1 + max(days_ago, 1))
    
    f['completion_rate'] = signals.get('interview_completion_rate', 0.0)
    f['engagement_score'] = signals.get('profile_completeness_score', 0.0) / 100.0
    
    # Location Boost
    loc = profile.get('location', '').lower()
    f['location_boost'] = 1.2 if any(c in loc for c in ['pune', 'noida', 'delhi', 'ncr', 'hyderabad', 'mumbai', 'bangalore', 'bengaluru']) else 1.0
    
    return f
