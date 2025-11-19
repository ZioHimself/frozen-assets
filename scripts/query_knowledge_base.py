#!/usr/bin/env python3
"""
Example script demonstrating how to query the Frozen Assets knowledge base.
Supports multiple backends: LlamaIndex, LangChain, or simple text search.
"""

import json
import os
import sys
from pathlib import Path

# Configuration
KNOWLEDGE_BASE_DIR = "knowledge_base"
METADATA_FILE = "knowledge_base/metadata.json"

def load_metadata():
    """Load the metadata JSON file."""
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def simple_search(query, metadata):
    """Simple keyword-based search through documents."""
    query_lower = query.lower()
    results = []
    
    for doc in metadata['documents']:
        if doc['status'] != 'success':
            continue
        
        # Search in title and description
        title = doc.get('title', '').lower()
        desc = doc.get('short_description', '').lower()
        
        if query_lower in title or query_lower in desc:
            results.append({
                'title': doc['title'],
                'filename': doc['filename'],
                'type': doc['type'],
                'authority': doc.get('authority', 'N/A'),
                'description': doc.get('short_description', 'N/A'),
                'url': doc['url']
            })
    
    return results

def search_with_llamaindex(query):
    """Search using LlamaIndex (if installed)."""
    try:
        from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
        from llama_index.core.settings import Settings
        
        print("🔍 Using LlamaIndex for semantic search...")
        
        # Load documents
        documents = SimpleDirectoryReader(KNOWLEDGE_BASE_DIR, 
                                         exclude=['metadata.json', 'README.md']).load_data()
        
        # Create index
        index = VectorStoreIndex.from_documents(documents)
        
        # Create query engine
        query_engine = index.as_query_engine()
        
        # Query
        response = query_engine.query(query)
        
        return str(response)
        
    except ImportError:
        print("❌ LlamaIndex not installed. Install with: pip install llama-index")
        return None

def search_with_langchain(query):
    """Search using LangChain (if installed)."""
    try:
        from langchain.document_loaders import DirectoryLoader
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import Chroma
        from langchain.chains import RetrievalQA
        from langchain.llms import OpenAI
        
        print("🔍 Using LangChain for semantic search...")
        
        # Load documents
        loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, 
                                glob="**/*.{pdf,html}",
                                show_progress=True)
        documents = loader.load()
        
        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(documents, embeddings)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        
        # Query
        response = qa_chain.run(query)
        
        return response
        
    except ImportError:
        print("❌ LangChain not installed. Install with: pip install langchain chromadb openai")
        return None

def main():
    """Main function."""
    print("=" * 70)
    print("📚 Frozen Assets Knowledge Base Query Tool")
    print("=" * 70)
    
    # Check if knowledge base exists
    if not os.path.exists(METADATA_FILE):
        print("\n❌ Knowledge base not found!")
        print("   Run: python3 download_articles.py")
        sys.exit(1)
    
    # Load metadata
    metadata = load_metadata()
    total_docs = metadata['successful_downloads']
    print(f"\n✅ Knowledge base loaded: {total_docs} documents")
    
    # Get query from command line or prompt
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        print("\n" + "=" * 70)
        query = input("Enter your question: ").strip()
    
    if not query:
        print("❌ No query provided")
        sys.exit(1)
    
    print(f"\n🔍 Searching for: '{query}'")
    print("=" * 70)
    
    # Try advanced search first (LlamaIndex or LangChain)
    result = None
    
    # Try LlamaIndex
    if os.environ.get('USE_LLAMAINDEX', '').lower() in ['1', 'true', 'yes']:
        result = search_with_llamaindex(query)
    
    # Try LangChain
    elif os.environ.get('USE_LANGCHAIN', '').lower() in ['1', 'true', 'yes']:
        result = search_with_langchain(query)
    
    # Fall back to simple search
    if result is None:
        print("🔍 Using simple keyword search...")
        print("   (For semantic search, install llama-index or langchain)")
        print()
        
        results = simple_search(query, metadata)
        
        if not results:
            print("❌ No results found")
            print("\nTry:")
            print("  - Different keywords")
            print("  - Broader search terms")
            print("  - Check available documents in knowledge_base/README.md")
        else:
            print(f"✅ Found {len(results)} matching documents:\n")
            
            for i, doc in enumerate(results, 1):
                print(f"{i}. {doc['title']}")
                print(f"   Type: {doc['type']}")
                print(f"   Authority: {doc['authority']}")
                print(f"   File: {doc['filename']}")
                print(f"   Description: {doc['description']}")
                print(f"   URL: {doc['url']}")
                print()
    else:
        print("\n📝 Answer:")
        print("=" * 70)
        print(result)
        print("=" * 70)
    
    print("\n✨ Search complete!")

if __name__ == "__main__":
    main()

