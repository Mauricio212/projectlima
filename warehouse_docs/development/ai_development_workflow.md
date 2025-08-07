# AI Development Workflow

## Current Development Process
1. **Human Analysis** - Problem identification and requirements
2. **AI Implementation** - Claude/ChatGPT code generation
3. **Human Testing** - Manual execution and validation
4. **Iterative Refinement** - AI fixes based on test results
5. **Production Deployment** - Manual deployment to EC2

## AI Assistant Coordination
- **Claude**: Primary development lead, system analysis, integration
- **ChatGPT**: Secondary support, testing, validation when needed
- **Human**: Execution interface, final approval, deployment

## Development Environment
- **Server**: EC2 52.200.101.103
- **Environment**: Python 3.9 virtual environment (lima_env)
- **Framework**: Flask web application
- **Database**: SQLite with plans for PostgreSQL migration
- **Process**: Gunicorn WSGI server

## Quality Standards
- All code must pass manual testing
- Zero placeholders in production code
- Integration safety validation required
- Step-by-step execution with human verification

## File Management
- Working files in `/home/ec2-user/project_lima/`
- Backup systems for critical components
- Version control through file naming conventions

*Last Updated: $(date)*
*Status: Active Development Process*
