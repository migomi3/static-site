import unittest
from block_markdown import *
from htmlnode import LeafNode


class TestBlockMarkdown(unittest.TestCase):
    #test markdown_to_blocks
    def test_markdown_to_blocks(self):
        text = """This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items"""
        self.assertEqual(markdown_to_blocks(text), [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"])
        
    def test_markdown_to_blocks_one_block(self):
        text = """This is **bolded** paragraph
        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line
        * This is a list
        * with items"""
        self.assertEqual(markdown_to_blocks(text), [
            "This is **bolded** paragraph\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n* This is a list\n* with items"])
    
    def test_markdown_to_blocks_extra_spaced_blocks(self):
        text = """This is **bolded** paragraph


        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line


        * This is a list
        * with items"""
        self.assertEqual(markdown_to_blocks(text), [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"])
    
    #test check_ordered_list
    def test_check_ordered_list(self):
        text = "1. This is **bolded** paragraph"
        self.assertTrue(check_ordered_list(text))
    
    def test_check_ordered_list_multiline(self):
        text = "1. This is a list\n2. with items"
        self.assertTrue(check_ordered_list(text))
    
    def test_check_ordered_list_no_space(self):
        text = "1.This is **bolded** paragraph"
        self.assertFalse(check_ordered_list(text))
    
    def test_check_ordered_list_multiline_out_of_order(self):
        text = "2. This is a list\n1. with items"
        self.assertFalse(check_ordered_list(text))

    #test block_to_block_type
    def test_block_to_block_type(self):
        text = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_heading(self):
        text = "### This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_heading)
    
    def test_block_to_block_type_heading_excess_hashes(self):
        text = "########## This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_heading_no_space(self):
        text = "###This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_heading_multiline(self):
        text = "# This is another paragraph with *italic* text and `code` here\n## This is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_heading)
    
    def test_block_to_block_type_heading_multiline_no_hash_second_line(self):
        text = "# This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_heading)
        
    def test_block_to_block_type_code(self):
        text = "```This is **bolded** paragraph```"
        self.assertEqual(block_to_block_type(text), block_type_code)

    def test_block_to_block_type_code_no_opening(self):
        text = "This is **bolded** paragraph```"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)

    def test_block_to_block_type_code_no_closing(self):
        text = "```This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)

    def test_block_to_block_type_unordered_list(self):
        text = "* This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_unordered_list)
    
    def test_block_to_block_type_unordered_list_excess_stars(self):
        text = "** This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_unordered_list_no_space(self):
        text = "*This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_unordered_list_multiline(self):
        text = "* This is another paragraph with *italic* text and `code` here\n* This is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_unordered_list)
    
    def test_block_to_block_type_unordered__multiline_no_star_second_line(self):
        text = "* This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)

    def test_block_to_block_type_unordered_list_dash(self):
        text = "- This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_unordered_list)
    
    def test_block_to_block_type_unordered_list_excess_dashes(self):
        text = "-- This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_unordered_list_dash_no_space(self):
        text = "-This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_unordered_list_multiline_dash(self):
        text = "- This is another paragraph with *italic* text and `code` here\n- This is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_unordered_list)
    
    def test_block_to_block_type_unordered__multiline_no_dash_second_line(self):
        text = "- This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)

    def test_block_to_block_type_ordered_list(self):
        text = "1. This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_ordered_list)
    
    def test_block_to_block_type_ordered_list_negative(self):
        text = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), block_type_paragraph)
    
    def test_block_to_block_type_ordered_list_multiline(self):
        text = "1. This is another paragraph with *italic* text and `code` here\n2. This is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), block_type_ordered_list)

    #test quote_to_html_node
    def test_quote_to_html_node(self):
        text = "> This is **bolded** paragraph"
        node = quote_to_html_node(text)
        self.assertEqual(str(node), str(ParentNode("blockquote", [LeafNode(None, "This is "), LeafNode("b", "bolded"), LeafNode(None, " paragraph")])))
    
    #test unordered_list_to_html_node
    def test_unordered_list_to_html_node(self):
        text = "- This is **bolded** paragraph"
        node = unordered_list_to_html_node(text)
        self.assertEqual(node.to_html(), "<ul><li>This is <b>bolded</b> paragraph</li></ul>")

    def test_unordered_list_to_html_node_multilined(self):
        text = "* test\n* test2"
        node = unordered_list_to_html_node(text)
        self.assertEqual(node.to_html(), "<ul><li>test</li><li>test2</li></ul>")
    
    #test ordered_list_to_html_node
    def test_ordered_list_to_html_node(self):
        text = "1. This is **bolded** paragraph"
        node = ordered_list_to_html_node(text)
        self.assertEqual(node.to_html(), "<ol><li>This is <b>bolded</b> paragraph</li></ol>")

    def test_ordered_list_to_html_node_multilined(self):
        text = "1. test\n2. test2"
        node = ordered_list_to_html_node(text)
        self.assertEqual(node.to_html(), "<ol><li>test</li><li>test2</li></ol>")
    
    #test code_to_html_node
    def test_code_to_html_node(self):
        text = "```This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line```"
        node = code_to_html_node(text)
        self.assertEqual(str(node), str(ParentNode("pre", [LeafNode("code", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line")])))

    #test heading_to_html_node
    def test_heading_to_html_node(self):
        text = "### This is **bolded** paragraph"
        nodes = heading_to_html_node(text)
        html_text = list(map(lambda node: node.to_html(), nodes))
        self.assertEqual(str(html_text), "['<h3>This is <b>bolded</b> paragraph</h3>']")
    
    def test_heading_to_html_node_mutiline(self):
        text = "# This is another paragraph with *italic* text and `code` here\n## This is the same paragraph on a new line"
        nodes = heading_to_html_node(text)
        html_text = list(map(lambda node: node.to_html(), nodes))
        self.assertEqual(str(html_text), "['<h1>This is another paragraph with <i>italic</i> text and <code>code</code> here</h1>', '<h2>This is the same paragraph on a new line</h2>']")

    #test paragraph_to_html_node
    def test_paragraph_to_html_node(self):
        text = "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
        node = paragraph_to_html_node(text)
        self.assertEqual(node.to_html(), "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here\nThis is the same paragraph on a new line</p>")

    #test markdown_to_html_node
    def test_markdown_to_html_node(self):
        markdown = """### This is **bolded** paragraph

        > This is a blockquote

        ```This is code
        fuckThis()```"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><h3>This is <b>bolded</b> paragraph</h3><blockquote>This is a blockquote</blockquote><pre><code>This is code\nfuckThis()</code></pre></div>")
    
    def test_markdown_to_html_node_pt2(self):
        markdown = """* This is a list
        * with items

        - with items

        1. This is a list
        2. with items
        
        Simple Paragraph"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ul><li>This is a list</li><li>with items</li></ul><ul><li>with items</li></ul><ol><li>This is a list</li><li>with items</li></ol><p>Simple Paragraph</p></div>")
    
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_extract_title_multi_line(self):
        self.assertEqual(extract_title("# Hello\n## bullshit"), "Hello")

if __name__ == "__main__":
    unittest.main()