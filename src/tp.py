# tp.py
from lexer_rules import *
from parser_rules import *
from ply.lex import lex
from ply.yacc import yacc
import sys
import svgwrite
#import cairosvg

lexer = lex()
parser = yacc()

for line in sys.stdin: 
    try:
        result = parser.parse(line, lexer)
        result.first_traversal()
        result.second_traversal()
        #print result.repr()

        # generate SVG document
        svg_doc = svgwrite.Drawing(filename="formula.svg")
        g = svg_doc.g(transform="translate(0, {})".format(result.h_top + result.h_bottom), 
            style="font-family:Courier")
        result.svg(svg_doc, g)
        svg_doc.add(g)
        #svg_doc.save()
        print svg_doc.tostring()
    except Exception as e:
        pass
