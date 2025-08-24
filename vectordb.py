# %% imports and init
import chromadb
import json

db_path = "./db/chromadb"

# %% insert data
chroma_client = chromadb.PersistentClient(db_path)

eso_sets_collection = chroma_client.get_or_create_collection(name="eso-sets")
with open("./all_sets_raw.json", "r") as raw:
    raw_json = json.load(raw)
    eso_sets_collection.add(
        ids=list(raw_json.keys()),
        documents=list(raw_json.values()),
    )

eso_skills_collection = chroma_client.get_or_create_collection(name="eso-skills")
with open("./all_skills_raw.json", "r") as s:
    skills_json = json.load(s)
    eso_skills_collection.add(
        ids=list(skills_json.keys()),
        documents=list(skills_json.values()),
    )

eso_cp_collection = chroma_client.get_or_create_collection(name="eso-cp")
with open("./all_cp_raw.json", "r") as s:
    cp_json = json.load(s)
    eso_cp_collection.add(
        ids=list(cp_json.keys()),
        documents=list(cp_json.values()),
    )

# %%
collection = chroma_client.get_or_create_collection(name="eso-sets")
results = collection.query(
    query_texts=["damage over time"], # Chroma will embed this for you
    n_results=10 # how many results to return
)

# %% 
skills = chroma_client.get_or_create_collection(name="eso-skills")
skills.query(
    query_texts=["status effect"], # Chroma will embed this for you
    n_results=10 # how many results to return
)

# %%
cp = chroma_client.get_or_create_collection(name="eso-cp")
cp.query(
    query_texts=["status effect"], # Chroma will embed this for you
    n_results=10 # how many results to return
)

# %%
