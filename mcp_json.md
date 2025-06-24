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
        "doubao_mcp_server.py"
      ],
      "env": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "API_MODEL_ID": "ep-20250528154802-c4np4",
        "IMAGE_SAVE_DIR": "C:/WorkSpace/mcp_server/mcp-server-docs/images"
      }
    }
  }
}

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