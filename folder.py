import os
website_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
print(website_dir)  

# find all file in this folder, subfolder and save it to files.txt
with open('files.txt', 'w') as f:
    for dirpath, dirnames, filenames in os.walk(website_dir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename) + '\n')