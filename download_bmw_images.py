#!/usr/bin/env python3
"""
BMW Image Downloader
Downloads real BMW car images from the web with appropriate sizes
"""

import os
import requests
import time
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BMWImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.images_dir = "static/images"
        
        # Ensure images directory exists
        os.makedirs(self.images_dir, exist_ok=True)
        
        # BMW model image URLs (using Unsplash and other free image sources)
        self.image_urls = {
            # Series images
            "bmw-suvs.jpg": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600&h=400&fit=crop&crop=center",
            "bmw-sedans.jpg": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&h=400&fit=crop&crop=center",
            "bmw-coupes.jpg": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=600&h=400&fit=crop&crop=center",
            "bmw-convertibles.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop&crop=center",
            "bmw-electric.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=600&h=400&fit=crop&crop=center",
            "bmw-m-models.jpg": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=600&h=400&fit=crop&crop=center",
            "bmw-hero-bg.jpg": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=1200&h=600&fit=crop&crop=center",
            
            # X Series SUVs
            "x1-front.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "x1-side.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "x1-rear.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "x1-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            "x3-front.jpg": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=450&fit=crop&crop=center",
            "x3-side.jpg": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=450&fit=crop&crop=center",
            "x3-rear.jpg": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=450&fit=crop&crop=center",
            "x3-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            "x5-front.jpg": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=450&fit=crop&crop=center",
            "x5-side.jpg": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=450&fit=crop&crop=center",
            "x5-rear.jpg": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=450&fit=crop&crop=center",
            "x5-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            # 3 Series
            "3-series-front.jpg": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&h=450&fit=crop&crop=center",
            "3-series-side.jpg": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&h=450&fit=crop&crop=center",
            "3-series-rear.jpg": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&h=450&fit=crop&crop=center",
            "3-series-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            # 5 Series
            "5-series-front.jpg": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=450&fit=crop&crop=center",
            "5-series-side.jpg": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=450&fit=crop&crop=center",
            "5-series-rear.jpg": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=450&fit=crop&crop=center",
            "5-series-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            # M Series
            "m3-front.jpg": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&h=450&fit=crop&crop=center",
            "m3-side.jpg": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&h=450&fit=crop&crop=center",
            "m3-rear.jpg": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=800&h=450&fit=crop&crop=center",
            "m3-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            "m5-front.jpg": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=450&fit=crop&crop=center",
            "m5-side.jpg": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=450&fit=crop&crop=center",
            "m5-rear.jpg": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=450&fit=crop&crop=center",
            "m5-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            # Electric i Series
            "i4-front.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "i4-side.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "i4-rear.jpg": "https://images.unsplash.com/photo-1617654112368-307921291f42?w=800&h=450&fit=crop&crop=center",
            "i4-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
            
            # Z4 Roadster
            "z4-front.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=450&fit=crop&crop=center",
            "z4-side.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=450&fit=crop&crop=center",
            "z4-rear.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=450&fit=crop&crop=center",
            "z4-interior.jpg": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=450&fit=crop&crop=center",
        }
    
    def download_image(self, filename, url, max_retries=3):
        """Download a single image with retry logic"""
        filepath = os.path.join(self.images_dir, filename)
        
        # Skip if file already exists and has reasonable size
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:  # > 10KB
            logger.info(f"✅ {filename} already exists and looks good")
            return True
        
        for attempt in range(max_retries):
            try:
                logger.info(f"📥 Downloading {filename} (attempt {attempt + 1}/{max_retries})")
                
                response = self.session.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    logger.warning(f"⚠️  URL doesn't return an image: {content_type}")
                    continue
                
                # Download and save
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Check file size
                file_size = os.path.getsize(filepath)
                if file_size < 1000:  # Less than 1KB might be an error
                    logger.warning(f"⚠️  Downloaded file seems too small: {file_size} bytes")
                    os.remove(filepath)
                    continue
                
                logger.info(f"✅ Successfully downloaded {filename} ({file_size:,} bytes)")
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to download {filename}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                
        return False
    
    def download_all_images(self):
        """Download all BMW images"""
        logger.info("🚗 Starting BMW image download...")
        
        successful = 0
        failed = 0
        
        for filename, url in self.image_urls.items():
            if self.download_image(filename, url):
                successful += 1
            else:
                failed += 1
            
            # Be respectful to the server
            time.sleep(1)
        
        logger.info(f"📊 Download complete: {successful} successful, {failed} failed")
        
        if failed > 0:
            logger.info("💡 For failed downloads, you may need to:")
            logger.info("   - Use different image URLs")
            logger.info("   - Check your internet connection")
            logger.info("   - Try running the script again")
        
        return successful, failed

    def download_alternative_images(self):
        """Download alternative BMW images from different sources"""
        logger.info("🔄 Trying alternative image sources...")
        
        # Alternative URLs using different image services
        alternative_urls = {
            "bmw-suvs.jpg": "https://picsum.photos/600/400?random=1",
            "bmw-sedans.jpg": "https://picsum.photos/600/400?random=2", 
            "bmw-coupes.jpg": "https://picsum.photos/600/400?random=3",
            "bmw-convertibles.jpg": "https://picsum.photos/600/400?random=4",
            "bmw-electric.jpg": "https://picsum.photos/600/400?random=5",
            "bmw-m-models.jpg": "https://picsum.photos/600/400?random=6",
            "bmw-hero-bg.jpg": "https://picsum.photos/1200/600?random=7",
        }
        
        successful = 0
        for filename, url in alternative_urls.items():
            if self.download_image(filename, url):
                successful += 1
            time.sleep(1)
        
        return successful

def main():
    downloader = BMWImageDownloader()
    
    # Try primary sources first
    successful, failed = downloader.download_all_images()
    
    # If some failed, try alternatives for series images
    if failed > 0:
        logger.info("🔄 Some downloads failed, trying alternative sources...")
        downloader.download_alternative_images()
    
    logger.info("🎉 BMW image download process completed!")
    logger.info("📁 Check the static/images/ directory for downloaded images")

if __name__ == "__main__":
    main()
