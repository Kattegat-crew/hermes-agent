---
name: rag-architecture-expert
description: Retrieval-Augmented Generation (RAG) architecture, hybrid search, reciprocal rank fusion, and context reranking.
license: MIT
compatibility: opencode
---

# RAG Architecture & Vector Search

Architectural patterns for production-grade Retrieval-Augmented Generation systems.

## Key Pipeline Components
1. **Chunking Strategies**: Semantic chunking with sliding windows and metadata preservation (headers, doc source, timestamps).
2. **Hybrid Retrieval**: Combine BM25 / Sparse lexical search with Dense Vector similarity (cosine/dot-product).
3. **Reciprocal Rank Fusion (RRF)**: Fuse lexical and vector results to maximize retrieval relevance.
4. **Cross-Encoder Re-Ranking**: Use Cohere ReRank or BGE-Reranker on the top-20 retrieved chunks before prompt injection.
5. **Evaluation**: Evaluate faithfulness, answer relevance, and context precision using Ragas / TruLens.
