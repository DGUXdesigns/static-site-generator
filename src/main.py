import os
import pathlib
import shutil
import sys

from html_markdown import markdown_to_html_node


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_dir(src: str, dest: str) -> None:
    # 1. Delete destination if it exists (clean build)
    if os.path.exists(dest):
        shutil.rmtree(dest)

    # 2. Recreate destination root
    os.mkdir(dest)

    # 3. Start recursive copy
    _copy_recursive(src, dest)


def _copy_recursive(src: str, dest: str) -> None:
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # it's a directory
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)

            # recurse into subdirectory
            _copy_recursive(src_path, dest_path)


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()

        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No H1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w", encoding="UTF-8") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Make sure the destination directory exists
    pathlib.Path(dest_dir_path).mkdir(parents=True, exist_ok=True)

    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path) and src_path.endswith(".md"):
            # Convert Markdown to HTML
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            print(f"Generating page from {src_path} -> {dest_path}")
            generate_page(src_path, template_path, dest_path, basepath)

        elif os.path.isdir(src_path):
            # Recurse into subdirectory
            generate_pages_recursive(src_path, template_path, dest_path, basepath)


main()
