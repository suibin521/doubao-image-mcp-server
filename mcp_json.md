# MCP Configuration Guide

## Claude Desktop Configuration

Add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "doubao-image-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/doubao-image-mcp-server",
        "run",
        "python",
        "doubao_mcp_server.py"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "your-api-key-here",
        "API_MODEL_ID": "your-endpoint-id-here"
      }
    }
  }
}
```

## Environment Variables

- `DOUBAO_API_KEY`: Your Volcano Engine API key
- `API_MODEL_ID`: Your inference endpoint model ID
- `BASE_URL`: API base URL (optional, defaults to Volcano Engine)

## Usage Examples

### Basic Usage
```
Generate a beautiful landscape
```

### Advanced Usage
```
Generate a cyberpunk city, size 1280x720, seed 12345, guidance scale 9.0, no watermark
```
