import pinecone
import os
import time
from datetime import datetime

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

# Connect to the index
index = pinecone.Index("multilingual-e5-large")

def init_namespace(namespace, endpoint_id):
    """Initialize a namespace with test vectors"""
    timestamp = datetime.now().isoformat()
    
    # Initial test vectors
    vectors = [
        {
            "id": f"{namespace}-test-1",
            "values": [0.1] * 1024,  # Match E5 dimensions
            "metadata": {
                "source": "initialization",
                "type": "test",
                "timestamp": timestamp,
                "endpoint_id": endpoint_id
            }
        },
        {
            "id": f"{namespace}-test-2",
            "values": [0.2] * 1024,
            "metadata": {
                "source": "initialization",
                "type": "test",
                "timestamp": timestamp,
                "endpoint_id": endpoint_id
            }
        }
    ]
    
    # Upsert vectors
    index.upsert(vectors=vectors, namespace=namespace)
    
    # Verify upsert
    time.sleep(1)  # Allow for propagation
    stats = index.describe_index_stats()
    print(f"Namespace {namespace} initialized.")
    print(f"Stats: {stats}")

def main():
    namespaces = [
        ("primary", "6296186210691842048"),
        ("secondary", "6301815710226055168"),
        ("tertiary", "3426267348149993472")
    ]
    
    for namespace, endpoint_id in namespaces:
        print(f"\nInitializing {namespace}...")
        init_namespace(namespace, endpoint_id)
        
if __name__ == "__main__":
    main()