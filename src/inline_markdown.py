from textnode import *
from htmlnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 != 0:
                for x in range(len(split_text)):
                    if split_text[x] != "":
                        if x % 2 == 1:
                            nodes.append(TextNode(split_text[x], text_type))
                        else:
                            nodes.append(TextNode(split_text[x], text_type_text))
            else:
                raise ValueError("Invalid markdown: closing formatter missing")

    return nodes

def extract_markdown_images(text):
    image_markdown =  re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image_markdown

def extract_markdown_links(text):
    link_markdown = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_markdown

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text

        image_tuples = extract_markdown_images(text)

        if node.text_type != text_type_text or len(image_tuples) == 0:
            new_nodes.append(node)
        else:
            for img in image_tuples:
                split_text = text.split(f"![{img[0]}]({img[1]})", 1)
                
                if len(split_text) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                
                new_nodes.append(TextNode(img[0], text_type_image, img[1]))

                text = split_text[1]
            
            if text != "":
                new_nodes.append(TextNode(text, text_type_text))

    return new_nodes

    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text

        link_tuples = extract_markdown_links(text)

        if node.text_type != text_type_text or len(link_tuples) == 0:
            new_nodes.append(node)
        else:
            for link in link_tuples:
                split_text = text.split(f"[{link[0]}]({link[1]})", 1)
                
                if len(split_text) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))

                text = split_text[1]
            
            if text != "":
                new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes