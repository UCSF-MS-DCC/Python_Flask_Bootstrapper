#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import platform
import venv
import shutil
import json
import datetime

def create_directory_structure(app_dir):
    """Create the standard Flask directory structure."""
    directories = [
        os.path.join(app_dir, "app"),
        os.path.join(app_dir, "app", "static"),
        os.path.join(app_dir, "app", "static", "css"),
        os.path.join(app_dir, "app", "static", "js"),
        os.path.join(app_dir, "app", "static", "img"),
        os.path.join(app_dir, "app", "templates"),
        os.path.join(app_dir, "app", "models"),
        os.path.join(app_dir, "app", "views"),
        os.path.join(app_dir, "app", "forms"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_app_file(app_dir, stubs_count=0):
    """Create a basic app.py file with optional stub routes."""
    app_content = """#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

@app.route('/')
def index():
    return render_template('index.html')
"""

    # Add stub routes if requested
    if stubs_count > 0:
        stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
        
        for i in range(stubs_count):
            stub_name = stub_names[i]
            app_content += f"""
@app.route('/{stub_name}/index')
def {stub_name}_index():
    return render_template('{stub_name}/index.html')
"""
    
    app_content += """
if __name__ == '__main__':
    app.run(debug=True)
"""
    
    with open(os.path.join(app_dir, "app.py"), "w") as f:
        f.write(app_content)
    print(f"Created app.py file with {stubs_count} stub route(s)")
    
    # Make app.py executable
    os.chmod(os.path.join(app_dir, "app.py"), 0o755)

def create_requirements_file(app_dir):
    """Create a requirements.txt file."""
    requirements_content = """flask==2.3.3
werkzeug==2.3.7
jinja2==3.1.2
"""
    
    with open(os.path.join(app_dir, "requirements.txt"), "w") as f:
        f.write(requirements_content)
    print(f"Created requirements.txt file")

def create_base_template(app_dir, stubs_count=0):
    """Create a base.html template using Pure CSS."""
    # Create stub menu items if requested
    menu_items = ""
    if stubs_count > 0:
        stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
        
        for i in range(stubs_count):
            stub_name = stub_names[i]
            menu_items += f"""                        <li class="pure-menu-item"><a href="/{stub_name}/index" 
class="pure-menu-link">{stub_name.capitalize()}</a></li>
"""
    
    template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Prototype{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" 
integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    {% block styles %}{% endblock %}
</head>
<body>
    <div class="pure-g">
        <div class="pure-u-1">
            <div class="header">
                <div class="pure-menu pure-menu-horizontal">
                    <a href="/" class="pure-menu-heading">PROTOTYPE</a>
                    <ul class="pure-menu-list">
                        <li class="pure-menu-item"><a href="/" class="pure-menu-link">Home</a></li>
""" + menu_items + """                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="pure-g">
        <div class="pure-u-1">
            <div class="content-wrapper">
                {% block content %}{% endblock %}
            </div>
        </div>
    </div>

    <div class="pure-g">
        <div class="pure-u-1">
            <div class="footer">
                <p>&copy; {% block year %}2025{% endblock %} Prototype App</p>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""
    
    template_path = os.path.join(app_dir, "app", "templates", "base.html")
    with open(template_path, "w") as f:
        f.write(template_content)
    print(f"Created base.html template")

def create_index_template(app_dir, build_count, build_history):
    """Create a basic index.html template that extends base.html with build tracking."""
    # Format the build history for display
    history_entries = ""
    for entry in build_history[-5:]:  # Show only the last 5 entries
        history_entries += f"""                <li><strong>{entry['date']}</strong>: App #{entry['id']} - 
{entry['name']}</li>
"""
    
    template_content = """{% extends "base.html" %}

{% block title %}Home - Prototype{% endblock %}

{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
{% endblock %}

{% block content %}
<div class="pure-g">
    <div class="pure-u-1">
        <h1>Welcome to your Flask Prototype Application!</h1>
        <p>This is a starter template for your Flask project using Pure CSS.</p>
        
        <div class="build-info">
            <h3>Build Statistics</h3>
            <p>This is app number <strong>""" + str(build_count) + """</strong> created with this bootstrapper.</p>
            
            <h4>Recent Build History</h4>
            <ul class="build-history">
""" + history_entries + """            </ul>
        </div>
        
        <h2>Libraries and Versions</h2>
        <div class="libraries-list">
            <h3>Backend Libraries (Python)</h3>
            <ul class="pure-list">
                <li><strong>Flask</strong>: 2.3.3</li>
                <li><strong>Werkzeug</strong>: 2.3.7</li>
                <li><strong>Jinja2</strong>: 3.1.2</li>
            </ul>
            
            <h3>Frontend Libraries (CDN)</h3>
            <ul class="pure-list">
                <li><strong>Pure CSS</strong>: 3.0.0</li>
                <li><strong>Pure CSS Responsive Grids</strong>: 3.0.0</li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/index.js') }}"></script>
{% endblock %}
"""
    
    template_path = os.path.join(app_dir, "app", "templates", "index.html")
    with open(template_path, "w") as f:
        f.write(template_content)
    print(f"Created index.html template with build tracking")

def create_stub_templates(app_dir, stubs_count):
    """Create templates for stub routes."""
    stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
    
    for i in range(stubs_count):
        stub_name = stub_names[i]
        
        # Create directory for stub templates
        stub_dir = os.path.join(app_dir, "app", "templates", stub_name)
        os.makedirs(stub_dir, exist_ok=True)
        
        # Create stub template
        template_content = f"""{{% extends "base.html" %}}

{{% block title %}}{stub_name.capitalize()} - Prototype{{% endblock %}}

{{% block styles %}}
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/{stub_name}.css') }}}}">
{{% endblock %}}

{{% block content %}}
<div class="pure-g">
    <div class="pure-u-1">
        <h1>{stub_name.capitalize()} Page</h1>
        <div class="{stub_name}-content">
            <!-- Content goes here -->
        </div>
    </div>
</div>
{{% endblock %}}

{{% block scripts %}}
<script src="{{{{ url_for('static', filename='js/{stub_name}.js') }}}}"></script>
{{% endblock %}}
"""
        
        template_path = os.path.join(stub_dir, "index.html")
        with open(template_path, "w") as f:
            f.write(template_content)
        print(f"Created {stub_name}/index.html template")

def create_base_css(app_dir):
    """Create a base CSS file."""
    css_content = """/* Base styles for Flask app */
body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

.header {
    background-color: #2d3e50;
    color: white;
    padding: 0.5em;
}

.pure-menu-heading {
    color: white !important;
    font-weight: bold;
    font-size: 1.2em;
    text-transform: uppercase;
}

.pure-menu-link {
    color: #ddd !important;
}

.pure-menu-link:hover {
    background-color: #1f2c38 !important;
}

.content-wrapper {
    padding: 2em;
    max-width: 1200px;
    margin: 0 auto;
}

.footer {
    background-color: #eee;
    color: #666;
    padding: 1em;
    text-align: center;
    font-size: 0.9em;
}

h1, h2, h3, h4 {
    color: #2d3e50;
    margin-top: 0;
}

.libraries-list, .build-info {
    margin: 2em 0;
    padding: 1.5em;
    background-color: #f8f9fa;
    border-radius: 5px;
    border-left: 4px solid #2d3e50;
}

.build-info {
    border-left-color: #e74c3c;
}

.pure-list, .build-history {
    list-style-type: none;
    padding-left: 0;
}

.pure-list li, .build-history li {
    padding: 0.5em 0;
    border-bottom: 1px solid #eee;
}

.pure-list li:last-child, .build-history li:last-child {
    border-bottom: none;
}
"""
    
    css_path = os.path.join(app_dir, "app", "static", "css", "base.css")
    with open(css_path, "w") as f:
        f.write(css_content)
    print(f"Created base.css file")

def create_css_file(app_dir):
    """Create a basic CSS file for index."""
    css_content = """/* Index page specific styles */
.welcome-section {
    padding: 2em 0;
}

.libraries-list h3, .build-info h3 {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    color: #2d3e50;
    border-bottom: 2px solid #eee;
    padding-bottom: 0.5em;
}

.build-info h3 {
    color: #e74c3c;
}

.build-info h4 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

.build-history {
    background-color: rgba(231, 76, 60, 0.05);
    padding: 0.5em 1em;
    border-radius: 4px;
}
"""
    
    css_path = os.path.join(app_dir, "app", "static", "css", "index.css")
    with open(css_path, "w") as f:
        f.write(css_content)
    print(f"Created index.css file")

def create_stub_css_files(app_dir, stubs_count):
    """Create CSS files for stub pages."""
    stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    for i in range(stubs_count):
        stub_name = stub_names[i]
        color = colors[i]
        
        css_content = f"""/* {stub_name.capitalize()} page specific styles */
.{stub_name}-content {{
    background-color: {color}20;
    border-left: 4px solid {color};
    padding: 1em;
    margin: 1em 0;
    border-radius: 4px;
}}

h1 {{
    color: {color};
}}
"""
        
        css_path = os.path.join(app_dir, "app", "static", "css", f"{stub_name}.css")
        with open(css_path, "w") as f:
            f.write(css_content)
        print(f"Created {stub_name}.css file")

def create_base_js(app_dir):
    """Create a base JavaScript file."""
    js_content = """// Base JavaScript functions
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask application loaded');
    
    // Add current year to footer if the element exists
    const yearElement = document.querySelector('.footer p');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.innerHTML = yearElement.innerHTML.replace('2025', currentYear);
    }
    
    // Highlight current page in menu
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.pure-menu-link');
    
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('pure-menu-selected');
            link.style.backgroundColor = '#1f2c38';
        }
    });
});
"""
    
    js_path = os.path.join(app_dir, "app", "static", "js", "base.js")
    with open(js_path, "w") as f:
        f.write(js_content)
    print(f"Created base.js file")

def create_js_file(app_dir):
    """Create a basic JavaScript file for index."""
    js_content = """// Index page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Index page loaded');
});
"""
    
    js_path = os.path.join(app_dir, "app", "static", "js", "index.js")
    with open(js_path, "w") as f:
        f.write(js_content)
    print(f"Created index.js file")

def create_stub_js_files(app_dir, stubs_count):
    """Create JavaScript files for stub pages."""
    stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
    
    for i in range(stubs_count):
        stub_name = stub_names[i]
        
        js_content = f"""// {stub_name.capitalize()} page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {{
    console.log('{stub_name.capitalize()} page loaded');
    
    // You can add page-specific JavaScript here
    const contentDiv = document.querySelector('.{stub_name}-content');
    if (contentDiv) {{
        contentDiv.innerHTML = '<p>This content was dynamically added by {stub_name}.js</p>';
    }}
}});
"""
        
        js_path = os.path.join(app_dir, "app", "static", "js", f"{stub_name}.js")
        with open(js_path, "w") as f:
            f.write(js_content)
        print(f"Created {stub_name}.js file")

def create_gitignore(app_dir):
    """Create a .gitignore file."""
    gitignore_content = """# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Environment Variables
.env
.flaskenv

# IDE specific files
.idea/
.vscode/
*.swp
*.swo
"""
    
    with open(os.path.join(app_dir, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    print(f"Created .gitignore file")

def create_readme(app_dir, app_name, stubs_count, build_count):
    """Create a README.md file."""
    stubs_text = ""
    if stubs_count > 0:
        stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
        stubs_text = "\n\n## Stub Routes\n\n"
        for i in range(stubs_count):
            stubs_text += f"- /{stub_names[i]}/index\n"
    
    readme_content = f"""# {app_name}

A Flask web application using Pure CSS framework.

> This is app #{build_count} created with the Flask Bootstrapper.

## Setup

1. Activate the virtual environment:
   - On Windows: `venv\\Scripts\\activate`
   - On macOS/Linux: `source venv/bin/activate`

2. Run the application:
   python app.py

3. Open your browser and go to: http://127.0.0.1:5000/{stubs_text}

## Libraries Used

### Backend (Python)
- Flask 2.3.3
- Werkzeug 2.3.7
- Jinja2 3.1.2

### Frontend (CDN)
- Pure CSS 3.0.0
- Pure CSS Responsive Grids 3.0.0

## Project Structure

{app_name}/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── templates/
│   ├── models/
│   ├── views/
│   └── forms/
│
├── venv/
├── app.py
├── requirements.txt
└── README.md

"""
    
    with open(os.path.join(app_dir, "README.md"), "w") as f:
        f.write(readme_content)
    print(f"Created README.md file")

def setup_virtual_environment(app_dir):
    """Set up a virtual environment and install dependencies."""
    venv_dir = os.path.join(app_dir, "venv")
    print(f"Creating virtual environment at {venv_dir}...")
    
    # Create virtual environment
    try:
        venv.create(venv_dir, with_pip=True)
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        return False
    
    # Determine the path to pip based on the OS
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
        activate_script = os.path.join(venv_dir, "bin", "activate")
    
    # Install dependencies
    requirements_path = os.path.join(app_dir, "requirements.txt")
    print(f"Installing dependencies from {requirements_path}...")
    
    try:
        subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    
    print(f"Virtual environment setup complete. Activate with: {activate_script}")
    return True

def get_build_stats():
    """Get build statistics from the tracker file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tracker_file = os.path.join(script_dir, '.flask_bootstrapper_stats.json')
    
    # Default stats if file doesn't exist
    stats = {
        "build_count": 0,
        "history": []
    }
    
    # Try to load existing stats
    if os.path.exists(tracker_file):
        try:
            with open(tracker_file, 'r') as f:
                stats = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or missing, use default stats
            pass
    
    return stats, tracker_file

def update_build_stats(tracker_file, stats, app_dir):
    """Update build statistics in the tracker file."""
    # Increment build count
    stats["build_count"] += 1
    
    # Get app name from directory
    app_name = os.path.basename(os.path.abspath(app_dir))
    
    # Add new entry to history
    new_entry = {
        "id": stats["build_count"],
        "name": app_name,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "path": app_dir
    }
    
    stats["history"].append(new_entry)
    
    # Save updated stats
    try:
        with open(tracker_file, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"Updated build statistics: App #{stats['build_count']}")
    except Exception as e:
        print(f"Warning: Could not update build statistics: {e}")
    
    return stats

def create_flask_app(app_dir, stubs_count=0):
    """Create a Flask application with the standard structure."""
    # Validate the directory
    if not os.path.exists(app_dir):
        try:
            os.makedirs(app_dir, exist_ok=True)
        except Exception as e:
            print(f"Error: App could not be created due to permission issues or invalid path: {e}")
            return False
    
    if not os.access(app_dir, os.W_OK):
        print(f"Error: App could not be created due to insufficient write permissions for {app_dir}")
        return False
    
    # Get the app name (directory name)
    app_name = os.path.basename(os.path.abspath(app_dir))
    
    # Get build stats
    stats, tracker_file = get_build_stats()
    
    # Update build stats
    stats = update_build_stats(tracker_file, stats, app_dir)
    build_count = stats["build_count"]
    build_history = stats["history"]
    
    print(f"Creating Flask application '{app_name}' (#{build_count}) in {app_dir} with {stubs_count} stub route(s)")
    
    # Create the directory structure
    create_directory_structure(app_dir)
    
    # Create base files
    create_base_template(app_dir, stubs_count)
    create_base_css(app_dir)
    create_base_js(app_dir)
    
    # Create app files
    create_app_file(app_dir, stubs_count)
    create_requirements_file(app_dir)
    create_index_template(app_dir, build_count, build_history)
    create_css_file(app_dir)
    create_js_file(app_dir)
    
    # Create stub files if requested
    if stubs_count > 0:
        create_stub_templates(app_dir, stubs_count)
        create_stub_css_files(app_dir, stubs_count)
        create_stub_js_files(app_dir, stubs_count)
    
    create_gitignore(app_dir)
    create_readme(app_dir, app_name, stubs_count, build_count)
    
    # Set up virtual environment and install dependencies
    venv_success = setup_virtual_environment(app_dir)
    
    if venv_success:
        print("\nFlask application setup complete!")
        print(f"\nCreated app #{build_count} - {app_name}")
        print(f"\nTo run your application:")
        if platform.system() == "Windows":
            print(f"  1. cd {app_dir}")
            print(f"  2. venv\\Scripts\\activate")
        else:
            print(f"  1. cd {app_dir}")
            print(f"  2. source venv/bin/activate")
        print(f"  3. python app.py")
        print(f"\nThen open your browser to: http://127.0.0.1:5000/")
        
        if stubs_count > 0:
            stub_names = ['first', 'second', 'third', 'fourth', 'fifth']
            print("\nStub routes available:")
            for i in range(stubs_count):
                print(f"  - http://127.0.0.1:5000/{stub_names[i]}/index")
        
        return True
    else:
        print("\nFlask application setup completed with errors during virtual environment setup.")
        print("Please check the error messages above and resolve any issues.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create a Flask application with the standard structure.')
    parser.add_argument('--build-dir', type=str, required=True, help='The directory to create the Flask application in')
    parser.add_argument('--stubs', type=int, choices=range(1, 6), default=0, help='Number of stub routes to create (1-5)')
    
    args = parser.parse_args()
    
    success = create_flask_app(args.build_dir, args.stubs)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
