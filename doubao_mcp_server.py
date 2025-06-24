#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doubao Image Generation MCP Server
Implements image generation functionality based on FastMCP framework and Volcano Engine API

豆包图像生成MCP服务器
基于FastMCP框架和火山方舟API实现图像生成功能
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from pydantic import Field

from doubao_image_gen import DoubaoImageGenerator

# Function for outputting debug information to stderr
# 用于将调试信息输出到stderr的函数
def debug_print(*args, **kwargs):
    """Output debug information to stderr
    将调试信息输出到stderr"""
    print(*args, file=sys.stderr, **kwargs)

# Setup logging system
# 设置日志系统
def setup_logging():
    """Setup logging system, output logs to file and stderr
    设置日志系统，将日志输出到文件和stderr"""
    # Create log directory
    # 创建log文件夹
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    
    # Configure log format
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure file logging
    # 配置文件日志
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / 'doubao_mcp_server.log', encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    return logging.getLogger(__name__)

# Initialize logging
# 初始化日志
logger = setup_logging()

# Initialize MCP server
# 初始化MCP服务器
mcp = FastMCP("Doubao Image Generation MCP Service")

# Get configuration from environment variables (module-level check)
# 从环境变量获取配置（模块级检查）
BASE_URL = os.getenv("BASE_URL", "").strip().strip('`') if os.getenv("BASE_URL") else None
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "").strip() if os.getenv("DOUBAO_API_KEY") else None
API_MODEL_ID = os.getenv("API_MODEL_ID", "").strip() if os.getenv("API_MODEL_ID") else None
IMAGE_SAVE_DIR = os.getenv("IMAGE_SAVE_DIR", "").strip() if os.getenv("IMAGE_SAVE_DIR") else None

# Module-level environment variable check
# 模块级环境变量检查
required_env_vars = {
    "BASE_URL": BASE_URL,
    "DOUBAO_API_KEY": DOUBAO_API_KEY,
    "API_MODEL_ID": API_MODEL_ID,
    "IMAGE_SAVE_DIR": IMAGE_SAVE_DIR
}

for var_name, var_value in required_env_vars.items():
    if not var_value:
        error_msg = f"Environment variable {var_name} is not set or empty, please check the environment field in MCP JSON configuration"
        logger.error(error_msg)
        debug_print(f"Error: {error_msg}")
        sys.exit(1)

logger.info("All required environment variables loaded successfully")
debug_print("✓ Environment variables check passed")

# Define available image resolutions
# 定义可用的图片分辨率
AVAILABLE_RESOLUTIONS = {
    "512x512": "512x512 (1:1 Small Square)",
    "768x768": "768x768 (1:1 Square)",
    "1024x1024": "1024x1024 (1:1 Large Square)",
    "864x1152": "864x1152 (3:4 Portrait)",
    "1152x864": "1152x864 (4:3 Landscape)",
    "1280x720": "1280x720 (16:9 Widescreen)",
    "720x1280": "720x1280 (9:16 Mobile Portrait)",
    "832x1248": "832x1248 (2:3)",
    "1248x832": "1248x832 (3:2)",
    "1512x648": "1512x648 (21:9 Ultra-wide)",
    "2048x2048": "2048x2048 (1:1 Extra Large Square)"
}



# Initialize image generation tool
# 初始化图像生成工具
image_generator = DoubaoImageGenerator(
    base_url=BASE_URL,
    api_key=DOUBAO_API_KEY,
    model_id=API_MODEL_ID,
    save_dir=IMAGE_SAVE_DIR
)

@mcp.resource("doubao://resolutions")
def get_available_resolutions() -> str:
    """Get available image resolution list
    获取可用的图片分辨率列表"""
    logger.info("Getting available resolution list")
    return format_options(AVAILABLE_RESOLUTIONS)

