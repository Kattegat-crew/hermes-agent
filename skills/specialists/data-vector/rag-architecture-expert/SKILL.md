---
name: rag-architecture-expert
description: "Use when designing RAG pipelines, hybrid search or rerank"
tags: [rag, retrieval, hybrid-search, bm25, rrf, reranking, chunking, vector-search]
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
