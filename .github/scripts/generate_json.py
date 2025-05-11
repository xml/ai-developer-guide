#!/usr/bin/env python3
"""
Script to convert markdown guide files to a single structured JSON file.
This simplified version combines the core guide and manifest into one file.
"""

import json
import os
import re
import sys
from datetime import datetime

def extract_references(content):
    """Extract references to specialized guides."""
    references = []
    
    # Pattern to match markdown links like [Python Guide](./docs/guides/python.md)
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    guide_links = re.finditer(link_pattern, content)
    
    for match in guide_links:
        name = match.group(1)
        path = match.group(2)
        
        # Only include links to guide documents
        if 'guides' in path and path.endswith('.md'):
            references.append({
                "name": name,
                "path": path,
                "type": infer_guide_type(path)
            })
    
    return references

def infer_guide_type(path):
    """Infer the type of guide from its path."""
    if 'python' in path.lower():
        return "language"
    elif 'make' in path.lower():
        return "pattern"
    elif 'postgresql' in path.lower() or 'sql' in path.lower():
        return "platform"
    elif 'shell' in path.lower():
        return "language"
    else:
        return "other"

def create_guide_json(readme_path, output_dir):
    """Create a single guide.json from README."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README: {e}")
        sys.exit(1)
    
    # Skip the HTML header and introduction sections
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Find where the actual guide begins
    guide_start_idx = content.find('## The Golden Rules')
    if guide_start_idx == -1:
        print("Error: Could not find the beginning of the guide.")
        sys.exit(1)
    
    # Get the main content from the guide start point onwards
    guide_content = content[guide_start_idx:]
    
    # Extract references to guides
    references = extract_references(guide_content)
    
    # Create a single combined guide.json structure
    guide_data = {
        "metadata": {
            "name": "AI Developer Guide",
            "version": "0.1.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "source": "https://github.com/dwmkerr/ai-developer-guide"
        },
        "content": guide_content,
        "references": references
    }
    
    # Ensure output directory exists
    api_dir = os.path.join(output_dir, "api")
    os.makedirs(api_dir, exist_ok=True)
    
    # Write the JSON file
    try:
        # Define paths
        guide_json_path = os.path.join(api_dir, "guide.json")
        index_html_path = os.path.join(output_dir, "index.html")
        
        # Write guide.json
        with open(guide_json_path, 'w', encoding='utf-8') as f:
            json.dump(guide_data, f, indent=2)
            print(f"✓ Created {guide_json_path}")
        
        # Create a simple index file to help with navigation
        index_html = """<!DOCTYPE html>
<html>
<head>
    <title>AI Developer Guide API</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        a { color: #0366d6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        code { background-color: #f6f8fa; padding: 3px 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>AI Developer Guide API</h1>
    <p>This is the JSON API for the AI Developer Guide. Available endpoint:</p>
    <ul>
        <li><a href="api/guide.json">guide.json</a> - Complete AI developer guide</li>
    </ul>
    <h2>Usage with MCP</h2>
    <p>To use with Model Context Protocol:</p>
    <pre><code>GET /api/guide.json  // Get the complete developer guide</code></pre>
</body>
</html>"""

        with open(index_html_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
            print(f"✓ Created {index_html_path}")

        print("Successfully generated JSON API files.")
        
        # List all created files for verification
        print(f"\nGenerated files in {output_dir}:")
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                print(f"  - {os.path.join(root, file)}")
    except Exception as e:
        print(f"Error writing JSON files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_json.py README_PATH OUTPUT_DIR")
        sys.exit(1)
    
    readme_path = sys.argv[1]
    output_dir = sys.argv[2]
    create_guide_json(readme_path, output_dir)
