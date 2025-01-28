import pinecone
import os
from google.cloud import aiplatform

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

def launch_dr_lucy():
    print("=== LAUNCHING DR. LUCY ===")
    
    # 1. Quick Pinecone Check
    print("\nChecking Pinecone...")
    try:
        index = pinecone.Index("multilingual-e5-large")
        print("✓ Pinecone connected")
    except Exception as e:
        print(f"✗ Pinecone error: {str(e)}")
        return False

    # 2. Verify Dr-Lucy-01
    print("\nVerifying Dr-Lucy-01...")
    ENDPOINT_ID = "6296186210691842048"
    try:
        aiplatform.init(project="api-for-warp-drive", location="us-west1")
        endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_ID)
        print(f"✓ Dr-Lucy-01 endpoint ready")
    except Exception as e:
        print(f"✗ Endpoint error: {str(e)}")
        return False

    # 3. Quick Vector Test
    print("\nTesting vector operations...")
    try:
        # Create a test vector (1024 dimensions for E5)
        test_vector = [0.1] * 1024
        
        response = index.query(
            vector=test_vector,
            top_k=1,
            namespace="primary"
        )
        print("✓ Vector operations functional")
    except Exception as e:
        print(f"✗ Vector test error: {str(e)}")
        return False

    print("\n=== DR. LUCY IS READY ===")
    return True

if __name__ == "__main__":
    success = launch_dr_lucy()
    exit(0 if success else 1)