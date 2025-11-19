# Frozen Assets Knowledge Base

This directory contains downloaded articles and documents from the Frozen Assets database for AI indexing and knowledge base purposes.

## Contents

- **18 successfully downloaded documents** (3 PDFs, 15 HTML files)
- **metadata.json** - Complete metadata for all documents including:
  - Document titles and descriptions
  - URLs and file types
  - Download timestamps
  - File sizes and content types
  - Success/failure status

## Document Types

### Legal Documents
- REPO Act - US Legislation (PDF, 467 KB)
- Research on confiscation perspectives
- Legal options analysis

### Policy & Analysis
- World Bank Ukraine Reconstruction Assessment
- Nobel laureates' joint appeal
- France legal aspects analysis
- EU solidarity action papers

### News & Opinion
- Articles from various sources on Russian asset confiscation
- Reparation loan analysis
- Political arguments and commentary

## File Naming

Files are named based on their titles with:
- Special characters removed
- Spaces replaced with underscores
- Maximum 100 character length
- Appropriate file extensions (.pdf, .html)

## Usage for AI/LLM

This knowledge base can be used for:
- RAG (Retrieval-Augmented Generation) systems
- Document Q&A systems
- Legal research and analysis
- Policy recommendation systems

### Recommended Tools

- **LlamaIndex** or **LangChain** for document indexing
- **ChromaDB** or **Pinecone** for vector storage
- **OpenAI Embeddings** or similar for semantic search

### Example Usage with LlamaIndex

```python
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex

# Load documents
documents = SimpleDirectoryReader('knowledge_base').load_data()

# Create index
index = GPTVectorStoreIndex.from_documents(documents)

# Query
response = index.query("What are the legal arguments for confiscating Russian assets?")
print(response)
```

## Failed Downloads

6 documents failed to download due to:
- 403 Forbidden errors (EU Council, Euroclear)
- 404 Not Found (European Parliament Resolution)
- Connection timeouts
- DNS resolution failures

These can be manually obtained if needed. See `metadata.json` for full details.

## Updating

To refresh the knowledge base with latest articles:

```bash
python3 download_articles.py
```

This will:
- Fetch latest data from the Google Sheets API
- Download new or updated documents
- Update metadata.json

## Last Updated

Generated: 2025-11-15

Total Documents in Database: 993  
Valid Documents: 24  
Successfully Downloaded: 18 (75%)