def format_options(options_dict: Dict[str, str]) -> str:
    """Format options dictionary to string
    将选项字典格式化为字符串"""
    formatted_lines = []
    for key, description in options_dict.items():
        formatted_lines.append(f"• {key}: {description}")
    return "\n".join(formatted_lines)

# Format resolution options
# 格式化分辨率选项
available_resolutions_list = format_options(AVAILABLE_RESOLUTIONS)

def validate_ascii_only(text: str, field_name: str) -> None:
    """Validate if text contains only ASCII characters
    验证文本是否只包含ASCII字符"""
    if not text.isascii():
        raise ValueError(f"{field_name} can only contain ASCII characters (letters, numbers, punctuation)")

def validate_resolution(size: str) -> None:
    """Validate if resolution is valid
    验证分辨率是否有效"""
    if size not in AVAILABLE_RESOLUTIONS:
        available = ", ".join(AVAILABLE_RESOLUTIONS.keys())
        raise ValueError(f"Invalid resolution '{size}'. Available resolutions: {available}")

@mcp.tool()
async def doubao_generate_image(
    prompt: Annotated[str, Field(description="Prompt for image generation, supports Chinese and English descriptions")],
    size: Annotated[str, Field(description=f"Image width and height in pixels, available values:\n{available_resolutions_list}")] = "1024x1024",
    seed: Annotated[int, Field(description="Random seed for controlling model generation randomness, if not specified, a random number will be auto-generated", ge=-1, le=2147483647)] = -1,
    guidance_scale: Annotated[float, Field(description="Consistency between model output and prompt, higher values follow prompt more strictly", ge=1.0, le=10.0)] = 8.0,
    watermark: Annotated[bool, Field(description="Whether to add watermark to generated images")] = True,
    file_prefix: Annotated[Optional[str], Field(description="Image filename prefix (letters, numbers, underscores only), max 20 characters")] = None
) -> List[TextContent]:
    """Generate image using Doubao API
    
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
    """
    
    logger.info(f"Starting image generation, prompt: {prompt[:50]}...")
    debug_print(f"🎨 Starting image generation: {prompt[:50]}...")
    
    try:
        # Parameter validation
        # 参数验证
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Validate resolution
        # 验证分辨率
        validate_resolution(size)
        
        # Validate file prefix (if provided)
        # 验证文件前缀（如果提供）
        if file_prefix:
            validate_ascii_only(file_prefix, "File prefix")
            # Validate file prefix length
            # 验证文件前缀长度
            if len(file_prefix) > 20:
                raise ValueError("File prefix length cannot exceed 20 characters")
            # Validate file prefix format
            # 验证文件前缀格式
            if not file_prefix.replace('_', '').replace('-', '').isalnum():
                raise ValueError("File prefix can only contain letters, numbers, underscores and hyphens")
        
        # Validate other parameters
        # 验证其他参数
        if not isinstance(seed, int) or seed < -1 or seed > 2147483647:
            raise ValueError("seed must be an integer between -1 and 2147483647")
        
        if not isinstance(guidance_scale, (int, float)) or guidance_scale < 1.0 or guidance_scale > 10.0:
            raise ValueError("guidance_scale must be a number between 1.0 and 10.0")
        
        if not isinstance(watermark, bool):
            raise ValueError("watermark must be a boolean value")
        
        logger.info(f"Parameter validation passed, calling image generation API")
        
        # Process seed parameter: if -1, generate a random number
        # 处理seed参数：如果是-1，则生成随机数
        import random
        actual_seed = seed
        if seed == -1:
            actual_seed = random.randint(0, 2147483647)
            logger.info(f"Generated random seed: {actual_seed}")
        
        # Call image generation processing
        # 调用图像生成处理
        result = await asyncio.create_task(
            image_generator.generate_image(
                prompt=prompt,
                size=size,
                seed=actual_seed,
                guidance_scale=guidance_scale,
                watermark=watermark,
                file_prefix=file_prefix
            )
        )
        
        logger.info(f"Image generation successful, result: {result}")
        debug_print(f"✅ Image generation successful")
        
        # Process return result
        # 处理返回结果
        if isinstance(result, dict) and "image_path" in result:
            image_path = result["image_path"]
            generation_info = result.get("generation_info", {})
            
            response_text = f"🎨 Image generation successful!\n\n"
            response_text += f"📁 Save path: {image_path}\n"
            response_text += f"📐 Resolution: {size}\n"
            response_text += f"🎯 Prompt: {prompt}\n"
            
            # Display actual seed used (from generation_info if available)
            # 显示实际使用的seed值（如果generation_info中有的话）
            actual_seed = generation_info.get('seed', seed) if generation_info else seed
            response_text += f"🎲 Seed: {actual_seed}\n"
            
            if generation_info:
                response_text += f"\n📊 Generation info:\n"
                for key, value in generation_info.items():
                    response_text += f"  • {key}: {value}\n"
            
            return [TextContent(type="text", text=response_text)]
        else:
            error_msg = "Image generation returned unexpected result format"
            logger.error(f"{error_msg}: {result}")
            return [TextContent(type="text", text=f"❌ {error_msg}")]
            
    except ValueError as e:
        error_msg = f"Parameter validation failed: {str(e)}"
        logger.error(error_msg)
        debug_print(f"❌ {error_msg}")
        return [TextContent(type="text", text=f"❌ {error_msg}")]
        
    except Exception as e:
        error_msg = f"Error occurred during image generation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        debug_print(f"❌ {error_msg}")
        return [TextContent(type="text", text=f"❌ {error_msg}")]

