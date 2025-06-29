# System Patterns

## System Architecture
The HK Health MCP Server is designed with a modular architecture to facilitate scalability and maintainability. The system follows a microservices-inspired approach, where each tool or data retrieval mechanism operates independently but integrates through a central MCP (Model Context Protocol) server framework.

- **Core Server**: The central component that handles incoming requests, routes them to appropriate tools, and manages responses. Built using Python, leveraging frameworks like FastAPI for asynchronous request handling.
- **Data Tools**: Individual modules responsible for fetching specific health service data (e.g., A&E waiting times, specialist waiting times). These tools are designed to be plug-and-play, allowing for easy addition of new data sources.
- **Data Sources**: Interfaces to official Hong Kong health service data endpoints, potentially using web scraping or API calls to retrieve real-time information.
- **Caching Layer**: An optional layer to store frequently accessed data temporarily, reducing load on data sources and improving response times. Redis or an in-memory cache could be utilized here.

## Key Technical Decisions
- **Python as Primary Language**: Chosen for its extensive library support, ease of development, and community resources, which are beneficial for rapid prototyping and deployment of MCP tools.
- **Asynchronous Processing**: Utilizing asynchronous programming to handle multiple data requests concurrently, ensuring the server remains responsive under load.
- **Modular Tool Design**: Each data retrieval tool is encapsulated as a separate module with a defined interface, allowing independent updates or replacements without affecting the core server.
- **Error Handling and Logging**: Comprehensive error handling at each layer to prevent system-wide failures due to individual tool issues, coupled with detailed logging for debugging and monitoring.

## Design Patterns in Use
- **Factory Pattern**: For creating data tool instances dynamically based on request types, ensuring flexibility in adding new tools without modifying core server logic.
- **Adapter Pattern**: To standardize interactions with varied data sources, converting disparate data formats into a unified structure usable by the MCP server.
- **Singleton Pattern**: Applied to the caching layer to ensure a single, shared cache instance across the application, optimizing resource usage.
- **Observer Pattern**: Potentially used for real-time data updates, where tools notify the server of new data availability, triggering cache updates or client notifications.

## Component Relationships
- **Server to Tools**: The server instantiates and delegates tasks to tools based on incoming MCP requests. Tools operate independently but report results back to the server.
- **Tools to Data Sources**: Tools interact directly with data sources, handling authentication, data parsing, and error recovery. They abstract these complexities from the server.
- **Server to Cache**: The server queries the cache before invoking tools for data retrieval, updating the cache with fresh data as needed to maintain consistency.
- **Tools to Logging**: Each tool logs its operations and errors to a centralized logging system, accessible by the server for monitoring and debugging purposes.

## Critical Implementation Paths
- **Request Handling Flow**: Incoming MCP request -> Server routing -> Cache check -> Tool invocation (if cache miss) -> Data source interaction -> Response formatting -> Cache update -> Response delivery.
- **Error Recovery Path**: Tool failure -> Error logging -> Server notification -> Fallback mechanism (if available) or error response to client.
- **Data Update Path**: Scheduled or triggered data refresh -> Tool activation -> Data source fetch -> Data validation -> Cache update -> Notification of update completion.
