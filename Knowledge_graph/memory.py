from mem0 import Memory

from dotenv import load_dotenv

load_dotenv()

config = {
    "version": "v1.1", 
    "embedder": {
        "provider": "google", 
        "config": {"api_key":  OPENAI_API_KEY, "model":"text-embedding-3-small"}
    },
    "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"},
    
    "vector_store":{
        "provider": "qdrant", 
        "config": {
            "host": QUADRANT_HOST, 
            "port": 6333,
        },
    },
    "graph_store": {
        "provider": "neo4j", 
        "config": {"url": NEO4J_URL, "username": neo4j_username, "password": neo4j_password},

    }
            
}
