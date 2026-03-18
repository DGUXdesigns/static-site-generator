import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            text_list = node.text.split(delimiter)

            if len(text_list) % 2 == 0:
                raise ValueError("Invalid Markdown: formatted section not closed")

            for i in range(len(text_list)):
                if text_list[i] == "":
                    continue

                if i % 2 != 0:
                    result.append(TextNode(text_list[i], text_type))
                else:
                    result.append(TextNode(text_list[i], TextType.TEXT))
    return result


def extract_markdown_images(text: str) -> list:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(pattern, text)
    return result


def extract_markdown_links(text: str) -> list:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = re.findall(pattern, text)
    return result


def split_nodes_image(old_nodes: list) -> list:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            result.append(old_node)
            continue

        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sections[1]

        if text != "":
            result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list) -> list:
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            result.append(old_node)
            continue

        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]

        if text != "":
            result.append(TextNode(text, TextType.TEXT))

    return result
