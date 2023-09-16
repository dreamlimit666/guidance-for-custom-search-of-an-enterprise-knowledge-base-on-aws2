"""Milvus Retriever"""
import warnings
from typing import Any, Dict, List, Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain.embeddings.base import Embeddings
from langchain.schema import BaseRetriever, Document
from langchain.vectorstores.milvus import Milvus

# TODO: Update to MilvusClient + Hybrid Search when available


class MilvusRetriever(BaseRetriever):
    """Retriever that uses the Milvus API."""

    def __init__(
        self,
        embedding_function: Embeddings,
        collection_name: str = "LangChainCollection",
        connection_args: Optional[Dict[str, Any]] = None,
        consistency_level: str = "Session",
        search_params: Optional[dict] = None,
    ):
        self.store = Milvus(
            embedding_function,
            collection_name,
            connection_args,
            consistency_level,
        )
        self.retriever = self.store.as_retriever(search_kwargs={"param": search_params})

    def add_texts(
        self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> None:
        """Add text to the Milvus store

        Args:
            texts (List[str]): The text
            metadatas (List[dict]): Metadata dicts, must line up with existing store
        """
        self.store.add_texts(texts, metadatas)

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
        **kwargs: Any,
    ) -> List[Document]:
        return self.retriever.get_relevant_documents(
            query, run_manager=run_manager.get_child(), **kwargs
        )

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
        **kwargs: Any,
    ) -> List[Document]:
        raise NotImplementedError


def MilvusRetreiver(*args: Any, **kwargs: Any) -> MilvusRetriever:
    """Deprecated MilvusRetreiver. Please use MilvusRetriever ('i' before 'e') instead.

    Args:
        *args:
        **kwargs:

    Returns:
        MilvusRetriever
    """
    warnings.warn(
        "MilvusRetreiver will be deprecated in the future. "
        "Please use MilvusRetriever ('i' before 'e') instead.",
        DeprecationWarning,
    )
    return MilvusRetriever(*args, **kwargs)