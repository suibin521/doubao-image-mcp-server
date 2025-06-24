#!/usr/bin/env python3
"""
Doubao Image Generation Module

This module provides image generation functionality using the Doubao API
from Volcano Engine. It supports various image generation parameters
including size, seed, guidance scale, and watermark options.

Author: suibin521
Version: 1.0.0
License: MIT
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any, List
from volcengine.ark import Ark


class DoubaoImageGenerator:
    """
    Doubao Image Generator using Volcano Engine API
    
    This class handles image generation requests to the Doubao API,
    including parameter validation, API calls, and image downloading.
    """
    
    # Available image sizes
    AVAILABLE_SIZES = [
        "512x512", "768x768", "1024x1024", "864x1152", "1152x864",
        "1280x720", "720x1280", "832x1248", "1248x832", "1512x648", "2048x2048"
    ]
    
    def __init__(self, api_key: str, base_url: str, model_id: str):
        """
        Initialize the Doubao Image Generator
        
        Args:
            api_key: Volcano Engine API key
            base_url: API base URL
            model_id: Model ID for image generation
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model_id
        self.client = Ark(api_key=api_key, base_url=base_url)
    
    def validate_parameters(self, size: str, seed: int, guidance_scale: float) -> None:
        """
        Validate generation parameters
        
        Args:
            size: Image size in format "WIDTHxHEIGHT"
            seed: Random seed for generation
            guidance_scale: Guidance scale for prompt adherence
            
        Raises:
            ValueError: If parameters are invalid
        """
        if size not in self.AVAILABLE_SIZES:
            raise ValueError(f"Size {size} not supported. Available sizes: {self.AVAILABLE_SIZES}")
        
        if not (-1 <= seed <= 2147483647):
            raise ValueError("Seed must be between -1 and 2147483647")
        
        if not (1.0 <= guidance_scale <= 10.0):
            raise ValueError("Guidance scale must be between 1.0 and 10.0")
    
    def generate_image(self, 
                      prompt: str, 
                      size: str = "1024x1024",
                      seed: int = -1,
                      guidance_scale: float = 8.0,
                      watermark: bool = True) -> Dict[str, Any]:
        """
        Generate an image using the Doubao API
        
        Args:
            prompt: Text description for image generation
            size: Image size (default: "1024x1024")
            seed: Random seed (default: -1 for random)
            guidance_scale: Guidance scale (default: 8.0)
            watermark: Whether to add watermark (default: True)
            
        Returns:
            Dictionary containing generation result and metadata
            
        Raises:
            ValueError: If parameters are invalid
            Exception: If API call fails
        """
        # Validate parameters
        self.validate_parameters(size, seed, guidance_scale)
        
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        try:
            # Prepare request parameters
            request_params = {
                "model": self.model_id,
                "prompt": prompt.strip(),
                "size": size,
                "guidance_scale": guidance_scale,
                "watermark": watermark
            }
            
            # Add seed if specified
            if seed != -1:
                request_params["seed"] = seed
            
            # Make API call
            response = self.client.images.generate(**request_params)
            
            # Extract response data
            if hasattr(response, 'data') and response.data:
                image_data = response.data[0]
                result = {
                    "url": image_data.url,
                    "revised_prompt": getattr(image_data, 'revised_prompt', prompt),
                    "model": response.model,
                    "created": response.created,
                    "seed": getattr(image_data, 'seed', seed),
                    "guidance_scale": guidance_scale,
                    "watermark": watermark,
                    "size": size,
                    "original_prompt": prompt
                }
                return result
            else:
                raise Exception("No image data in API response")
                
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    def download_image(self, url: str, save_path: str) -> bool:
        """
        Download image from URL to local file
        
        Args:
            url: Image URL
            save_path: Local file path to save the image
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to file
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Failed to download image: {str(e)}")
            return False
    
    def generate_and_save(self, 
                         prompt: str,
                         save_dir: str = "./images",
                         filename_prefix: str = "image",
                         size: str = "1024x1024",
                         seed: int = -1,
                         guidance_scale: float = 8.0,
                         watermark: bool = True) -> Dict[str, Any]:
        """
        Generate image and save to local file
        
        Args:
            prompt: Text description for image generation
            save_dir: Directory to save the image
            filename_prefix: Prefix for the filename
            size: Image size
            seed: Random seed
            guidance_scale: Guidance scale
            watermark: Whether to add watermark
            
        Returns:
            Dictionary containing generation result and local file path
        """
        # Generate image
        result = self.generate_image(prompt, size, seed, guidance_scale, watermark)
        
        # Create filename with timestamp
        timestamp = int(time.time())
        if filename_prefix:
            filename = f"{filename_prefix}_{timestamp}.jpg"
        else:
            filename = f"image_{timestamp}.jpg"
        
        save_path = os.path.join(save_dir, filename)
        
        # Download and save image
        if self.download_image(result["url"], save_path):
            result["local_path"] = save_path
            result["filename"] = filename
        else:
            result["local_path"] = None
            result["filename"] = None
        
        return result
