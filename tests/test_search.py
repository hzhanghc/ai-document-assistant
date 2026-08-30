from app.search import search_documents


query = "What is the definition of machine learning according to Tom Mitchell?"

results = search_documents(
    query,
    n_results=5
)


print(f"\nQuery: {query}")
print(f"Results found: {len(results)}")


for index, result in enumerate(results, start=1):

    print(f"\n{'=' * 60}")
    print(f"Result {index}")
    print(f"Page: {result['page']}")
    print(f"Distance: {result['distance']:.4f}")
    print(f"{'=' * 60}")

    print(result["text"][:1000])