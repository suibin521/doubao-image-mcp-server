# Doubao Image MCP Server

An image generation MCP server based on FastMCP framework and Volcano Engine API, supporting high-quality image generation through Doubao (doubao-seedream-3.0-t2i) model.

## 1. Features

- 🎨 **High-Quality Image Generation**: Based on Doubao seedream-3.0-t2i model, supports 2K resolution
- 🌐 **Bilingual Support**: Prompts support both Chinese and English descriptions
- 📐 **Multiple Resolutions**: Supports various resolutions from 512x512 to 2048x2048
- 🎯 **Precise Control**: Supports seed, guidance scale, watermark and other parameter controls
- 📁 **Local Storage**: Automatically downloads and saves generated images to specified directory
- 🔧 **MCP Protocol**: Fully compatible with MCP protocol, can be integrated with MCP-supported AI assistants
- 📊 **Detailed Logging**: Complete logging and error handling

## 2. Requirements

- Python >= 3.13
- Volcano Engine API Key
- Inference Endpoint Model ID

## 3. Installation & Configuration

### 3.1 Clone Project

```bash
git clone git@github.com:suibin521/doubao-image-mcp-server.git
cd doubao-image-mcp-server
```

### 3.2 Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 3.3 Configure Environment Variables

This project does not use `.env` files. All configurations are passed through the `env` field in the MCP JSON configuration file.

#### 3.3.1 Environment Variable Configuration Example
```json
"env": {
  "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
  "DOUBAO_API_KEY": "your-dev-api-key-here",
  "API_MODEL_ID": "ep-20250528154802-c4np4",
}
```

#### 3.3.2 Required Environment Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `DOUBAO_API_KEY` | Volcano Engine API Key | `ak-xxx` |
| `API_MODEL_ID` | Inference Endpoint Model ID | `ep-20250528154802-c4np4` |
| `BASE_URL` | API Base URL (optional) | `https://ark.cn-beijing.volces.com/api/v3` |

### 3.4 Get Volcano Engine API Credentials

#### 3.4.1 Register Volcano Engine Account
1. Visit [Volcano Engine Console](https://console.volcengine.com/)
2. Register and complete real-name verification
3. Navigate to "Machine Learning Platform" > "Model Inference"

![Volcano Engine Signup](images/volcengine_signup.jpg)

#### 3.4.2 Activate Model
1. In the Model Inference page, find "doubao-seedream-3.0-t2i" model
2. Click "Activate" and follow the prompts
3. Wait for activation to complete

![Model Activation](images/model_activation.jpg)

#### 3.4.3 Create Inference Endpoint
1. After model activation, click "Create Inference Endpoint"
2. Configure endpoint parameters (use default settings)
3. Wait for endpoint creation to complete
4. Copy the Endpoint ID (format: `ep-xxxxxxxxx`)

![Create Inference Endpoint](images/create_inference_endpoint.jpg)

#### 3.4.4 Create API Key
1. Navigate to "API Key Management"
2. Click "Create API Key"
3. Copy the generated API Key (format: `ak-xxxxxxxxx`)
4. **Important**: Save the API Key securely as it cannot be viewed again

![Create API Key](images/create_api_key.jpg)

## 4. Usage

### 4.1 MCP Configuration

Add the following configuration to your MCP client (e.g., Claude Desktop):

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

### 4.2 Tool Usage Examples

#### 4.2.1 Basic Call
```
Generate a beautiful sunset landscape
```

#### 4.2.2 Complete Parameters Call
```
Generate a cyberpunk city at night, size 1280x720, seed 12345, guidance scale 9.0, no watermark
```

#### 4.2.3 Specify Seed for Reproducible Results
```
Generate a cute kitten, seed 98765
```

## 5. Available Parameters

### 5.1 Image Sizes

| Size | Ratio | Description |
|------|-------|-------------|
| 512x512 | 1:1 | Small Square |
| 768x768 | 1:1 | Square |
| 1024x1024 | 1:1 | Large Square |
| 864x1152 | 3:4 | Portrait |
| 1152x864 | 4:3 | Landscape |
| 1280x720 | 16:9 | Widescreen |
| 720x1280 | 9:16 | Mobile Portrait |
| 832x1248 | 2:3 | Portrait |
| 1248x832 | 3:2 | Landscape |
| 1512x648 | 21:9 | Ultra-wide |
| 2048x2048 | 1:1 | Extra Large Square |

### 5.2 Parameter Ranges

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `seed` | -1 to 2147483647 | -1 | Random seed (-1 for random) |
| `guidance_scale` | 1.0 to 10.0 | 8.0 | Prompt adherence strength |
| `watermark` | true/false | true | Add watermark to image |
| `file_prefix` | 1-20 chars | "image" | Filename prefix |

## 6. Output

Generated images are saved to the `./images` directory with the following naming convention:
```
{file_prefix}_{timestamp}.jpg
```

Example: `image_1703123456.jpg`

## 7. Error Handling

The server provides detailed error messages for common issues:

- **Missing API Key**: Check `DOUBAO_API_KEY` environment variable
- **Invalid Model ID**: Verify `API_MODEL_ID` is correct
- **Invalid Parameters**: Check parameter ranges and formats
- **Network Issues**: Check internet connection and API endpoint
- **Quota Exceeded**: Check your Volcano Engine account balance

## 8. Development

### 8.1 Project Structure
```
doubao-image-mcp-server/
├── doubao_image_gen.py      # Core image generation module
├── doubao_mcp_server.py     # MCP server implementation
├── pyproject.toml           # Project configuration
├── README.md                # English documentation
├── README_CN.md             # Chinese documentation
├── LICENSE                  # MIT License
└── images/                  # Generated images directory
    ├── create_api_key.jpg
    ├── create_inference_endpoint.jpg
    ├── model_activation.jpg
    └── volcengine_signup.jpg
```

### 8.2 Testing

Run the server directly for testing:
```bash
python doubao_mcp_server.py
```

### 8.3 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 10. Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/suibin521/doubao-image-mcp-server/issues) page
2. Create a new issue with detailed information
3. Include error messages and configuration details

## 11. Changelog

### Version 1.0.0 (2024-06-24)
- ✨ Initial release
- 🎨 Support for Doubao image generation
- 🔧 Full MCP protocol compatibility
- 📐 Multiple resolution support
- 🎯 Advanced parameter controls
- 📁 Local image storage
- 🌐 Bilingual documentation

---

**Note**: This project is not officially affiliated with Volcano Engine or ByteDance. It's an independent implementation using their public APIs.
