<<<<<<< HEAD
{
  "mcpServers": {
    "doubao_image_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/WorkSpace/mcp_server/doubao_image_mcp_server",
        "run",
        "main.py"
      ]
    }
  }
}

{
  "mcpServers": {
    "doubao_image_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/WorkSpace/mcp_server/doubao_image_mcp_server",
        "run",
=======
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
>>>>>>> c9df404282c86290a94da00488a28f812235bd54
        "doubao_mcp_server.py"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
<<<<<<< HEAD
        "DOUBAO_API_KEY": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "API_MODEL_ID": "ep-20250528154802-c4np4",
        "IMAGE_SAVE_DIR": "C:/WorkSpace/mcp_server/mcp-server-docs/images"
=======
        "DOUBAO_API_KEY": "your-api-key-here",
        "API_MODEL_ID": "your-endpoint-id-here"
>>>>>>> c9df404282c86290a94da00488a28f812235bd54
      }
    }
  }
}
<<<<<<< HEAD

{
  "mcpServers": {
    "doubao_image_mcp_server_test": {
      "command": "uvx",
      "args": [
        "--index-url", "https://test.pypi.org/simple/",
        "--extra-index-url", "https://pypi.org/simple/",
        "doubao-image-mcp-server"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "API_MODEL_ID": "ep-20250528154802-c4np4",
        "IMAGE_SAVE_DIR": "C:/WorkSpace/mcp_server/doubao_image_mcp_server/images"
      }
    }
  }
}

{
  "mcpServers": {
    "doubao_image_mcp_server_test": {
      "command": "uvx",
      "args": [
        "doubao-image-mcp-server"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "API_MODEL_ID": "ep-20250528154802-c4np4",
        "IMAGE_SAVE_DIR": "C:/WorkSpace/mcp_server/doubao_image_mcp_server/images"
      }
    }
  }
}
=======
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
>>>>>>> c9df404282c86290a94da00488a28f812235bd54
