import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'SELECT',
   'FROM',
   'WHERE',
   'DELIMITER1',
   'DELIMITER2',
   'ATTRIBUTE',
   'NUMBER',
   'OPERATOR'
)

# Regular expression rules for the tokens
t_SELECT    = r'(?i)select'
t_FROM   = r'(?i)from'
t_WHERE   = r'(?i)where'
t_DELIMITER1  = r','
t_DELIMITER2  = r';'
t_OPERATOR = r'(<|>|=)+'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

t_ATTRIBUTE  = r'\w+'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = 'SELECT id, nome, salario FROM empregados WHERE salario>=820'

# Give the lexer some input
lexer.input(data)

for tok in lexer:
    #print(tok)
    print(tok.type, tok.value, tok.lineno, tok.lexpos)