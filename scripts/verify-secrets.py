from google.cloud import secretmanager
import pinecone
import os

def verify_gcp_secrets():
    """Verify access to GCP Secret Manager"""
    print("Checking GCP Secret Manager access...")
    client = secretmanager.SecretManagerServiceClient()
    
    project_id = "api-for-warp-drive"
    
    # List all secrets to verify access
    parent = f"projects/{project_id}"
    
    try:
        secrets = client.list_secrets(request={"parent": parent})
        print("✓ GCP Secret Manager access verified")
        
        # Check for specific secrets
        expected_secrets = [
            "pinecone-api-key",
            "github-token",
            "drlucyautomation-key"
        ]
        
        found_secrets = set()
        for secret in secrets:
            name = secret.name.split('/')[-1]
            found_secrets.add(name)
        
        for expected in expected_secrets:
            if expected in found_secrets:
                print(f"✓ Found secret: {expected}")
            else:
                print(f"⚠ Missing secret: {expected}")
                
    except Exception as e:
        print(f"✗ GCP Secret Manager error: {str(e)}")
        return False

def verify_pinecone_connection():
    """Verify Pinecone access and configuration"""
    print("\nChecking Pinecone connection...")
    try:
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment="gcp-us-central1-4a9f"
        )
        
        index = pinecone.Index("multilingual-e5-large")
        stats = index.describe_index_stats()
        print("✓ Pinecone connection verified")
        print(f"✓ Index stats: {stats}")
    except Exception as e:
        print(f"✗ Pinecone connection error: {str(e)}")
        return False

def verify_github_secrets():
    """Verify GitHub Actions secrets are accessible"""
    print("\nChecking GitHub Actions secrets...")
    required_secrets = [
        'PINECONE_API_KEY',
        'GCP_SA_KEY'
    ]
    
    for secret in required_secrets:
        if os.getenv(secret):
            print(f"✓ Found secret: {secret}")
        else:
            print(f"⚠ Missing secret: {secret}")

def main():
    print("=== Starting Secrets Verification ===\n")
    verify_gcp_secrets()
    verify_pinecone_connection()
    verify_github_secrets()
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    main()