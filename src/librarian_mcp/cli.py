"""
CLI entry point for `librarian-mcp` console script.

Thin wrapper — delegates to the FastMCP server.
"""


def main() -> None:
    """Run the Librarian MCP server on stdio transport."""
    from librarian_mcp.server import main as serve
    serve()


if __name__ == "__main__":
    main()
