import re
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    stripped_lines = list(map(lambda item: item.strip(), lines))

    blocks = []
    block = ""

    for line in stripped_lines:
        if line != "" and line != " " and line != "  ":
            block = block + "\n" + line
        else:
            if block != "":
                blocks.append(block.lstrip("\n"))
                block =""
    
    if block != "":
        blocks.append(block.strip("\n "))

    return blocks

def check_ordered_list(block):
    lines = block.split("\n")
    
    for x in range(len(lines)):
        if str(x + 1) != lines[x][0] or lines[x][1:3] != ". ":
            return False
    
    return True

def block_to_block_type(markdown_block):
    match markdown_block:
        case markdown_block if re.search(r"^#{1,6} ", markdown_block):
            return block_type_heading
        case markdown_block if markdown_block[:3] == "```" and markdown_block[-3:] == "```":
            return block_type_code
        case markdown_block if markdown_block[0] == ">" and not re.search(r"\n[^>]", markdown_block):
            return block_type_quote
        case markdown_block if (markdown_block[0:2] == "* " or markdown_block[0:2] == "- ") and not re.search(r"\n[^\*-]", markdown_block):
            return block_type_unordered_list
        case markdown_block if check_ordered_list(markdown_block):
            return block_type_ordered_list
        case _:
            return block_type_paragraph


def quote_to_html_node(block):
    nodes = []
    for line in block.split("\n"):
        nodes.extend(list(map(text_node_to_html_node, text_to_textnodes(line.lstrip("> ")))))

    return ParentNode("blockquote", nodes)

def unordered_list_to_html_node(block):
    nodes = []
    for line in block.split("\n"):
        nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(line[2:])))))
    
    return ParentNode("ul", nodes)

def ordered_list_to_html_node(block):
    nodes = []
    for line in block.split("\n"):
        nodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(line[3:])))))

    return ParentNode("ol", nodes)

def code_to_html_node(block):
    return ParentNode("pre", [LeafNode("code", block.strip("`\n"))])

def heading_to_html_node(block):
    lines = block.split("\n")
    nodes = []

    for x in range(len(lines)):
        for y in range(len(lines[x])):
            if lines[x][y] == " ":
                nodes.append(ParentNode(f"h{y}", list(map(text_node_to_html_node, text_to_textnodes(lines[x][y+1:])))))
                break

    return nodes

def paragraph_to_html_node(block):
    nodes = list(map(text_node_to_html_node, text_to_textnodes(block)))
    return ParentNode("p", nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case block_type if block_type == block_type_quote:
                nodes.append(quote_to_html_node(block))
            case block_type if block_type == block_type_unordered_list:
                nodes.append(unordered_list_to_html_node(block))
            case block_type if block_type == block_type_ordered_list:
                nodes.append(ordered_list_to_html_node(block))
            case block_type if block_type == block_type_code:
                nodes.append(code_to_html_node(block))
            case block_type if block_type == block_type_heading:
                nodes.extend(heading_to_html_node(block))
            case _:
                nodes.append(paragraph_to_html_node(block))
    
    return ParentNode("div", nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == block_type_heading:
            for line in block.split("\n"):
                if line.startswith("# "):
                    return line[2:]
    
    raise Exception("Missing Title: no h1 found")