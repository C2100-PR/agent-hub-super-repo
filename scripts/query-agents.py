import pinecone
import os

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment="gcp-us-central1-4a9f"
)

index = pinecone.Index("multilingual-e5-large")

def query_agents():
    print("=== Querying Agent Records ===\n")
    
    # Query Dr. Lucy agents
    print("Dr. Lucy Agents (Primary Namespace):")
    for prefix in ["Dr-Lucy-01", "Dr-Lucy-02", "Dr-Lucy-03"]:
        response = index.query(
            vector=[0.1] * 1024,  # Test vector
            top_k=1,
            namespace="primary",
            filter={
                "name": {"$eq": prefix}
            },
            include_metadata=True
        )
        if response.matches:
            match = response.matches[0]
            print(f"\n{prefix} Details:")
            print(f"  Endpoint ID: {match.metadata['endpoint_id']}")
            print(f"  Region: {match.metadata['region']}")
            print(f"  Memory: {match.metadata['memory']}")
            print(f"  Type: {match.metadata['type']}")
            print(f"  Capabilities: {', '.join(match.metadata['capabilities'])}")
    
    # Query Super Claude
    print("\nSuper Claude Agents:")
    response = index.query(
        vector=[0.2] * 1024,  # Test vector
        top_k=1,
        namespace="super_claude",
        include_metadata=True
    )
    if response.matches:
        match = response.matches[0]
        print(f"\nSuper Claude 1 Details:")
        print(f"  Endpoint ID: {match.metadata['endpoint_id']}")
        print(f"  Region: {match.metadata['region']}")
        print(f"  Model: {match.metadata['model']}")
        print(f"  Type: {match.metadata['type']}")
        print(f"  Capabilities: {', '.join(match.metadata['capabilities'])}")
    
    # Get total record count
    stats = index.describe_index_stats()
    print(f"\nTotal records in index: {stats.total_vector_count}")

if __name__ == "__main__":
    query_agents()