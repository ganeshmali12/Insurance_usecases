from rag_store import create_vector_store, load_vector_store

# Run this only once
create_vector_store()

db = load_vector_store()

query = "Why is low deductible better for families?"

results = db.similarity_search(query, k=2)

print("\n🔍 Retrieved Knowledge:\n")
for doc in results:
    print(doc.page_content)
    print("------")
