import pinecone
import os
import numpy as np

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

# Connect to the index
index = pinecone.Index("multilingual-e5-large")

def test_namespace_query(namespace="primary"):
    # Create a test vector matching E5 dimensions
    query_vector = np.random.rand(1024).tolist()
    
    try:
        # Execute query
        response = index.query(
            namespace=namespace,
            vector=query_vector,
            top_k=2,
            include_values=True,
            include_metadata=True,
            filter={
                "type": {"$eq": "test"}
            }
        )
        
        print(f"\nQuery Results for namespace {namespace}:")
        print(response)
        
        # Test specific metadata query
        response_with_filter = index.query(
            namespace=namespace,
            vector=query_vector,
            top_k=2,
            include_values=True,
            include_metadata=True,
            filter={
                "source": {"$eq": "initialization"}
            }
        )
        
        print(f"\nFiltered Query Results for {namespace}:")
        print(response_with_filter)
        
    except Exception as e:
        print(f"Error querying namespace {namespace}: {str(e)}")

def main():
    # Test each namespace
    for namespace in ["primary", "secondary", "tertiary"]:
        print(f"\nTesting queries for {namespace}...")
        test_namespace_query(namespace)

if __name__ == "__main__":
    main()