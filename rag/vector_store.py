from pathlib import Path
from typing import Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings

GEAR_DOCS_PATH = Path(__file__).resolve().parent.parent / "data" / "gear_docs.json"
CHROMA_PERSIST_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"


class GearVectorStore:
    """Singleton vector store for trail running gear recommendations."""

    _instance: Optional["GearVectorStore"] = None

    def __new__(cls) -> "GearVectorStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self.embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
        self._load_or_create_store()

    def _load_or_create_store(self) -> None:
        if CHROMA_PERSIST_DIR.exists():
            self.store = Chroma(
                persist_directory=str(CHROMA_PERSIST_DIR),
                embedding_function=self.embeddings,
            )
            return

        documents = self._load_documents()
        if not documents:
            self.store = Chroma(
                persist_directory=str(CHROMA_PERSIST_DIR),
                embedding_function=self.embeddings,
            )
            return

        self.store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(CHROMA_PERSIST_DIR),
        )

    def _load_documents(self) -> list[Document]:
        try:
            import json

            with open(GEAR_DOCS_PATH, encoding="utf-8") as f:
                items = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: failed to load gear docs: {e}")
            return []

        documents = []
        for item in items:
            name = item.get("name", "未知装备")
            page_content = (
                f"装备名称：{name}\n"
                f"价格：{item.get('price', 0)}元\n"
                f"适用地形：{item.get('terrain', '')}\n"
                f"适用爬升：{item.get('elevation', '')}\n"
                f"特点：{item.get('description', '')}"
            )
            documents.append(
                Document(page_content=page_content, metadata={"name": name, **item})
            )

        return documents

    def search(self, query: str, k: int = 3, filter: Optional[dict] = None) -> list[Document]:
        if not hasattr(self, "store"):
            return []
        return self.store.similarity_search(query, k=k, filter=filter)

    @staticmethod
    def format_results(results: list[Document]) -> str:
        if not results:
            return "未找到相关装备信息。"
        return "\n\n---\n\n".join(doc.page_content for doc in results)


# 关键词 → category 映射
_CATEGORY_KEYWORDS: dict[str, str] = {
    "鞋": "shoe",
    "跑鞋": "shoe",
    "越野鞋": "shoe",
    "背包": "vest",
    "登山包": "vest",
    "越野包": "vest",
    "背心": "vest",
    "杖": "pole",
    "手杖": "pole",
    "登山杖": "pole",
    "手表": "watch",
    "手錶": "watch",
    "表": "watch",
    "跑表": "watch",
    "运动手表": "watch",
}


def _infer_category(query: str) -> Optional[str]:
    for keyword, category in _CATEGORY_KEYWORDS.items():
        if keyword in query:
            return category
    return None


_store: Optional[GearVectorStore] = None


def get_gear_store() -> GearVectorStore:
    global _store
    if _store is None:
        _store = GearVectorStore()
    return _store


def search_gear(query: str, k: int = 3) -> str:
    store = get_gear_store()
    category = _infer_category(query)
    filter_dict = {"category": category} if category else None
    results = store.search(query, k=k, filter=filter_dict)
    return store.format_results(results)
