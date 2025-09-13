import os
import requests
from urllib.parse import urlparse

def download_image(url, folder, filename=None):
    """Download an image from a URL and save it to the specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    if not filename:
        # Extract filename from URL if not provided
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
    
    filepath = os.path.join(folder, filename)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filepath}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    # Base directory for images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Image URLs with their respective folders and filenames
    images = [
        # Hero images
        ("https://images.unsplash.com/photo-1441984904996-e0b6ba687e04", "images/hero", "hero-bg.jpg"),
        
        # Product images
        ("https://images.unsplash.com/photo-1521572163474-6864f9cf17ab", "images/products", "t-shirt-1.jpg"),
        ("https://images.unsplash.com/photo-1521225230528-429f70e8b9b3", "images/products", "polo-shirt-1.jpg"),
        ("https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9", "images/products", "hoodie-1.jpg"),
        ("https://images.unsplash.com/photo-1551232864-3f0890e580d9", "images/products", "sweatshirt-1.jpg"),
        ("https://images.unsplash.com/photo-1525507119028-ed4c629a60a3", "images/products", "t-shirt-2.jpg"),
        ("https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9", "images/products", "polo-shirt-2.jpg"),
        
        # Team images
        ("https://randomuser.me/api/portraits/men/32.jpg", "images/team", "team-1.jpg"),
        ("https://randomuser.me/api/portraits/women/44.jpg", "images/team", "team-2.jpg"),
        ("https://randomuser.me/api/portraits/men/75.jpg", "images/team", "team-3.jpg"),
        ("https://randomuser.me/api/portraits/women/68.jpg", "images/team", "team-4.jpg"),
        
        # Testimonial images
        ("https://randomuser.me/api/portraits/men/22.jpg", "images/testimonials", "testimonial-1.jpg"),
        ("https://randomuser.me/api/portraits/women/33.jpg", "images/testimonials", "testimonial-2.jpg"),
        ("https://randomuser.me/api/portraits/men/45.jpg", "images/testimonials", "testimonial-3.jpg"),
        
        # About page images
        ("https://images.unsplash.com/photo-1522071820081-6f153eaf13f9", "images", "about-hero.jpg"),
        ("https://images.unsplash.com/photo-1522202176988-66273c2fd55f", "images", "team-photo.jpg"),
        
        # Contact page images
        ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab", "images", "contact-bg.jpg"),
        
        # Products page images
        ("https://images.unsplash.com/photo-1489987707025-afc232f7ea0f", "images", "products-hero.jpg"),
    ]
    
    # Download all images
    for url, folder, filename in images:
        full_folder = os.path.join(base_dir, folder)
        download_image(url, full_folder, filename)
    
    # Create a simple apple-touch-icon.png
    apple_touch_icon = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QgJDx0H7p1jXQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAJklEQVQ4y2NgGAWjFjAMcQv+Y2J8GmCg0gQeFhZQ1QIA4dQkGQZQpVUAAAAASUVORK5CYII="""
    
    apple_touch_path = os.path.join(base_dir, "images", "apple-touch-icon.png")
    with open(apple_touch_path, "wb") as f:
        f.write(apple_touch_icon.encode('latin1'))
    print(f"Created: {apple_touch_path}")
    
    print("\nImage download and setup complete!")

if __name__ == "__main__":
    main()
