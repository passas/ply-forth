import ply.lex as lex
import re

reservados = {
# t.value : t.type
    'MOD' : 'MOD',

    'IF' : 'IF',
    'ELSE' : 'ELSE',
    'THEN' : 'THEN',
    
    'DO' : 'DO',
    'LOOP' : 'LOOP',
    '+LOOP' : 'MAIS_LOOP',
    
    'I' : 'I',
    'J' : 'J',
    
    'BEGIN' : 'BEGIN',
    'UNTIL' : 'UNTIL',
    'WHILE' : 'WHILE',
    'REPEAT' : 'REPEAT',

    'DUP' : 'DUP',
    'DROP' : 'DROP',
    
    'EMIT' : 'EMIT',
}

tokens = (

    'PONTO',  

    'INT',

    'CHAR',
    'EMIT',
    'STRING',
    'CR',


    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',

    'DUP',
    'DROP',

    'KEYWORD',

    'START_FUNC',
    'END_FUNC',

    'IF',
    'ELSE',
    'THEN',

    'DO',
    'LOOP',
    'MAIS_LOOP',
    'INT_MAIS_LOOP',
    'I',
    'J',

    'BEGIN',
    'UNTIL',
    'WHILE',
    'REPEAT',

    'IGUAL',
    'DIFERENTE',
    'MENOR',
    'SUPERIOR',
    'ZERO_IGUAL',
    'NEGATIVO',
    'POSITIVO',

    'VARIABLE',
    'STORE',
    'FETCH',
    'SHOW',
    'INC',

    'ARRAY',
    'ARRAYSTORE',
    'ARRAYFETCH',
    'ARRAYSHOW',

    'COMMENT',

    )

t_IGUAL = r'='
t_DIFERENTE = r'<>'
t_MENOR = r'<'
t_SUPERIOR = r'>'
t_ZERO_IGUAL = r'0='    #compete com o INT
t_NEGATIVO = r'0<'      #compete com o INT
t_POSITIVO = r'0>'      #compete com o INT


def t_STORE (t):
    r'(-?\d+)\s([a-zA-Z][a-zA-Z0-9]+)\s!'

    return (t)

def t_INT_MAIS_LOOP (t):
    r'(-?\d+)\s?\+LOOP'            #compete com o INT
    return (t)

def t_INT (t):
    r'-?\d+'            #compete com o SUB
    return (t)

t_MAIS_LOOP = r'\+LOOP' #compete com o ADD

t_ADD = r'\+'           
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'

##############
def t_MOD (t):
    #compete com o KEYWORD
    r'%'
    return (t)
##############

#################
def t_COMMENT (t):
    r'\(.*?\)'
    return (t)
##############

#################
def t_STRING (t):
    r'\."(.*?)"'

    ##### ambush ############################
    string = re.search (r'\."(.*)"', t.value)
    t.value = string.group(1)
    #########################################
    return (t)
##############

t_PONTO = r'\.'

t_START_FUNC = r':'
t_END_FUNC = r';'

t_I = r'I'
t_J = r'J'

#############
def t_CR (t):
    r'CR'
    return (t)

################
def t_ARRAY (t):
    r'VARIABLE\s([a-zA-Z][a-zA-Z0-9]+)\s+(\d+)\sCELLS\sALLOT'
    mo = re.search (r'VARIABLE\s([a-zA-Z][a-zA-Z0-9]+)\s+(\d+)\sCELLS\sALLOT', t.value)
    t.value = ( mo.group (1), mo.group(2) )
    return (t)
###################
def t_VARIABLE (t):
    r'VARIABLE\s([a-zA-Z][a-zA-Z0-9]+)'
    mo = re.search (r'VARIABLE\s([a-zA-Z][a-zA-Z0-9]+)', t.value)
    t.value = mo.group (1)
    return (t)
#####################
def t_ARRAYSTORE (t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s!'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s!', t.value)
    t.value = ( mo.group (1), mo.group(2) )
    return (t)
#####################
def t_ARRAYFETCH (t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s@'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s@', t.value)
    t.value = ( mo.group (1), mo.group(2) )
    return (t)
####################
def t_ARRAYSHOW (t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s\?'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s(\d+)\sCELLS\s\+\s\?', t.value)
    t.value = ( mo.group (1), mo.group(2) )
    return (t)
################
def t_FETCH (t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s@'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s@', t.value)
    t.value = mo.group (1)
    return (t)
##############
def t_SHOW(t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s\?'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s\?', t.value)
    t.value = mo.group (1)
    return (t)
##############
def t_INC(t):
    r'([a-zA-Z][a-zA-Z0-9]+)\s\+!'
    mo = re.search (r'([a-zA-Z][a-zA-Z0-9]+)\s!', t.value)
    t.value = mo.group (1)
    return (t)
##############

######################################################
## sem def passa à frente de todos os outros tokens ##
######################################################
def t_KEYWORD (t):                                   #
    r'[a-zA-Z][a-zA-Z0-9]+'                          #
                                                     #
    ##### ambush ############                        #
    if t.value in reservados:                        #
        t.type = reservados[ t.value ]               #
    #########################                        #
                                                     #
    return (t)                                       #
######################################################

###############
def t_CHAR (t):
    r'\[CHAR\]\s?([!-~])'

    mo = re.search ( r'\[CHAR\]\s?([!-~])', t.value)
    t.value = mo.group(1)
    
    return (t)
##############

t_ignore = ' \t'

##################
def t_NEWLINE (t):
    r'\n'
    t.lexer.lineno += 1

    global LEXCOLUNA
    LEXCOLUNA = t.lexer.lexpos
    
    pass
##################

def t_error (t):
    print ("t_error")
    print (t)
    t.lexer.skip(1)

lexer = lex.lex()
LEXCOLUNA = 0