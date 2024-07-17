import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    #Test HTMLNode methods
    def test_props_to_html(self):
        node = HTMLNode("p", "test", [], {"target":"blank"})
        self.assertEqual(node.props_to_html(), "target=\"blank\"")
    
    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "test")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_multiple_props(self):
        node = HTMLNode("p", "test", [], {"href":"https://www.google.com", "target":"blank"})
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"blank\"")
    
    #Test LeafNode methods
    def test_leaf_to_html(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_leaf_to_html_with_props(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    #Test ParentNode methods
    def test_parent_to_html(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_nested_parent_to_html(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                    ]),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b><p>Normal text<i>italic text</i></p>Normal text</p>")
    
    def test_multi_nested_parent_to_html(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [
                               ParentNode("p", [LeafNode(None, "Normal text")]),
                                LeafNode("i", "italic text"),
                            ]),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b><p><p>Normal text</p><i>italic text</i></p>Normal text</p>")
    
    def test_parent_to_html_with_props(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"target":"blank"}
        )
        self.assertEqual(parent.to_html(), "<p target=\"blank\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == "__main__":
    unittest.main()