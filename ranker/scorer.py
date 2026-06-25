def compute_score(f, ghost_penalty, honeypot_multiplier, stuffer_penalty):
    technical = (
        f['embedding_score']      * 0.35 +
        f['vector_db_score']      * 0.25 +
        f['finetuning_score']     * 0.25 +
        f['eval_framework_score'] * 0.15
    )

    experience = (
        f['total_exp_score']   * 0.30 +
        f['ai_exp_score']      * 0.40 +
        f['product_co_ratio']  * 0.30
    )

    shipper = (
        f['production_signal'] * 0.50 +
        f['github_signal']     * 0.25 +
        f['startup_bonus']     * 0.25
    )

    behavioral = (
        f['response_rate']      * 0.35 +
        f['activity_score']     * 0.30 +
        f['completion_rate']    * 0.20 +
        f['engagement_score']   * 0.15
    )

    raw_score = (
        technical  * 0.45 +  # Increased weight on technical as per strategy
        experience * 0.25 +
        shipper    * 0.20 +
        behavioral * 0.10
    )
    
    # Apply location boost
    raw_score *= f.get('location_boost', 1.0)

    # Apply trap penalties
    return raw_score * ghost_penalty * honeypot_multiplier * stuffer_penalty
