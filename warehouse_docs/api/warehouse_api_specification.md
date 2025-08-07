# Document Warehouse API Specification

## New Warehouse Endpoints for AI Access

### GET /api/warehouse/docs/{doc_path}
- **Purpose**: Retrieve document content for AI assistants
- **Authentication**: API key header required
- **Parameters**: doc_path (e.g., "system/golden_rules_specification.md")
- **Response**: Document content as plain text
- **Example**: `GET /api/warehouse/docs/system/project_lima_overview.md`

### POST /api/warehouse/docs/{doc_path}
- **Purpose**: Update document content via AI assistants
- **Authentication**: API key header required
- **Parameters**: doc_path, content in request body
- **Response**: Success/failure status
- **Validation**: Content must pass quality checks

### GET /api/warehouse/search
- **Purpose**: Search documents by content or title
- **Authentication**: API key header required
- **Parameters**: query string
- **Response**: List of matching documents with snippets
- **Example**: `GET /api/warehouse/search?q=golden+rules`

### GET /api/warehouse/list
- **Purpose**: List all available documents
- **Authentication**: API key header required
- **Response**: Directory structure with document metadata
- **Format**: JSON with paths, sizes, last modified dates

## Implementation Details
- **Framework**: Flask integration with existing web_app_professional_secured.py
- **Storage**: File-based storage in warehouse_docs/ directory
- **Security**: API key validation for AI access
- **Rate Limiting**: Basic protection for personal-scale system
- **File Safety**: Path validation to prevent directory traversal

## API Key Management
- **Generation**: Secure random key generation
- **Storage**: Environment variable or secure file
- **Rotation**: Manual key rotation when needed
- **Access**: Claude and other authorized AI assistants

*Last Updated: $(date)*
*Status: Ready for Implementation*
