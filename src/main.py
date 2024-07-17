#!/usr/bin/python3
import os
import shutil

from block_markdown import extract_title, markdown_to_html_node

def copy_dir(source, destination, destination_cleared=False):
    this_file = '~/static-site/src/main.py'
    os.access(this_file, os.F_OK)

    if os.path.exists(destination) and os.path.exists(source):
        if not destination_cleared:
            shutil.rmtree(destination)
            os.mkdir(destination)
            destination_cleared = True
        source_files = os.listdir(source)
        for file in source_files:
            file_path = os.path.join(source, file)
            print(file_path)
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination)
            else:
                os.mkdir(os.path.join(destination, file))
                copy_dir(file_path, os.path.join(destination, file), destination_cleared)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if not os.path.exists(from_path):
        raise Exception("Invalid source path")
    
    source_file = open(from_path, "r")
    template_file = open(template_path, "r")

    markdown = source_file.read()
    template = template_file.read()

    source_file.close()
    template_file.close()

    HTML_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", HTML_content)

    serperate_dest_path = os.path.dirname(dest_path)

    if not os.path.exists(serperate_dest_path):
        os.makedirs(serperate_dest_path)

    with open(dest_path, "w+") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Invalid content path")
    
    content_files = os.listdir(dir_path_content)
    
    for entry in content_files:
        content_file = os.path.join(dir_path_content, entry)
        dest_file = os.path.join(dest_dir_path, entry)

        if os.path.isfile(content_file):
            generate_page(content_file, template_path, dest_file[:-3] + ".html")
        else:
            generate_pages_recursive(content_file, template_path, dest_file)


def main():
    copy_dir("static","public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()