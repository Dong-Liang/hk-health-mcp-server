# Tech Context

## Technologies Used
- **Python**: The primary programming language for the HK Health MCP Server, chosen for its versatility, extensive libraries, and strong community support.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. Used for creating the MCP server endpoints.
- **Pydantic**: For data validation and settings management using Python type annotations, ensuring robust input handling for MCP tools.
- **HTTPX**: An asynchronous HTTP client for Python, used for making requests to fetch data from health service sources.
- **BeautifulSoup** or **Scrapy**: Potential libraries for web scraping if direct API access to health data is unavailable, allowing extraction of data from HTML pages.
- **Redis**: Considered for caching frequently accessed data to reduce load on external data sources and improve response times.
- **pytest**: For writing and running tests to ensure the reliability and correctness of the MCP server tools and core functionality.

## Development Setup
- **Environment**: Development is conducted in a virtual environment (venv) to isolate project dependencies and avoid conflicts with system-wide packages.
- **IDE**: Visual Studio Code is used for development, providing integrated debugging, linting, and version control features.
- **Version Control**: Git for tracking changes, with repositories potentially hosted on platforms like GitHub for collaboration and backup.
- **Dependency Management**: Managed via `pyproject.toml` using tools like Poetry or pip for installing and updating project dependencies.
- **Testing**: Local testing with pytest, running unit and integration tests to validate tool functionality and server responses before deployment.

## Technical Constraints
- **Data Source Availability**: Dependent on the reliability and update frequency of official Hong Kong health service data sources. Potential delays or downtime in these sources could affect data timeliness.
- **Rate Limiting**: Possible restrictions on request frequency to data sources, necessitating efficient caching strategies and request batching.
- **Data Format Variability**: Health data may be presented in inconsistent formats across different sources, requiring robust parsing and normalization logic.
- **Scalability**: Must design the server to handle increased load as more applications integrate with the MCP server, potentially requiring load balancing or distributed architectures in the future.
- **Security**: Need to ensure data transmission is secure (HTTPS), and consider authentication mechanisms for API access to prevent abuse.

## Dependencies
- **Internal**: The project structure includes separate modules for each MCP tool (e.g., `tool_aed_waiting.py`, `tool_specialist_waiting_time_by_cluster.py`), which depend on a central app module (`app.py`) for routing and initialization.
- **External**: Reliance on third-party libraries as listed under Technologies Used. These are specified in `pyproject.toml` for version control and reproducibility.
- **Data Sources**: Dependency on external health service websites or APIs for raw data, which are subject to change in structure or availability.

## Tool Usage Patterns
- **MCP Tool Development**: Each tool is developed as a standalone module with a clear input schema and output format, registered with the MCP server for dynamic invocation.
- **Data Fetching**: Tools typically follow a pattern of request -> parse -> validate -> format, ensuring data integrity before returning results to the server.
- **Error Handling**: Tools are designed to catch and log exceptions, returning meaningful error messages to the server for client communication.
- **Testing**: Each tool includes corresponding test files (e.g., `test_tool_aed_waiting.py`) to verify functionality across various scenarios, including edge cases and failures.
- **Documentation**: Inline code comments and docstrings are used for tool implementation details, while high-level usage and integration are documented in the Memory Bank files.
