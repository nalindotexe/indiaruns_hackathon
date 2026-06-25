def generate_reasoning(candidate, features):
    parts = []
    profile = candidate.get('profile', {})
    years = profile.get('years_of_experience', 0)
    title = profile.get('current_title', 'Engineer')
    
    career = candidate.get('career_history', [])
    last_co = career[0].get('company', 'Unknown') if career else 'Unknown'

    if features['embedding_score'] > 0.5:
        parts.append(f"{years}y exp with strong embeddings/retrieval at {last_co}")
    else:
        parts.append(f"{years}y exp {title} at {last_co}")
        
    if features['vector_db_score'] > 0.5:
        parts.append("hands-on with vector databases")
        
    if features['product_co_ratio'] > 0.8:
        parts.append("strong product-company background")
        
    if features.get('production_signal', 0) > 0:
        parts.append("proven production deployment experience")
        
    # Behavioral callouts
    response_rate = candidate.get('redrob_signals', {}).get('recruiter_response_rate', 0)
    if response_rate > 0.8:
        parts.append(f"highly responsive ({int(response_rate*100)}% reply rate)")
        
    if candidate.get('redrob_signals', {}).get('github_activity_score', -1) > 50:
        parts.append("strong open-source/GitHub signal")

    if not parts:
        parts.append(f"{years}y exp {title} matching baseline criteria")

    # Combine 2-3 parts into a sentence
    return ". ".join(parts[:3]).capitalize() + "."
