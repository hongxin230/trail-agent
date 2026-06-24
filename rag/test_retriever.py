from rag.vector_store import search_gear

query = "适合100公里越野跑的登山包"
result = search_gear(query)

print("\n===== Search Result =====\n")
print(result)