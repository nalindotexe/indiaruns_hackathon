from datetime import datetime

def is_honeypot(candidate):
    """
    Check for impossible mathematical/temporal claims.
    Returns True if honeypot, False otherwise.
    """
    total_exp = candidate.get('profile', {}).get('years_of_experience', 0)
    
    # 1. Check skill duration > total experience
    skills = candidate.get('skills', [])
    for skill in skills:
        duration_months = skill.get('duration_months', 0)
        proficiency = skill.get('proficiency', '').lower()
        
        if duration_months > (total_exp * 12) + 12: # Add 1 year buffer for internships
            return True
        
        if proficiency == 'expert' and duration_months == 0:
            return True
            
    # 2. Check timeline impossibilities (start date after end date)
    career = candidate.get('career_history', [])
    for role in career:
        start = role.get('start_date')
        end = role.get('end_date')
        if start and end:
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                if start_dt > end_dt:
                    return True
            except ValueError:
                pass
                
    return False

def get_stuffer_penalty(candidate):
    """
    Detects non-engineers who just list AI keywords.
    """
    from ranker.constants import NON_ENG_TITLES
    
    title = candidate.get('profile', {}).get('current_title', '').lower()
    is_non_eng = any(nt in title for nt in NON_ENG_TITLES)
    
    skills = candidate.get('skills', [])
    ai_skills_count = sum(1 for s in skills if any(k in s.get('name', '').lower() for k in ['ai', 'ml', 'llm', 'gpt', 'model', 'data']))
    
    if is_non_eng and ai_skills_count > 5:
        return 0.05 # Massive penalty
    elif is_non_eng:
        return 0.1 # General penalty for non-eng titles
        
    return 1.0

def get_ghost_penalty(candidate):
    """
    Penalizes candidates with low engagement signals.
    """
    signals = candidate.get('redrob_signals', {})
    penalty = 1.0
    
    response_rate = signals.get('recruiter_response_rate', 1.0)
    if response_rate < 0.15:
        penalty *= 0.3
        
    last_active = signals.get('last_active_date')
    if last_active:
        try:
            # Assuming 'today' is the end of the dataset, say mid 2026 based on sample data
            # We'll use May 2026 as reference point if not specified, but let's calculate days dynamically
            # For hackathon safety, we parse it relative to a fixed date or just compute difference
            ref_date = datetime(2026, 6, 1)
            active_dt = datetime.strptime(last_active, "%Y-%m-%d")
            days_ago = (ref_date - active_dt).days
            if days_ago > 180:
                penalty *= 0.5
        except ValueError:
            pass
            
    completion_rate = signals.get('interview_completion_rate', 1.0)
    if completion_rate < 0.3:
        penalty *= 0.6
        
    return penalty

def is_hard_filtered(candidate):
    """
    Returns True if the candidate violates hard filters (e.g. pure consulting).
    """
    from ranker.constants import CONSULTING_FIRMS, NON_ENG_TITLES
    
    career = candidate.get('career_history', [])
    if not career:
        return True
        
    # Check consulting experience penalty
    has_consulting = False
    product_months = 0
    
    for role in career:
        company = role.get('company', '').lower()
        if any(cf in company for cf in CONSULTING_FIRMS):
            has_consulting = True
        else:
            product_months += role.get('duration_months', 0)
            
    # Apply penalty if they have consulting background BUT don't have >= 2 years (24 months) of product-focused experience
    if has_consulting and product_months < 24:
        return True
        
    # Check pure academic (Researcher/Postdoc without 'production' experience)
    current_title = candidate.get('profile', {}).get('current_title', '').lower()
    academic_titles = ['researcher', 'phd student', 'postdoc', 'research assistant']
    if any(at in current_title for at in academic_titles):
        has_prod = False
        for role in career:
            desc = role.get('description', '').lower()
            if 'production' in desc or 'deployed' in desc:
                has_prod = True
                break
        if not has_prod:
            return True
            
    # Hard filter non-engineers (Marketing, Sales, HR, Finance, etc.)
    non_eng = ['marketing', 'sales', 'hr', 'human resources', 'bd', 'finance', 'operations', 'recruiter', 'accountant', 'graphic designer', 'content writer', 'support', 'customer']
    if any(nt in current_title for nt in non_eng):
        return True
            
    return False
