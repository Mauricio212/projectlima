#!/usr/bin/env python3
"""
Project Lima - Document Warehouse API Integration (Fixed)
Adds warehouse endpoints to existing Flask application
"""
import os
import glob
import json
from datetime import datetime
from flask import request, jsonify, abort
from functools import wraps

# Warehouse configuration
WAREHOUSE_DIR = "/home/ec2-user/project_lima/warehouse_docs"
API_KEY = "lima_warehouse_2025_secure_key"  # TODO: Move to environment variable

def require_api_key(f):
    """Decorator to require API key for warehouse endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key or api_key != API_KEY:
            abort(401, description="Valid API key required")
        return f(*args, **kwargs)
    return decorated_function

def safe_path(doc_path):
    """Validate and sanitize document path to prevent directory traversal"""
    # Remove any path traversal attempts
    doc_path = doc_path.replace('..', '').replace('//', '/')
    # Ensure path is within warehouse directory
    full_path = os.path.join(WAREHOUSE_DIR, doc_path.lstrip('/'))
    # Verify it's within warehouse bounds
    if not full_path.startswith(WAREHOUSE_DIR):
        abort(400, description="Invalid document path")
    return full_path

def register_warehouse_routes(app):
    """Register warehouse API routes with Flask app"""
    
    @app.route('/api/warehouse/docs/<path:doc_path>', methods=['GET'])
    @require_api_key
    def get_document(doc_path):
        """Retrieve document content"""
        file_path = safe_path(doc_path)
        
        # Check if file exists BEFORE try block
        if not os.path.exists(file_path):
            abort(404, description="Document not found")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "status": "success",
                "document": doc_path,
                "content": content,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            }
        except Exception as e:
            abort(500, description=f"Error reading document: {str(e)}")
    
    @app.route('/api/warehouse/docs/<path:doc_path>', methods=['POST'])
    @require_api_key
    def update_document(doc_path):
        """Update document content"""
        try:
            file_path = safe_path(doc_path)
            data = request.get_json()
            
            if not data or 'content' not in data:
                abort(400, description="Content required in request body")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data['content'])
            
            return {
                "status": "success",
                "document": doc_path,
                "message": "Document updated successfully",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            abort(500, description=f"Error updating document: {str(e)}")
    
    @app.route('/api/warehouse/list', methods=['GET'])
    @require_api_key
    def list_documents():
        """List all documents with metadata"""
        try:
            documents = []
            for root, dirs, files in os.walk(WAREHOUSE_DIR):
                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, WAREHOUSE_DIR)
                        stat = os.stat(full_path)
                        
                        documents.append({
                            "path": rel_path,
                            "size": stat.st_size,
                            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "category": rel_path.split('/')[0] if '/' in rel_path else "root"
                        })
            
            return {
                "status": "success",
                "document_count": len(documents),
                "documents": sorted(documents, key=lambda x: x['path'])
            }
        except Exception as e:
            abort(500, description=f"Error listing documents: {str(e)}")
    
    @app.route('/api/warehouse/search', methods=['GET'])
    @require_api_key
    def search_documents():
        """Search documents by content"""
        try:
            query = request.args.get('q', '').lower()
            if not query:
                abort(400, description="Query parameter 'q' required")
            
            results = []
            for root, dirs, files in os.walk(WAREHOUSE_DIR):
                for file in files:
                    if file.endswith('.md'):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, WAREHOUSE_DIR)
                        
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if query in content.lower() or query in file.lower():
                                # Find snippet containing query
                                lines = content.split('\n')
                                snippet_lines = []
                                for i, line in enumerate(lines):
                                    if query in line.lower():
                                        start = max(0, i-2)
                                        end = min(len(lines), i+3)
                                        snippet_lines = lines[start:end]
                                        break
                                
                                results.append({
                                    "path": rel_path,
                                    "title": file.replace('.md', '').replace('_', ' ').title(),
                                    "snippet": '\n'.join(snippet_lines)[:200] + "..." if snippet_lines else content[:200] + "...",
                                    "relevance": content.lower().count(query)
                                })
                        except Exception:
                            continue  # Skip files that can't be read
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance'], reverse=True)
            
            return {
                "status": "success",
                "query": query,
                "result_count": len(results),
                "results": results
            }
        except Exception as e:
            abort(500, description=f"Error searching documents: {str(e)}")

if __name__ == "__main__":
    print("Warehouse API module - import this into your Flask app")
    print("Usage: from warehouse_api import register_warehouse_routes")
    print("Then: register_warehouse_routes(app)")
