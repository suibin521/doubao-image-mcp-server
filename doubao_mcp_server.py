#!/usr/bin/env python3
"""
Doubao Image MCP Server

A Model Context Protocol (MCP) server for image generation using the Doubao API.
This server provides a standardized interface for AI assistants to generate
high-quality images through the Volcano Engine's Doubao model.

Author: suibin521
Version: 1.0.0
License: MIT
"""

import os
import asyncio
from typing import Any, Sequence
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource
)
from pydantic import AnyUrl
from doubao_image_gen import DoubaoImageGenerator


# Server configuration
server = Server("doubao-image-mcp-server")

# Global generator instance
generator = None


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """
    List available resources.
    
    Returns:
        List of available resources (currently empty)
    """
    return []


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific resource.
    
    Args:
        uri: Resource URI
        
    Returns:
        Resource content
    """
    return f"Resource content for {uri}"


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools.
    
    Returns:
        List of available tools for image generation
    """
    return [
        Tool(
            name="doubao_generate_image",
            description="""Generate image using Doubao API

This function is the core tool function of the MCP server, used to call Doubao (Volcano Engine) API to generate images.
The function validates input parameters, calls the underlying image generator, and returns formatted result information.

使用豆包API生成图像

这个函数是MCP服务器的核心工具函数，用于调用豆包（火山方舟）API生成图像。
函数会验证输入参数，调用底层的图像生成器，并返回格式化的结果信息。

Args:
    prompt (str): Prompt for image generation, supports Chinese and English descriptions, cannot be empty
                 用于生成图像的提示词，支持中英文描述，不能为空
    size (str): Image width and height in pixels, must be one of predefined resolutions, default "1024x1024"
               生成图像的宽高像素，必须是预定义的分辨率之一，默认"1024x1024"
    seed (int): Random seed for controlling model generation randomness, if not specified, a random number will be auto-generated, range -1 to 2147483647
               随机数种子，用于控制模型生成内容的随机性，如果不指定则自动生成随机数，范围-1到2147483647
    guidance_scale (float): Consistency between model output and prompt, higher values follow prompt more strictly, range 1.0 to 10.0
                           模型输出结果与prompt的一致程度，值越大越严格遵循提示词，范围1.0到10.0
    watermark (bool): Whether to add watermark to generated image, default True
                     是否在生成的图片中添加水印，默认True
    file_prefix (Optional[str]): Image filename prefix, only English letters, numbers, underscores and hyphens allowed, max 20 characters
                                图片文件名前缀，仅限英文字母、数字、下划线和连字符，长度不超过20个字符

Returns:
    List[TextContent]: Text content list containing image generation result information, including save path, resolution, prompt, etc.
                      包含图像生成结果信息的文本内容列表，包括保存路径、分辨率、提示词等信息

Raises:
    ValueError: Raised when input parameters do not meet requirements, such as empty prompt, invalid resolution, incorrect file prefix format, etc.
               当输入参数不符合要求时抛出，如提示词为空、分辨率无效、文件前缀格式错误等
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt for image generation, supports Chinese and English descriptions",
                        "title": "Prompt"
                    },
                    "size": {
                        "type": "string",
                        "description": """Image width and height in pixels, available values:
• 512x512: 512x512 (1:1 Small Square)
• 768x768: 768x768 (1:1 Square)
• 1024x1024: 1024x1024 (1:1 Large Square)
• 864x1152: 864x1152 (3:4 Portrait)
• 1152x864: 1152x864 (4:3 Landscape)
• 1280x720: 1280x720 (16:9 Widescreen)
• 720x1280: 720x1280 (9:16 Mobile Portrait)
• 832x1248: 832x1248 (2:3)
• 1248x832: 1248x832 (3:2)
• 1512x648: 1512x648 (21:9 Ultra-wide)
• 2048x2048: 2048x2048 (1:1 Extra Large Square)""",
                        "default": "1024x1024",
                        "title": "Size"
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for controlling model generation randomness, if not specified, a random number will be auto-generated",
                        "default": -1,
                        "minimum": -1,
                        "maximum": 2147483647,
                        "title": "Seed"
                    },
                    "guidance_scale": {
                        "type": "number",
                        "description": "Consistency between model output and prompt, higher values follow prompt more strictly",
                        "default": 8,
                        "minimum": 1,
                        "maximum": 10,
                        "title": "Guidance Scale"
                    },
                    "watermark": {
                        "type": "boolean",
                        "description": "Whether to add watermark to generated images",
                        "default": True,
                        "title": "Watermark"
                    },
                    "file_prefix": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "Image filename prefix (letters, numbers, underscores only), max 20 characters",
                        "default": None,
                        "title": "File Prefix"
                    }
                },
                "required": ["prompt"],
                "title": "doubao_generate_imageArguments"
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls.
    
    Args:
        name: Tool name
        arguments: Tool arguments
        
    Returns:
        List of text content with results
    """
    if name == "doubao_generate_image":
        return await handle_generate_image(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_generate_image(
    prompt: str,
    size: str = "1024x1024",
    seed: int = -1,
    guidance_scale: float = 8.0,
    watermark: bool = True,
    file_prefix: str = None
) -> list[TextContent]:
    """
    Handle image generation requests.
    
    Args:
        prompt: Image generation prompt
        size: Image size
        seed: Random seed
        guidance_scale: Guidance scale
        watermark: Whether to add watermark
        file_prefix: Filename prefix
        
    Returns:
        List of text content with generation results
    """
    global generator
    
    if generator is None:
        return [TextContent(
            type="text",
            text="❌ Error: Image generator not initialized. Please check your environment variables."
        )]
    
    try:
        # Validate file prefix
        if file_prefix:
            if len(file_prefix) > 20:
                raise ValueError("File prefix must be 20 characters or less")
            if not file_prefix.replace('_', '').replace('-', '').isalnum():
                raise ValueError("File prefix can only contain letters, numbers, underscores and hyphens")
        
        # Set default save directory
        save_dir = os.path.join(os.getcwd(), "images")
        
        # Generate and save image
        result = generator.generate_and_save(
            prompt=prompt,
            save_dir=save_dir,
            filename_prefix=file_prefix or "image",
            size=size,
            seed=seed,
            guidance_scale=guidance_scale,
            watermark=watermark
        )
        
        # Format response
        if result.get("local_path"):
            response_text = f"""🎨 Image generation successful!

📁 Save path: {result['local_path']}
📐 Resolution: {result['size']}
🎯 Prompt: {result['original_prompt']}
🎲 Seed: {result['seed']}

📊 Generation info:
  • model: {result['model']}
  • created: {result['created']}
  • seed: {result['seed']}
  • guidance_scale: {result['guidance_scale']}
  • watermark: {result['watermark']}
  • size: {result['size']}
  • original_url: {result['url']}
"""
        else:
            response_text = f"""⚠️ Image generation completed but download failed!

🌐 Image URL: {result['url']}
📐 Resolution: {result['size']}
🎯 Prompt: {result['original_prompt']}
🎲 Seed: {result['seed']}

📊 Generation info:
  • model: {result['model']}
  • created: {result['created']}
  • seed: {result['seed']}
  • guidance_scale: {result['guidance_scale']}
  • watermark: {result['watermark']}
  • size: {result['size']}
"""
        
        return [TextContent(type="text", text=response_text)]
        
    except Exception as e:
        error_text = f"❌ Image generation failed: {str(e)}"
        return [TextContent(type="text", text=error_text)]


async def main():
    """
    Main function to run the MCP server.
    """
    global generator
    
    # Get configuration from environment variables
    api_key = os.getenv("DOUBAO_API_KEY")
    base_url = os.getenv("BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    model_id = os.getenv("API_MODEL_ID")
    
    if not api_key:
        print("❌ Error: DOUBAO_API_KEY environment variable is required")
        return
    
    if not model_id:
        print("❌ Error: API_MODEL_ID environment variable is required")
        return
    
    # Initialize generator
    try:
        generator = DoubaoImageGenerator(api_key, base_url, model_id)
        print("✅ Doubao Image Generator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize generator: {str(e)}")
        return
    
    # Run server
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="doubao-image-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
