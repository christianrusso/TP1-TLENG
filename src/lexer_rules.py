tokens = (
    'SUPERI',
    'SUBI',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'OPERAND',
)

t_SUPERI        = r'\^'
t_SUBI          = r'_'
t_DIVIDE        = r'/'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'{'
t_RBRACE        = r'}'
t_OPERAND       = r'[^\^_/{}\(\)]'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise Exception('ILLEGAL CHARACTER')
    t.lexer.skip(1)
