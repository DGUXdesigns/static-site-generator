import os
import shutil

from html_markdown import markdown_to_html_node


def main():
    copy_dir("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    updated_template = template_content.replace("{{ Title }}", title)
    final_template = updated_template.replace("{{ Content }}", html_string)

    with open(dest_path, "w", encoding="UTF-8") as f:
        f.write(final_template)


main()
