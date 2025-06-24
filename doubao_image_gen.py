#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doubao Image Generation Tool
Implements image generation functionality based on Volcano Engine API

豆包图像生成工具
基于火山方舟API实现图像生成功能
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import requests
from PIL import Image
from io import BytesIO
from volcenginesdkarkruntime import Ark

# Function for outputting debug information to stderr
# 用于将调试信息输出到stderr的函数
def debug_print(*args, **kwargs):
    """Output debug information to stderr
    将调试信息输出到stderr"""
    print(*args, file=sys.stderr, **kwargs)

# Setup logging system
# 设置日志系统
def setup_logging():
    """Setup logging system, output logs to file
    设置日志系统，将日志输出到文件"""
    # Create log directory
    # 创建log文件夹
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    
    # Configure log format
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logger
    # 创建logger
    logger = logging.getLogger('doubao_image_gen')
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding duplicate handlers
    # 避免重复添加handler
    if not logger.handlers:
        # File handler
        # 文件handler
        file_handler = logging.FileHandler(log_dir / 'doubao_image_gen.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        
        # stderr handler
        # stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.INFO)
        stderr_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(stderr_handler)
    
    return logger

class DoubaoImageGenerator:
    """Doubao image generation tool class
    豆包图像生成工具类"""
    
    def __init__(self, base_url: str, api_key: str, model_id: str, save_dir: str):
        """Initialize image generation tool
        
        初始化图像生成工具
        
        Args:
            base_url: Doubao API base URL / 豆包API基础URL
            api_key: API key / API密钥
            model_id: Model ID / 模型ID
            save_dir: Image save directory / 图片保存目录
        """
        self.logger = setup_logging()
        
        # Set global variables
        # 设置全局变量
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.save_dir = save_dir
        
        self.logger.info(f"Initializing Doubao image generation tool")
        self.logger.info(f"BASE_URL: {base_url}")
        self.logger.info(f"MODEL_ID: {model_id}")
        self.logger.info(f"SAVE_DIR: {save_dir}")
        
        # Initialize Ark client
        # 初始化Ark客户端
        try:
            self.client = Ark(
                base_url=base_url,
                api_key=api_key
            )
            self.logger.info("Ark client initialized successfully")
            debug_print("✓ Ark client initialized successfully")
        except Exception as e:
            error_msg = f"Ark client initialization failed: {str(e)}"
            self.logger.error(error_msg)
            debug_print(f"❌ {error_msg}")
            raise
        
        # Create image save directory
        # 创建图片保存目录
        try:
            self.save_path = Path(save_dir)
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Image save directory created: {self.save_path.absolute()}")
            debug_print(f"✓ Image save directory: {self.save_path.absolute()}")
        except Exception as e:
            error_msg = f"Failed to create image save directory: {str(e)}"
            self.logger.error(error_msg)
            debug_print(f"❌ {error_msg}")
            raise
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        seed: int = -1,
        guidance_scale: float = 8.0,
        watermark: bool = True,
        file_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate image
        
        生成图像
        
        Args:
            prompt: Prompt for image generation / 用于生成图像的提示词
            size: Image width and height in pixels / 生成图像的宽高像素
            seed: Random seed / 随机数种子
            guidance_scale: Consistency between model output and prompt / 模型输出结果与prompt的一致程度
            watermark: Whether to add watermark to generated image / 是否在生成的图片中添加水印
            file_prefix: Image filename prefix / 图片文件名前缀
            
        Returns:
            Dictionary containing image path and generation information / 包含图片路径和生成信息的字典
        """
        
        self.logger.info(f"Starting image generation")
        self.logger.info(f"Parameters - prompt: {prompt[:100]}...")
        self.logger.info(f"Parameters - size: {size}, seed: {seed}, guidance_scale: {guidance_scale}")
        self.logger.info(f"Parameters - watermark: {watermark}, file_prefix: {file_prefix}")
        
        debug_print(f"🎨 Generating image...")
        
        try:
            # Parameter validation
            # 参数验证
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty")
            
            # Call Doubao API to generate image
            # 调用豆包API生成图片
            self.logger.info("Calling Doubao API to generate image")
            response = self.client.images.generate(
                model=self.model_id,
                prompt=prompt,
                size=size,
                seed=seed,
                guidance_scale=guidance_scale,
                watermark=watermark,
                response_format="url"  # 固定使用URL格式
            )
            
            self.logger.info("API call successful, processing response")
            debug_print("✓ API call successful")
            
            # Check response
            # 检查响应
            if not response or not response.data:
                raise ValueError("API returned empty response")
            
            # Get image URL
            # 获取图片URL
            image_url = response.data[0].url
            self.logger.info(f"Got image URL: {image_url}")
            
            # Wait and download image
            # 等待并下载图片
            self.logger.info("Starting image download")
            debug_print("📥 Downloading image...")
            
            # Add retry mechanism for image download
            # 添加重试机制的图片下载
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    # Asynchronously download image
                    # 异步下载图片
                    image_data = await self._download_image_async(image_url)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"Image download failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff / 指数退避
                    else:
                        raise
            
            self.logger.info("Image download successful")
            debug_print("✓ Image download successful")
            
            # Generate filename
            # 生成文件名
            if file_prefix:
                filename = f"image_{file_prefix}_{int(time.time())}.jpg"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}.jpg"
            
            # Save image
            # 保存图片
            image_path = self.save_path / filename
            
            # Save image data to file
            # 将图片数据保存到文件
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            self.logger.info(f"Image saved to: {image_path.absolute()}")
            debug_print(f"💾 Image saved: {image_path.name}")
            
            # Collect generation information
            # 收集生成信息
            # Use the seed parameter passed from MCP server (already processed for random generation)
            # 使用从MCP服务器传递的seed参数（已经处理过随机生成）
            
            generation_info = {
                "model": getattr(response, 'model', self.model_id),
                "created": getattr(response, 'created', int(time.time())),
                "seed": seed,
                "guidance_scale": guidance_scale,
                "watermark": watermark,
                "size": size,
                "original_url": image_url
            }
            
            result = {
                "image_path": str(image_path.absolute()),
                "filename": filename,
                "generation_info": generation_info
            }
            
            self.logger.info(f"Image generation completed: {result}")
            return result
            
        except Exception as e:
            error_msg = f"Image generation failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            debug_print(f"❌ {error_msg}")
            raise
    
    async def _download_image_async(self, url: str) -> bytes:
        """Asynchronously download image
        
        异步下载图片
        
        Args:
            url: Image URL / 图片URL
            
        Returns:
            Image binary data / 图片二进制数据
        """
        
        try:
            # Use requests to download image (consider using aiohttp in actual async environment)
            # 使用requests下载图片（在实际异步环境中可以考虑使用aiohttp）
            loop = asyncio.get_event_loop()
            
            def download_sync():
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.content
            
            # Execute synchronous download in thread pool
            # 在线程池中执行同步下载
            image_data = await loop.run_in_executor(None, download_sync)
            
            # Validate image data
            # 验证图片数据
            try:
                img = Image.open(BytesIO(image_data))
                img.verify()  # Verify image integrity / 验证图片完整性
                self.logger.info(f"Image validation successful, format: {img.format}, size: {img.size}")
            except Exception as e:
                raise ValueError(f"Downloaded image data is invalid: {str(e)}")
            
            return image_data
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Image download failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to process image data: {str(e)}")

# Test function
# 测试函数
async def test_image_generation():
    """Test image generation functionality
    测试图像生成功能"""
    
    print("🧪 Starting Doubao image generation test")
    
    # Test parameters (refer to fixed values in test_ark_image_generation.py)
    # 测试参数（参照test_ark_image_generation.py中的固定值）
    test_params = {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        #"api_key": "your_api_key_here",  # Need to replace with actual API key / 需要替换为实际的API密钥
        "api_key": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "model_id": "ep-20250528154802-c4np4",  # Need to replace with actual model ID / 需要替换为实际的模型ID
        "save_dir": "images"
    }
    
    test_prompt = "A fantasy scene of tiny people who accidentally entered a normal human kitchen and are cooking with human kitchen utensils"
    
    try:
        # Create image generator
        # 创建图像生成器
        generator = DoubaoImageGenerator(
            base_url=test_params["base_url"],
            api_key=test_params["api_key"],
            model_id=test_params["model_id"],
            save_dir=test_params["save_dir"]
        )
        
        print(f"✓ Image generator initialized successfully")
        
        # Generate image
        # 生成图片
        result = await generator.generate_image(
            prompt=test_prompt,
            size="1024x1024",
            seed=-1,
            guidance_scale=10.0,
            watermark=False,
            file_prefix="test"
        )
        
        print(f"✅ Test successful!")
        print(f"📁 Image path: {result['image_path']}")
        print(f"📊 Generation info: {result['generation_info']}")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Doubao Image Generation Tool - Standalone Test Mode")
    print("Note: Please ensure correct API key and model ID are set")
    
    # Run test
    # 运行测试
    asyncio.run(test_image_generation())
