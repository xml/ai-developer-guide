#!/usr/bin/env python3
"""
Script to convert markdown guide files to structured JSON for MCP consumption.
Initially focuses on just converting the core README.md to JSON.
"""

import json
import os
import re
import sys
from datetime import datetime

def extract_sections(content):
    """Extract main sections from the README file."""
    # Skip the HTML header and introduction sections
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Find where the actual guide begins
    guide_start_idx = content.find('## The Golden Rules')
    if guide_start_idx == -1:
        print("Error: Could not find the beginning of the guide.")
        sys.exit(1)
    
    content = content[guide_start_idx:]
    
    # Extract main sections
    sections = {}
    
    # Extract Golden Rules section
    golden_rules_match = re.search(r'## The Golden Rules(.*?)(?=##)', content, re.DOTALL)
    if golden_rules_match:
        sections["goldenRules"] = golden_rules_match.group(1).strip()
    
    # Extract Plan/Implement/Review Approach
    approach_match = re.search(r'## The Plan / Implement / Review Approach(.*?)(?=## The Developer Guide)', content, re.DOTALL)
    if approach_match:
        approach_content = approach_match.group(1).strip()
        
        # Extract subsections for Planning, Implementation, and Review
        planning_match = re.search(r'### Phase 1: Planning(.*?)(?=### Phase 2)', approach_content, re.DOTALL)
        implementation_match = re.search(r'### Phase 2: Implementation(.*?)(?=### Phase 3)', approach_content, re.DOTALL)
        review_match = re.search(r'### Phase 3: Review(.*?)$', approach_content, re.DOTALL)
        
        sections["approach"] = {
            "overview": approach_content.split("### Phase")[0].strip(),
            "phases": {
                "planning": planning_match.group(1).strip() if planning_match else "",
                "implementation": implementation_match.group(1).strip() if implementation_match else "",
                "review": review_match.group(1).strip() if review_match else ""
            }
        }
    
    # Extract Developer Guide sections
    dev_guide_match = re.search(r'## The Developer Guide(.*?)(?=## Project Components|$)', content, re.DOTALL)
    if dev_guide_match:
        dev_guide_content = dev_guide_match.group(1).strip()
        
        # Extract subsections
        documentation_match = re.search(r'### Documentation(.*?)(?=### Comments|$)', dev_guide_content, re.DOTALL)
        comments_match = re.search(r'### Comments(.*?)(?=### Modules|$)', dev_guide_content, re.DOTALL)
        modules_match = re.search(r'### Modules(.*?)(?=### Project Structure|$)', dev_guide_content, re.DOTALL)
        project_structure_match = re.search(r'### Project Structure(.*?)(?=### Technical Debt|$)', dev_guide_content, re.DOTALL)
        tech_debt_match = re.search(r'### Technical Debt(.*?)$', dev_guide_content, re.DOTALL)
        
        sections["developerGuide"] = {
            "overview": dev_guide_content.split("### ")[0].strip(),
            "sections": {
                "documentation": documentation_match.group(1).strip() if documentation_match else "",
                "comments": comments_match.group(1).strip() if comments_match else "",
                "modules": modules_match.group(1).strip() if modules_match else "",
                "projectStructure": project_structure_match.group(1).strip() if project_structure_match else "",
                "technicalDebt": tech_debt_match.group(1).strip() if tech_debt_match else ""
            }
        }
    
    # Extract references to specific guides
    sections["references"] = extract_references(content)
    
    return sections

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

def create_core_json(readme_path, output_dir):
    """Create core.json from README."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README: {e}")
        sys.exit(1)
    
    sections = extract_sections(content)
    
    # Create core.json structure
    core_data = {
        "metadata": {
            "name": "AI Developer Guide",
            "version": "0.1.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "source": "https://github.com/dwmkerr/ai-developer-guide"
        },
        "core": sections
    }
    
    # Create manifest.json structure
    manifest_data = {
        "metadata": {
            "name": "AI Developer Guide",
            "version": "0.1.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d")
        },
        "guides": {
            "core": "/api/core.json",
            "languages": {
                "python": "/api/guides/languages/python.json",
                "shellScripts": "/api/guides/languages/shell-scripts.json"
            },
            "patterns": {
                "makefiles": "/api/guides/patterns/make.json"
            },
            "platforms": {
                "postgresql": "/api/guides/platforms/postgresql.json"
            }
        },
        "references": sections.get("references", [])
    }
    
    # Ensure output directory exists
    api_dir = os.path.join(output_dir, "api")
    os.makedirs(api_dir, exist_ok=True)
    
    # Write the JSON files
    try:
        # Define paths
        core_json_path = os.path.join(api_dir, "core.json")
        manifest_json_path = os.path.join(api_dir, "manifest.json")
        index_html_path = os.path.join(output_dir, "index.html")
        
        # Write core.json
        with open(core_json_path, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, indent=2)
            print(f"✓ Created {core_json_path}")
        
        # Write manifest.json
        with open(manifest_json_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2)
            print(f"✓ Created {manifest_json_path}")
        
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
    <p>This is the JSON API for the AI Developer Guide. Available endpoints:</p>
    <ul>
        <li><a href="api/manifest.json">manifest.json</a> - Overview of all available guides</li>
        <li><a href="api/core.json">core.json</a> - Core developer guide principles</li>
    </ul>
    <h2>Usage with MCP</h2>
    <p>To use with Model Context Protocol:</p>
    <pre><code>GET /api/manifest.json  // Discover available guides
GET /api/core.json     // Get core developer guide</code></pre>
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
    create_core_json(readme_path, output_dir)