@mcp.prompt()
def image_generation_prompt(
    prompt: str,
    size: str = "1024x1024",
    seed: int = -1,
    guidance_scale: float = 8.0,
    watermark: bool = True,
    file_prefix: str = ""
) -> str:
    """Create image generation prompt template
    创建图片生成提示模板"""
    
    template = f"""
# Doubao Image Generation Request

## Basic Parameters
- **Prompt**: {prompt}
- **Resolution**: {size}
- **Random Seed**: {seed if seed != -1 else 'Auto-generate random number'}
- **Guidance Scale**: {guidance_scale}
- **Add Watermark**: {'Yes' if watermark else 'No'}
- **File Prefix**: {file_prefix if file_prefix else 'Use timestamp'}

## Available Resolution Options
{available_resolutions_list}

## Parameter Description
- **prompt**: Image description text, supports Chinese and English, more detailed descriptions yield better results
- **size**: Image width and height in pixels, choose from available options above
- **seed**: Random seed, if not specified, a random number will be auto-generated, same seed can reproduce results
- **guidance_scale**: 1.0-10.0, higher values follow prompt more strictly
- **watermark**: Whether to add "AI Generated" watermark
- **file_prefix**: Image filename prefix, letters, numbers and underscores only

## Usage Example
```
doubao_generate_image(
    prompt="A cute orange cat sitting on a sunny windowsill",
    size="1024x1024",
    guidance_scale=8.0,
    watermark=False,
    file_prefix="cute_cat"
)
```
"""
    
    return template

def main():
    """Main function entry point, start MCP server
    主函数入口，启动MCP服务器"""
    logger.info("Starting Doubao Image Generation MCP Server")
    debug_print("🚀 Starting Doubao Image Generation MCP Server")
    
    # Display configuration information (for debugging only)
    # 显示配置信息（仅用于调试）
    debug_print(f"📋 Configuration:")
    debug_print(f"  • BASE_URL: {BASE_URL}")
    debug_print(f"  • API_MODEL_ID: {API_MODEL_ID}")
    debug_print(f"  • IMAGE_SAVE_DIR: {IMAGE_SAVE_DIR}")
    debug_print(f"  • DOUBAO_API_KEY: {'Set' if DOUBAO_API_KEY else 'Not Set'}")
    
    # Start MCP server
    # 启动MCP服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
