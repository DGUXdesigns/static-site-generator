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
