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

# Agent details
agents = {
    "primary": {
        "Dr-Lucy-01": {
            "id": "6296186210691842048",
            "region": "us-west1",
            "memory": "96GB",
            "type": "primary_agent",
            "service_account": "drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com",
            "capabilities": ["inference", "conversation", "memory_management"]
        },
        "Dr-Lucy-02": {
            "id": "6301815710226055168",
            "region": "us-west1",
            "memory": "96GB",
            "type": "primary_agent",
            "service_account": "drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com",
            "capabilities": ["inference", "conversation", "memory_management"]
        },
        "Dr-Lucy-03": {
            "id": "3426267348149993472",
            "region": "us-west1",
            "memory": "96GB",
            "type": "primary_agent",
            "service_account": "drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com",
            "capabilities": ["inference", "conversation", "memory_management"]
        }
    },
    "super_claude": {
        "Super-Claude-1": {
            "id": "4313929473532624896",
            "region": "us-west4",
            "model": "knowledge-base-model",
            "type": "super_agent",
            "service_account": "drlucyatuomation@api-for-warp-drive.iam.gserviceaccount.com",
            "capabilities": ["knowledge_base", "advanced_inference"]
        }
    }
}

def create_agent_vector(agent_data):
    """Create a representative vector for agent metadata"""
    # Using a deterministic method to create vectors
    base_vector = np.zeros(1024)
    
    # Encode region information
    if agent_data["region"] == "us-west1":
        base_vector[0:256] = 0.1
    elif agent_data["region"] == "us-west4":
        base_vector[0:256] = 0.2

    # Encode agent type
    if agent_data["type"] == "primary_agent":
        base_vector[256:512] = 0.3
    elif agent_data["type"] == "super_agent":
        base_vector[256:512] = 0.4

    # Encode capabilities
    cap_start = 512
    for cap in agent_data["capabilities"]:
        if cap == "inference":
            base_vector[cap_start:cap_start+100] = 0.5
        elif cap == "conversation":
            base_vector[cap_start+100:cap_start+200] = 0.6
        elif cap == "memory_management":
            base_vector[cap_start+200:cap_start+300] = 0.7
        elif cap == "knowledge_base":
            base_vector[cap_start+300:cap_start+400] = 0.8
        elif cap == "advanced_inference":
            base_vector[cap_start+400:cap_start+500] = 0.9

    return base_vector.tolist()

def populate_agents():
    print("Starting agent population in Pinecone...")
    timestamp = datetime.now().isoformat()

    # Process Dr. Lucy agents
    for agent_name, agent_data in agents["primary"].items():
        vector = create_agent_vector(agent_data)
        
        index.upsert(
            vectors=[{
                "id": f"agent_{agent_data['id']}",
                "values": vector,
                "metadata": {
                    "name": agent_name,
                    "endpoint_id": agent_data["id"],
                    "region": agent_data["region"],
                    "memory": agent_data["memory"],
                    "type": agent_data["type"],
                    "service_account": agent_data["service_account"],
                    "capabilities": agent_data["capabilities"],
                    "timestamp": timestamp
                }
            }],
            namespace="primary"
        )
        print(f"Added {agent_name} to Pinecone")

    # Process Super Claude
    for agent_name, agent_data in agents["super_claude"].items():
        vector = create_agent_vector(agent_data)
        
        index.upsert(
            vectors=[{
                "id": f"agent_{agent_data['id']}",
                "values": vector,
                "metadata": {
                    "name": agent_name,
                    "endpoint_id": agent_data["id"],
                    "region": agent_data["region"],
                    "model": agent_data["model"],
                    "type": agent_data["type"],
                    "service_account": agent_data["service_account"],
                    "capabilities": agent_data["capabilities"],
                    "timestamp": timestamp
                }
            }],
            namespace="super_claude"
        )
        print(f"Added {agent_name} to Pinecone")

    print("\nVerifying records...")
    stats = index.describe_index_stats()
    print(f"Index stats after population: {stats}")

if __name__ == "__main__":
    populate_agents()