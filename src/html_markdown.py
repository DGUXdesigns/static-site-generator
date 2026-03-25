import re

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from util import text_to_textnodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                text = " ".join(lines)
                block_node_children = text_to_children(text)
                block_node = ParentNode("p", block_node_children)
                children.append(block_node)
            case BlockType.HEADING:
                i = 0
                while block[i] == "#":
                    i += 1

                text = block[i + 1 :]
                block_node_children = text_to_children(text)
                block_node = ParentNode(f"h{i}", block_node_children)
                children.append(block_node)
            case BlockType.CODE:
                lines = block.split("\n")
                stripped = lines[1:-1]
                text = ""

                for strip in stripped:
                    text += strip + "\n"

                block_text_node = TextNode(text, TextType.CODE)
                block_node = ParentNode(
                    "pre", [text_node_to_html_node(block_text_node)]
                )
                children.append(block_node)
            case BlockType.QUOTE:
                lines = block.split("\n")
                stripped = [line.removeprefix(">").strip() for line in lines]
                text = " ".join(stripped)

                block_node_children = text_to_children(text)
                block_node = ParentNode("blockquote", block_node_children)
                children.append(block_node)
            case BlockType.ULIST:
                lines = block.split("\n")
                items = []
                for line in lines:
                    text = strip_unordered_list_prefix(line)
                    items.append(ParentNode("li", text_to_children(text)))
                block_node = ParentNode("ul", items)
                children.append(block_node)
            case BlockType.OLIST:
                lines = block.split("\n")
                items = []
                for line in lines:
                    text = strip_ordered_list_prefix(line)
                    items.append(ParentNode("li", text_to_children(text)))
                block_node = ParentNode("ol", items)
                children.append(block_node)

    return ParentNode("div", children)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children


def strip_ordered_list_prefix(line: str) -> str:
    return re.sub(r"^\s*\d+\.\s+", "", line)


def strip_unordered_list_prefix(line: str) -> str:
    return re.sub(r"^\s*[-*+]\s+", "", line)


# Testing
md = """
1. This is text that _should_ remain
2. the **same** even with inline stuff
3. item 3
"""

if __name__ == "__main__":
    markdown_to_html_node(md)
