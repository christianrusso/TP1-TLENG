from ast import DivisionNode, ConcatenationNode, \
                SuperindexNode, SubindexNode, SuperSubindexNode, SubSuperindexNode, \
                ParenthesesNode, OperandNode


# E -> E / C
def p_expression_divide(p):
    'expression : expression DIVIDE concatenation'
    p[0] = DivisionNode(p[1], p[3])

# E -> C
def p_expression_concatenation(p):
    'expression : concatenation'
    p[0] = p[1]

# C -> CI
def p_concatenation_concatenation(p):
    'concatenation : concatenation index'
    p[0] = ConcatenationNode(p[1], p[2])

# C -> I
def p_concatenation_index(p):
    'concatenation : index'
    p[0] = p[1]

# I -> A^A
def p_index_superindex(p):
    'index : group SUPERI group'
    p[0] = SuperindexNode(p[1], p[3])

# I -> A_A
def p_index_subindex(p):
    'index : group SUBI group'
    p[0] = SubindexNode(p[1], p[3])

# I -> A^A_A
def p_index_superindex_subindex(p):
    'index : group SUPERI group SUBI group'
    p[0] = SuperSubindexNode(p[1], p[3], p[5])
# I -> A_A^A
def p_index_subindex_superindex(p):
    'index : group SUBI group SUPERI group'
    p[0] = SubSuperindexNode(p[1], p[3], p[5])

# I -> A
def p_index_group(p):
    'index : group'
    p[0] = p[1]

# A -> {E}
def p_group_braces(p):
    'group : LBRACE expression RBRACE'
    p[0] = p[2]

# A -> (E)
def p_group_parentheses(p):
    'group : LPAREN expression RPAREN'
    p[0] = ParenthesesNode(p[2])

# A -> l
def p_group_operand(p):
    'group : OPERAND'
    p[0] = OperandNode(p[1])

def p_error(p):
    print("Syntax error in input!")
