import os

directories = ['scraper', 'enrichment', 'dashboard', 'utils', 'data']
base_path = os.path.dirname(os.path.abspath(__file__))

for directory in directories:
    dir_path = os.path.join(base_path, directory)
    os.makedirs(dir_path, exist_ok=True)

# Create necessary __init__.py files
for directory in directories:
    init_file = os.path.join(base_path, directory, '__init__.py')
    with open(init_file, 'w') as f:
        pass
