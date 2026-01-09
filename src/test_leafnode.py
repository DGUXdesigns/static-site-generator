import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_Leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<p class="highlight">Hello, world!</p>')

    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, props: None)")
