import pinecone
import os
import numpy as np
from datetime import datetime

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

# Connect to index
index = pinecone.Index("multilingual-e5-large")

def add_test_record():
    # Create test vector (1024 dimensions)
    test_vector = np.random.rand(1024).tolist()
    
    # Test record
    record = {
        "id": "dr-lucy-test-1",
        "values": test_vector,
        "metadata": {
            "agent": "Dr-Lucy-01",
            "endpoint_id": "6296186210691842048",
            "timestamp": datetime.now().isoformat(),
            "type": "test_record",
            "status": "active"
        }
    }
    
    try:
        # Insert into primary namespace
        index.upsert(
            vectors=[record],
            namespace="primary"
        )
        print(f"✓ Test record added successfully")
        
        # Verify record
        query_response = index.fetch(
            ids=["dr-lucy-test-1"],
            namespace="primary"
        )
        print(f"\nVerification:")
        print(f"Found record: {query_response}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    add_test_record()