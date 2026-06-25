# List of consulting / service companies to penalize
CONSULTING_FIRMS = {
    'tcs', 'infosys', 'wipro', 'cognizant', 'accenture', 'hcl', 'capgemini',
    'tech mahindra', 'l&t', 'mindtree', 'mphasis', 'genpact', 'ibm', 'deloitte',
    'pwc', 'ey', 'kpmg'
}

# Non-engineering titles
NON_ENG_TITLES = {
    'marketing', 'sales', 'hr', 'human resources', 'bd', 'business development',
    'finance', 'operations', 'recruiter', 'accountant', 'graphic designer',
    'content writer', 'support', 'customer'
}

# Keywords for technical features
EMBEDDING_KEYWORDS = {'embedding', 'sentence-transformers', 'dense retrieval', 'vector representation', 'bge', 'e5', 'voyage', 'cross-encoder', 'semantic similarity', 'reranking'}
VECTOR_DB_KEYWORDS = {'pinecone', 'qdrant', 'milvus', 'weaviate', 'faiss', 'chromadb', 'opensearch', 'elasticsearch', 'redis', 'pgvector', 'hnswlib', 'annoy'}
EVAL_KEYWORDS = {'ndcg', 'map', 'mrr', 'a/b test', 'offline eval', 'evaluation', 'correlation', 'statistical significance', 'conversion rate'}
FINETUNING_KEYWORDS = {'fine-tuning', 'lora', 'rlhf', 'sft', 'peft', 'qlora', 'fine tune', 'finetune'}

# Production signals
PRODUCTION_SIGNALS = {'deployed', 'production', 'serving', 'latency', 'throughput', 'real-time', 'scale', 'sla', 'uptime', 'incident', 'observability', 'grafana', 'prometheus', 'distributed', 'ci/cd', 'container', 'docker', 'kubernetes', 'optimization'}

# AI/ML Role Keywords
AI_ML_ROLES = {'ai', 'ml', 'machine learning', 'data scientist', 'backend', 'software', 'engineer', 'developer'}
