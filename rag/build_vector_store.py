import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
GEAR_DOCS_PATH = BASE_DIR / "data" / "gear_docs.json"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

# 1. Embeddings 模型（ONNX 推理，无需 torch）
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

# 2. 读取装备库
with open(GEAR_DOCS_PATH, encoding="utf-8") as f:
    gear_data = json.load(f)

# 3. 转 Document
documents = []

for item in gear_data:
    content = (
        f"名称: {item['name']}\n"
        f"地形: {item['terrain']}\n"
        f"爬升: {item['elevation']}\n"
        f"价格: {item['price']}元\n"
        f"描述: {item['description']}"
    )
    doc = Document(
        page_content=content,
        metadata={
            "name": item["name"],
            "category": item["category"],
            "price": item["price"],
            "terrain": item["terrain"],
        },
    )
    documents.append(doc)

print(f"Loaded documents: {len(documents)}")

# 4. 创建向量库（持久化到 data/chroma_db）
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR),
)

print(f"Vector store created successfully at {CHROMA_DIR}")