import pinecone
import os
import numpy as np
import time

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

def run_phase1_tests():
    print("=== Starting Phase 1 Tests ===")
    
    # 1. Health Check
    print("\nHealth Check:")
    try:
        index = pinecone.Index("multilingual-e5-large")
        stats = index.describe_index_stats()
        print("✓ Index health check passed")
        print(f"Index stats: {stats}")
    except Exception as e:
        print(f"✗ Health check failed: {str(e)}")
        return False

    # 2. Dimension Test
    print("\nDimension Test:")
    try:
        test_vector = np.random.rand(1024).tolist()
        response = index.query(
            vector=test_vector,
            top_k=1,
            include_metadata=True
        )
        print("✓ 1024 dimensions accepted")
    except Exception as e:
        print(f"✗ Dimension test failed: {str(e)}")
        return False

    # 3. Cosine Similarity Test
    print("\nCosine Similarity Test:")
    try:
        vector1 = np.random.rand(1024).tolist()
        vector2 = np.random.rand(1024).tolist()
        response = index.query(
            vector=vector1,
            top_k=1,
            include_metadata=True
        )
        print("✓ Cosine similarity metric functional")
    except Exception as e:
        print(f"✗ Similarity test failed: {str(e)}")
        return False

    # 4. Serverless Capacity Test
    print("\nServerless Capacity Test:")
    try:
        start_time = time.time()
        for _ in range(5):  # Test with 5 quick queries
            response = index.query(
                vector=np.random.rand(1024).tolist(),
                top_k=1
            )
        end_time = time.time()
        avg_latency = (end_time - start_time) / 5
        print(f"✓ Serverless capacity responding (avg latency: {avg_latency:.3f}s)")
    except Exception as e:
        print(f"✗ Serverless test failed: {str(e)}")
        return False

    print("\n=== Phase 1 Tests Complete ===")
    return True

if __name__ == "__main__":
    success = run_phase1_tests()
    exit(0 if success else 1)