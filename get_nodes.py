from html.parser import HTMLParser
import argparse

class MyHTMLParser(HTMLParser):
    in_class = False
    in_args = False
    getting_id = False
    parsing_node = ""
    nodes = []

    def handle_starttag(self, tag, attrs):
        if tag == 'dt' and attrs and attrs[0][0] == 'id':
            self.in_class = True 
        
        elif tag == 'code' and self.in_class:
            self.getting_id = True
            
            # self.parsing_node = attrs[0][1]
        
        elif tag == 'span' and ('class', 'sig-paren') in attrs and not self.in_args:
            self.in_args = True
            self.parsing_node += "("
            

        # elif tag == 'span' and ('class', 'sig-paren') in attrs and self.in_args:
            # self.parsing_node += ")"

    def handle_endtag(self, tag):
        pass
        # if tag == 'dl':
        #     self.in_class = False
        if tag == 'dt' and self.in_class:
            self.in_args = False
            self.in_class = False
            if "(" not in self.parsing_node:
                self.parsing_node += "()"

            self.nodes.append(self.parsing_node)
            self.parsing_node = ""

    def handle_data(self, data):
        if self.getting_id:
            self.parsing_node = data
            self.getting_id = False

        elif data == ")" and self.in_args:
            self.parsing_node = self.parsing_node[:-2] + data
            
        elif self.in_args and data not in ["(", ")", ", "]:
            # filter out the paragraph character
            if data != "\xc2\xb6":
                self.parsing_node += data + ", "
        


parser = argparse.ArgumentParser(prog='get_nodes', description="get ast_type python nodes from documentation page",
                                     usage="python get_nodes <doc.html>")
parser.add_argument('filename', type=str)

if __name__ == '__main__':
    
    args = parser.parse_args()
    html = ""
    
    with open(args.filename, "r") as f:
        html = f.read()
    

    html_parser = MyHTMLParser()

    html_parser.feed(html)
    # print html_parser.nodes
    print ''.join(x + "\n" for x in html_parser.nodes),