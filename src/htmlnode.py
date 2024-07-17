class HTMLNode:
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        props = ""
        for key, value in self.props.items():
            props += f"{key}=\"{value}\" "
        return props.rstrip(" ")
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,  tag=None, value=None, props={}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: No value")
        if self.tag == None:
            return self.value
        
        if len(self.props) != 0:
            return f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: No tag")
        if self.children == None:
            raise ValueError("Invalid HTML: No children")
        
        kids = ""

        for node in self.children:
            kids += node.to_html()

        if self.props != None and len(self.props) != 0:
            return f"<{self.tag} {super().props_to_html()}>{kids}</{self.tag}>"

        return f"<{self.tag}>{kids}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"