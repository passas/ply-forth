from lex import tokens
import ply.yacc as yacc
import sys
import re

import lex  #lex.LEXCOLUNA


###################
def p_Programa (p):
    'Programa : Instrucoes'

    ### Ambush #############
    if parser.exito == True and parser.erro == False:

        ## Warnings ########
        if parser.banco > 0:
            parser.erros.append (f"Warning: O programa pode deixar {parser.banco} operando(s) em Stack...")
        ####################

        p[0] = "Start\n"
        p[0] += p[1] + "\n"
        ## Heap #################
        if parser.my_heap > 0:
            p[0] += "frees:\n"
            while parser.my_heap > 0:
                p[0] += "\t" + "popst" + "\n"
                parser.my_heap -= 1
        #########################
        p[0] += "Stop"


        # EWVM #######
        parser.compilacao = p[0]
        ##############
    
    ########################
    return (p)
#####################
def p_Instrucoes (p):
    'Instrucoes : Instrucoes Instrucao'

    p[0] = p[1] + "\n"
    p[0] += p[2]

    return (p)
######################
def p_Instrucoes_ (p):
    'Instrucoes : Instrucao'
    
    p[0] = p[1]

    return (p)
####################
def p_Instrucao (p):
    '''
    Instrucao : Operando
              | Operador
              | Keyword
              | Funcao
              | Condicao
              | Loop
              | Variavel
              | Store
              | Fetch
              | Show
              | Inc
              | Array
              | ArrayStore
              | ArrayFetch
              | ArrayShow
              | Comment
    '''

    p[0] = p[1]

    return (p)
###################
def p_Operando (p):
    '''
    Operando : Int
             | Char
             | String
             | i
             | j
             | Cr
    '''

    p[0] = p[1]

    return (p)
#.............
def p_Int (p):
    'Int : INT'

    ## Stack ####
    calcula_saldo ('INT')
    #############

    p[0] = "\t" + "pushi" + " " + p[1]

    ## +LOOP #########################
    parser.mais_loop_op = int ( p[1] )
    ##################################

    return (p)
#..............
def p_Char (p):
    'Char : CHAR'

    codigo_ascii = ord ( p[1] ) # char -> int
    p[0] = "\t" + "pushi" + " " + str (codigo_ascii)

    ## Stack ####
    calcula_saldo ('INT')
    #############

    return (p)
#................
def p_String (p):
    'String : STRING'

    p[0] = "\t" + "pushs" + "  " + "\""+p[1]+"\"" + "\n"
    p[0] += "\t" + "writes"

    return (p)
#...........
def p_i (p):
    'i : I'
    
    if len (parser.stack_loop_labels) == 0:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável fora de um ciclo DO ... [+]LOOP!\n  {p.lineno(1)}|\t{p[1]}")
        parser.exito = False
        p[0] = ""
    else:
        ## Endereco #####################################################
        endereco = "<0xf+" + str ( len (parser.stack_loop_labels) - 1 ) + ">"
        #################################################################
    
        ## DO ################################
        p[0] = "\t" + "pushst" + " " + endereco + "\n"
        p[0] += "\t" + "load 0"
    
        ## Stack ####
        calcula_saldo ('I')
        #############

    return (p)
#...........
def p_j (p):
    'j : J'
    
    if len (parser.stack_loop_labels) == 0:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável fora de um ciclo DO ... [+]LOOP!\n  {p.lineno(1)}|\t{p[1]}")
        parser.exito = False
        p[0] = ""
    else:
        ## Endereco #####################################################
        endereco = "<0xf+" + str ( len (parser.stack_loop_labels) - 2 ) + ">"
        #################################################################
    
        ## DO DO ##############################
        p[0] = "\t" + "pushst" + " " + endereco + "\n"
        p[0] += "\t" + "load 0"
    
        ## Stack ####
        calcula_saldo ('J')
        #############

    return (p)
#############
def p_Cr (p):
    'Cr : CR'

    p[0] = "\t" + "writeln"

    return (p)
###################
def p_Operador (p):
    '''
    Operador : Add
             | Sub
             | Mul
             | Div
             | Mod
             | Igual
             | Diferente
             | Menor
             | Superior
             | Zero_Igual
             | Negativo
             | Positivo
             | Ponto
             | Dup
             | Drop
             | Emit

    '''

    p[0] = p[1]

    return (p)
#.............
def p_Add (p):
    'Add : ADD'

    ## Stack #####
    calcula_saldo ('ADD', p.lineno(1), p.lexpos(1), p[1])
    ##############

    p[0] = "\t" + "add"

    return (p)
#.............
def p_Sub (p):
    'Sub : SUB'

    ## Stack ####
    calcula_saldo ('SUB',  p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "sub"

    return (p)
#.............
def p_Mul (p):
    'Mul : MUL'

    ## Stack ####
    calcula_saldo ('MUL')
    #############

    p[0] = "\t" + "mul"

    return (p)
#.............
def p_Div (p):
    'Div : DIV'

    ## Stack ####
    calcula_saldo ('DIV', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "div" + "\n"
    p[0] += "\t" + "ftoi"

    return (p)
#.............
def p_Mod (p):
    'Mod : MOD'

    ## Stack ####
    calcula_saldo ('MOD', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "mod"

    return (p)
#...............
def p_Igual (p):
    'Igual : IGUAL'

    ## Stack ####
    calcula_saldo ('IGUAL', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "equal"

    return (p)
#...................
def p_Diferente (p):
    'Diferente : DIFERENTE'

    ## Stack ####
    calcula_saldo ('DIFERENTE', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "equal" + "\n"
    p[0] += "\t" + "not"

    return (p)
#...............
def p_Menor (p):
    'Menor : MENOR'

    ## Stack ####
    calcula_saldo ('MENOR', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "inf"

    return (p)
#..................
def p_Superior (p):
    'Superior : SUPERIOR'

    ## Stack ####
    calcula_saldo ('SUPERIOR', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "sup"

    return (p)
#....................
def p_Zero_Igual (p):
    'Zero_Igual : ZERO_IGUAL'

    ## Stack ####
    calcula_saldo ('ZERO_IGUAL', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "pushi 0" + "\n"
    p[0] += "\t" + "equal"

    return (p)
#..................
def p_Negativo (p):
    'Negativo : NEGATIVO'

    ## Stack ####
    calcula_saldo ('NEGATIVO', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "pushi 0" + "\n"
    p[0] += "\t" + "inf"

    return (p)
#..................
def p_Positivo (p):
    'Positivo : POSITIVO'

    ## Stack ####
    calcula_saldo ('POSITIVO', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "pushi 0" + "\n"
    p[0] += "\t" + "sup"

    return (p)
#...............
def p_Ponto (p):
    'Ponto : PONTO'

    ## Stack ####
    calcula_saldo ('PONTO', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "writei" + "\n"
    p[0] += "\t" + "pushi 32" + "\n"
    p[0] += "\t" + "writechr"

    return (p)
#.............
def p_Dup (p):
    'Dup : DUP'

    ## Stack ####
    calcula_saldo ('DUP', p.lineno(1), p.lexpos(1), p[1])
    #############

    p[0] = "\t" + "dup 1"

    return (p)
#..............
def p_Drop (p):
    'Drop : DROP'

    p[0] = "\t" + "pop 1"

    ## Stack ####
    calcula_saldo ('DROP', p.lineno(1), p.lexpos(1), p[1])
    #############

    return (p)
#..............
def p_Emit (p):
    'Emit : EMIT'

    p[0] = "\t" + "writechr"

    ## Stack ####
    calcula_saldo ('EMIT', p.lineno(1), p.lexpos(1), p[1])
    #############

    return (p)
##################
def p_Keyword (p):
    'Keyword : KEYWORD'

    ## Stack ####
    calcula_saldo (p[1], p.lineno(1), p.lexpos(1), p[1])
    #############

    ## Pull Def. #
    p[0] = assemble_func (p[1])
    ##############
    
    return (p)
#################
def p_Funcao (p):
    'Funcao : Start_Func Instrucoes End_Func'
    
    ## ambush ######
    if parser.exito == True:
        nome, _, _ = parser.stack_construtor.pop()

        ## ambush2 #################
        if nome in parser.variaveis:
            parser.variaveis.remove (nome)
        ############################
        
        ## Custo #########
        if parser.if_flag:
            parser.custos [ nome ] = ( 0, 0, parser.heap_alloc ) #untreaceable
            parser.if_flag = False
            parser.do_flag = False
        elif parser.do_flag:
            parser.custos [ nome ] = ( parser.divida_construtor, 0, parser.heap_alloc ) #untreaceable
            parser.do_flag = False
        else:
            parser.custos [ nome ] = ( parser.divida_construtor, parser.banco_construtor, parser.heap_alloc )
        #################
        
        ## learn ###
        parser.dicionario [ nome ] = p[2]
        ############

    ################

    p[0] = ""

    return (p)
#....................
def p_Start_Func (p):
    'Start_Func : START_FUNC KEYWORD'

    #### ambush ######################
    if len (parser.stack_construtor) == 0:

        ## construtor: activate ####
        parser.stack_construtor.append ( (p[2], p.lineno(1), p.lexpos(1)) )
        ############################

        ## construtor: activate ####
        parser.divida_construtor = 0
        parser.banco_construtor = 0
        ############################

        ## loop: reset ######
        parser.heap_alloc = 0
        #####################

    #><><><><><><><><><><><><><><><><>
    elif len (parser.stack_construtor) >= 1:
        parser.erros. append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Tentativa de definição dentro de uma definição!\n  {p.lineno(1)}|\t{parser.stack_construtor[0][1]}:{parser.stack_construtor[0][2]} {parser.stack_construtor[0][0]} {p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA} {p[2]}")
        parser.exito = False
        parser.stack_construtor.append ( (p[2], p.lineno(1), p.lexpos(1) - lex.LEXCOLUNA) )
    ##################################

    p[0] = p[2]

    return (p)
#..................
def p_End_Func (p):
    'End_Func : END_FUNC'

    #### ambush #####################
    if len (parser.stack_construtor) > 1:
        nome, linha, coluna = parser.stack_construtor.pop()
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Função {nome} não definida!\n  {p.lineno(1)}|\t{nome}")
        parser.exito = False
    #><><><><><><><><><><><><><><><><
    elif parser.exito == False:
        nome, linha, coluna = parser.stack_construtor.pop()
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Função {nome} não definida!\n  {p.lineno(1)}|\t{nome}")
    #################################

    return (p)
###################
def p_Condicao (p):
    'Condicao : If Instrucoes Then'

    ## Label ###################################
    then_label = parser.stack_then_labels.pop ()
    ############################################

    ## False ###################################
    p[0] = "\t" + "jz" + " " + then_label + "\n"
    ############################################
    
    ## True ###########
    p[0] += p[2] + "\n"
    p[0] += "\t" + "jump" + " " + then_label + "\n"
    ###############################################

    ## Then ####
    p[0] += p[3]
    ############

    return (p)
#............
def p_If (p):
    'If : IF'

    ## Outside a Definition? #######
    if parser.stack_construtor == 0:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Tentativa de IF fora de uma função!\n  {p.lineno(1)}|\tIF")
    ################################

    parser.if_flag = True

    ## Stack ####
    calcula_saldo ( 'IF' )
    #############

    return (p)
#..............
def p_Then (p):
    'Then : THEN'

    ## Outside a Definition? #######
    if parser.stack_construtor == 0:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Tentativa de {p[1]} fora de uma função!\n  {p.lineno(1)}|\t{p[1]}")
    ################################

    ## Label #################################
    label = "then" + str (parser.label_then_n)
    parser.stack_then_labels.append ( label )
    parser.label_then_n += 1
    ########################

    p[0] = label + ":"

    return (p)
####################
def p_Condicao_ (p):
    'Condicao : If Instrucoes Else Instrucoes Then'
    
    ## Label's ################################
    then_label = parser.stack_then_labels.pop()
    else_label = parser.stack_else_labels.pop()
    ###########################################

    ## False ###################################
    p[0] = "\t" + "jz" + " " + else_label + "\n"
    ############################################

    ## True  ##########
    p[0] += p[2] + "\n"
    p[0] += "\t" + "jump" + " " + then_label + "\n"
    ###############################################
    
    ## Else ###########
    p[0] += p[3] + "\n"
    p[0] += p[4] + "\n"
    ###################

    ## Then ####
    p[0] += p[5]
    ############

    ## Outside a Definition? #######
    if parser.stack_construtor == 0:
        parser.exito = False
    ################################

    return (p)
#..............
def p_Else (p):
    'Else : ELSE'

    ## Label ##################################
    label =  "else" + str (parser.label_else_n)
    parser.stack_else_labels.append ( label )
    parser.label_else_n += 1
    ########################

    p[0] = label + ":"

    return (p)
###############
def p_Loop (p):
    'Loop : Do Instrucoes LOOP'

    ## Label's ################################
    loop_label = parser.stack_loop_labels.pop()
    loop_start = loop_label + "start"
    loop_cond = loop_label + "cond"
    loop_body = loop_label + "body"
    loop_inc = loop_label + "inc"
    loop_fim = loop_label + "fim"
    ########################

    ## Endereco #####################################################
    endereco = "<0xf+" + str ( len (parser.stack_loop_labels) ) + ">"
    #################################################################

    ## Begin #####################
    p[0] = loop_start + ":" + "\n"
    ##############################

    ## Alloc. ####################
    p[0] += "\t" + "alloc 3" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    #############################

    p[0] += "\n"
    ## 0: I ############################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    p[0] += "\n"
    ## 1: Limit ########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 1" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    p[0] += "\n"
    ## 2: Step #########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushi 1" + "\n"
    p[0] += "\t" + "store 2" + "\n"
    ###############################


    p[0] += "\n"
    ## Cond. #####################
    p[0] += loop_cond + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 1" + "\n"
    p[0] += "\t" + "inf" + "\n"
    p[0] += "\t" + "jz" + " " + loop_fim + "\n" 
    ###########################################

    p[0] += "\n"
    ## Body ######################
    p[0] += loop_body + ":" + "\n"
    p[0] += p[2] + "\n"
    ###################

    p[0] += "\n"
    ## Inc. #####################
    p[0] += loop_inc + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 2" + "\n"
    p[0] += "\t" + "add" + "\n"
    p[0] += "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "jump" + " " + loop_cond + "\n"
    ##############################################

    p[0] += "\n"
    ## End ###############
    p[0] += loop_fim + ":"
    ######################

    return (p)
#............
def p_Do (p):
    'Do : DO'

    ## DO ###############
    parser.do_flag = True
    #####################

    ## Heap ##############
    parser.heap_alloc += 1
    ######################

    ## Label ##################################
    label =  "loop" + str (parser.label_loop_n)
    parser.stack_loop_labels.append ( label )
    parser.label_loop_n += 1
    ########################

    ## Stack ####
    calcula_saldo ('DO')
    #############

    return (p)
#################
def p_Loop_0 (p):
    'Loop : Do Instrucoes INT_MAIS_LOOP'

    ## Label's ################################
    loop_label = parser.stack_loop_labels.pop()
    loop_start = loop_label + "start"
    loop_cond = loop_label + "cond"
    loop_body = loop_label + "body"
    loop_inc = loop_label + "inc"
    loop_fim = loop_label + "fim"
    ########################

    ## Endereco #####################################################
    endereco = "<0xf+" + str ( len (parser.stack_loop_labels) ) + ">"
    #################################################################

    ## Start #####################
    p[0] = loop_start + ":" + "\n"
    ##############################

    ## Alloc. ####################
    p[0] += "\t" + "alloc 3" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    #############################

    ## 0: I ############################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    ## 1: Limit ########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 1" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    ## Step + ################################
    mo = re.search (r'(-?\d+)\s?\+LOOP', p[3])
    p[3] = mo.group (1)
    ###################
    ## 2: Step #########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushi" + " " + p[3] + "\n"
    p[0] += "\t" + "store 2" + "\n"
    ###############################

    ## Cond. #####################
    p[0] += loop_cond + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst 0" + "\n"
    p[0] += "\t" + "load 1" + "\n"
    if int (p[3]) < 0:
        p[0] += "\t" + "sup" + "\n"
    else:
        p[0] += "\t" + "inf" + "\n"
    p[0] += "\t" + "jz" + " " + loop_fim + "\n" 
    ###########################################

    ## Body ######################
    p[0] += loop_body + ":" + "\n"
    p[0] += p[2] + "\n"
    ###################

    ## Inc. #####################
    p[0] += loop_inc + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 2" + "\n"
    p[0] += "\t" + "add" + "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "jump" + " " + loop_cond + "\n"
    ##############################################

    ## End ###############
    p[0] += loop_fim + ":"
    ######################


    return (p)
#################
def p_Loop_1 (p):
    'Loop : Do Instrucoes MAIS_LOOP'

    ## Endereco #####################################################
    endereco = "<0xf+" + str ( len (parser.stack_loop_labels) ) + ">"
    #################################################################

    ## Label's ################################
    loop_label = parser.stack_loop_labels.pop()
    loop_start = loop_label + "start"
    loop_cond = loop_label + "cond"
    loop_body = loop_label + "body"
    loop_inc = loop_label + "inc"
    loop_fim = loop_label + "fim"
    ########################

    p[0] = loop_start + ":" + "\n"

    ## Alloc. #####################
    p[0] += "\t" + "alloc 3" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    #############################

    ## 0: I ############################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    ## 1: Limit ########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 1" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    ###############################

    ## 2: Step #########################
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushsp" + "\n"
    p[0] += "\t" + "load -1" + "\n"
    p[0] += "\t" + "store 2" + "\n"
    p[0] += "\t" + "pop 1" + "\n"
    #############################

    ## Cond. #####################
    p[0] += loop_cond + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst 0" + "\n"
    p[0] += "\t" + "load 1" + "\n"
    if parser.mais_loop_op < 0:
        p[0] += "\t" + "sup" + "\n"
    else:
        p[0] += "\t" + "inf" + "\n"
    p[0] += "\t" + "jz" + " " + loop_fim + "\n" 
    ###########################################

    ## Body ######################
    p[0] += loop_body + ":" + "\n"
    p[0] += p[2] + "\n"
    ###################

    ## Inc. #####################
    p[0] += loop_inc + ":" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 0" + "\n"
    p[0] += "\t" + "pushst" + " " + endereco + "\n"
    p[0] += "\t" + "load 2" + "\n"
    p[0] += "\t" + "add" + "\n"
    p[0] += "\t" + "store 0" + "\n"
    p[0] += "\t" + "jump" + " " + loop_cond + "\n"
    ##############################################

    ## End ###############
    p[0] += loop_fim + ":"
    ######################

    ## Stack ####
    calcula_saldo ('+LOOP')
    #############

    return (p)
#################
def p_Loop__ (p):
    'Loop : Begin Instrucoes UNTIL'

    ## Label's ################################
    loop_label = parser.stack_loop_labels.pop()
    loop_do = loop_label + "do"
    ###########################

    ## DO #####################
    p[0] = loop_do + ":" + "\n"
    p[0] += p[1] + "\n"
    ###################

    ## Until ######################
    p[0] += "\t" + "pushi 0" + "\n"
    p[0] += "\t" + "equal" + "\n"
    p[0] += "\t" + "not" + "\n"
    p[0] += "\t" + "jz" + " " + loop_do
    ################################### 


    return (p)
#...............
def p_Begin (p):
    'Begin : BEGIN'

    ## Label ##################################
    label =  "loop" + str (parser.label_loop_n)
    parser.stack_loop_labels.append ( label )
    parser.label_loop_n += 1
    ########################
    
    return (p)
##################
def p_Loop___ (p):
    'Loop : Begin Instrucoes WHILE Instrucoes REPEAT'

    ## Label's ################################
    loop_label = parser.stack_loop_labels.pop()
    loop_begin = loop_label + "begin"
    loop_do = loop_label + "do"
    loop_fim = loop_label + "fim"
    #############################

    ## DO ########################
    p[0] = loop_begin + ":" + "\n"
    p[0] += p[1] + "\n"
    ###################

    ## While ######################
    p[0] += "\t" + "pushi 0" + "\n"
    p[0] += "\t" + "equal" + "\n"
    p[0] += "\t" + "jz" + " " + loop_fim + "\n"
    p[0] += p[2] + "\n"
    p[0] += "\t" + "jump" + " " + loop_begin + "\n"
    p[0] += loop_fim + ":"
    ######################

    return (p)
###################
def p_Variavel (p):
    'Variavel : VARIABLE'

    if p[1] in parser.dicionario:
        parser.dicionario.remove (p[1])
    elif p[1] in parser.arrays:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Tentativa de definição de um Array como Variável!\n  {p.lineno(1)}|\t{p[1]}")
    
    p[0] = "\t" + "alloc 1" + "\n"
    p[0] += "\t" + "pop 1" + "\n"

    parser.variaveis[ p[1] ] = parser.my_heap
    parser.my_heap += 1

    return (p)
#...............
def p_Store (p):
    'Store : STORE'

    mo = re.search (r'(-?\d+)\s([a-zA-Z][a-zA-Z0-9]+)\s!', p[1])
    inteiro = mo.group (1)
    _id = mo.group (2)

    if _id not in parser.variaveis:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável {_id} não definida!\n  {p.lineno(1)}|\t{_id}")
    else:
        endereco = parser.variaveis [ _id ]
        p[0] = "\t" + "pushst" + " " + str (endereco) + "\n"
        p[0] += "\t" + "pushi" + " " + inteiro + "\n"
        p[0] += "\t" + "store 0"


    return (p)
#...............
def p_Fetch (p):
    'Fetch : FETCH'

    if p[1] not in parser.variaveis:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável {p[1]} não definida!\n  {p.lineno(1)}|\t{p[1]}")
    else:
        endereco = parser.variaveis [ p[1] ]
        p[0] = "\t" + "pushst" + " " + str (endereco) + "\n"
        p[0] += "\t" + "load 0" + "\n"

        ## Stack ####
        calcula_saldo ('INT')
        #############

    return (p)
#..............
def p_Show (p):
    'Show : SHOW'

    if p[1] not in parser.variaveis:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável {p[1]} não definida!\n  {p.lineno(1)}|\t{p[1]}")
    else:
        endereco = parser.variaveis [ p[1] ]
        p[0] = "\t" + "pushst" + " " + str (endereco) + "\n"
        p[0] += "\t" + "load 0" + "\n"
        p[0] += "\t" + "writei" + "\n"
        p[0] += "\t" + "pushi 32" + "\n"
        p[0] += "\t" + "writechr"

    return (p)
#.............
def p_Inc (p):
    'Inc : INC'

    if p[1] not in parser.variaveis:
        parser.exito = False
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Variável {p[1]} não definida!\n  {p.lineno(1)}|\t{p[1]}")
    else:
        endereco = parser.variaveis [ p[1] ]
        p[0] = "\t" + "pushst" + " " + str (endereco) + "\n"
        p[0] = "\t" + "pushst" + " " + str (endereco) + "\n"
        p[0] += "\t" + "load 0" + "\n"
        p[0] += "\t" + "pushi 1" + "\n"
        p[0] += "\t" + "add" + "\n"
        p[0] += "\t" + "store 0"


    return (p)
################
def p_Array (p):
    'Array : ARRAY'

    p[0] = ""

    if p[1][0] in parser.dicionario:
        parser.dicionario.remove (p[1][0])
    elif p[1][0] in parser.variaveis:
        parser.variaveis.remove (p[1][0])
    
    p[0] = "\t" + "alloc" + " " + str (p[1][1]) + "\n"
    p[0] += "\t" + "pop 1" + "\n"

    parser.arrays[ p[1][0] ] = (parser.my_heap, p[1][1])
    parser.my_heap += 1

    return (p)
################
def p_ArrayStore (p):
    'ArrayStore : ARRAYSTORE'

    _id = p[1][0]
    offset = p[1][1]

    p[0] = ""

    if _id not in parser.arrays:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Array {p[1]} não definido!\n  {p.lineno(1)}|\t{p[1]}")
        parser.erro = True
    elif _id in parser.arrays:
        
        limite = parser.arrays[ p[1][0] ][1]
        
        if int (offset) >= int (limite):
            parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Limite {p[1]} ultrapassado!\n  {p.lineno(1)}|\t{p[1]}")
            parser.erro = True
        else:
            bloco = parser.arrays[ p[1][0] ][0]
        
            p[0] = "\t" + "pushst" + " " + str (bloco) + "\n"
            p[0] += "\n"
            p[0] += "\t" + "pushsp" + "\n"
            p[0] += "\t" + "load -1" + "\n"
            p[0] += "\n"
            p[0] += "\t" + "store" + " " + offset + "\n"
            p[0] += "\n"
            p[0] += "\t" + "pop 1"

    return (p)
#####################
def p_ArrayFetch (p):
    'ArrayFetch : ARRAYFETCH'

    _id = p[1][0]
    offset = p[1][1]

    p[0] = ""

    if _id not in parser.arrays:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Array {p[1]} não definido!\n  {p.lineno(1)}|\t{p[1]}")
        parser.erro = True
    elif _id in parser.arrays:
        
        limite = parser.arrays[ p[1][0] ][1]
        
        if int (offset) >= int (limite):
            parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Limite {p[1]} ultrapassado!\n  {p.lineno(1)}|\t{p[1]}")
            parser.erro = True
        else:
            bloco = parser.arrays[ p[1][0] ][0]
        
            p[0] = "\t" + "pushst" + " " + str (bloco) + "\n"
            p[0] += "\t" + "load" + " " + offset + "\n"

            ## Stack ####
            calcula_saldo ('INT')
            #############

    return (p)
#####################
def p_ArrayShow (p):
    'ArrayShow : ARRAYSHOW'

    _id = p[1][0]
    offset = p[1][1]

    p[0] = ""
    if _id not in parser.arrays:
        parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Array {p[1]} não definido!\n  {p.lineno(1)}|\t{p[1]}")
        parser.erro = True
    elif _id in parser.arrays:
        
        limite = parser.arrays[ p[1][0] ][1]
        
        if int (offset) >= int (limite):
            parser.erros.append (f"Erro:{p.lineno(1)}:{p.lexpos(1) - lex.LEXCOLUNA}: Limite {p[1]} ultrapassado!\n  {p.lineno(1)}|\t{p[1]}")
            parser.erro = True
        else:
            bloco = parser.arrays[ p[1][0] ][0]
        
            p[0] = "\t" + "pushst" + " " + str (bloco) + "\n"
            p[0] += "\t" + "load" + " " + offset + "\n"
            p[0] += "\t" + "writei" + "\n"
            p[0] += "\t" + "pushi 32" + "\n"
            p[0] += "\t" + "writechr"

    return (p)
##################
def p_Comment (p):
    'Comment : COMMENT'
    p[0] = ""
    return (p)
################
def p_error (p):
    parser.erros.append (f"Erro:{p.lineno}:{p.lexpos - lex.LEXCOLUNA}: Palavra \" {p.value} \" não reconhecida no contexto!")
    parser.exito = False

    ## THEN? ############
    if (p.value == 'THEN') and len (parser.stack_construtor) > 0:
        parser.erros.append (f"  {p.lineno}|\t{p.lineno}:{p.lexpos - lex.LEXCOLUNA} Provavelmente à espera de instruções...")
    ## ELSE? ##############
    elif (p.value == 'ELSE') and len (parser.stack_construtor) > 0:
        parser.erros.append (f"  {p.lineno}|\t{p.lineno}:{p.lexpos - lex.LEXCOLUNA} Provavelmente à espera de instruções...")
        #raise Exception("STOP: Parsing abortado!!!")
    #######################

    ## DO?   ####################
    if (p.value == "DO") and len (parser.stack_construtor) > 0:
        parser.erros.append (f"  {p.lineno}|\t{p.lineno}:{p.lexpos - lex.LEXCOLUNA} Provavelmente à espera de instruções...")
    #############################

    ## LOOP? ####################
    if (p.type == "INT_MAIS_LOOP") and len (parser.stack_construtor )> 0:
        parser.erros.append (f"  {p.lineno}|\t{p.lineno}:{p.lexpos - lex.LEXCOLUNA} Provavelmente à espera de instruções...")
    #############################
    
    pass
########

#+---   I Am The Context   -----------------------------+

########################################################
def calcula_saldo (token, linha=0, coluna=0, valor=""):
    
    #. . Where Am I? . . . . . . . . . . . 
    if parser.exito == False:
        return ()

    # - Interpretador -- -- -- -- -- -- --
    if len (parser.stack_construtor) == 0:

        ## ambush ####################
        if token not in parser.custos:
            parser.erros.append (f"Erro:{linha}:{coluna - lex.LEXCOLUNA}: A função {token} não está definida!\n  {linha}|\t{token}")
            parser.critical = False
        #<><><><><><><><><><><><><><><
        else:
            ## In debt? ###########
            while ( parser.banco - parser.custos[ token ][0] ) < 0:
                parser.divida += 1
                parser.banco  += 1
            #######################

            ### Pay   #############
            parser.banco -= parser.custos[ token ][0] 
            #######################
            
            # Recieve #############
            parser.banco += parser.custos[ token ][1] 
            #######################

            ### Stack #############
            verifica_stack ()
            if parser.erro == True:
                erro_operandos (linha, coluna, valor)
            #######################

        ##############################
    
    # - Construtor -- -- -- -- -- -- -- --
    else:

        ## ambush ###################################################################
        if (token not in parser.custos) and (token != parser.stack_construtor[0][0]):
            parser.erros.append (f"Erro:{linha}:{coluna - lex.LEXCOLUNA}: A função {token} não está definida!\n  {linha}|\t{token}")
            parser.critical = True
        #><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
        else:
            ## In debt? ###########
            while ( parser.banco_construtor - parser.custos[ token ][0] ) < 0:
                parser.divida_construtor += 1
                parser.banco_construtor  += 1
            #######################

            ### Pay   #############
            parser.banco_construtor -= parser.custos[ token ][0] 
            #######################
            
            # Recieve #############
            parser.banco_construtor += parser.custos[ token ][1] 
            #######################
        #############################################################################
    #. . . . . . . . . . . . . . . . . . .
    
    return ()
######################
def verifica_stack ():

    ### ambush ########################### 
    if len (parser.stack_construtor) == 0:
        if parser.divida > 0:
            parser.erro = True
    ##########################
    
    return ()
#################################################
def erro_operandos (linha=0, coluna=0, valor=""):
    
    ### ambush ###########################
    if len (parser.stack_construtor) == 0:
        if parser.erro == True:
            parser.erros.append (f"Erro: {linha}:{coluna - lex.LEXCOLUNA}: Falta(m) {parser.divida} operando(s)!\n  {linha}|\t{valor}")
    ##################################

    return ()
############################
def assemble_func (keyword):
    assembly = ""

    if keyword in parser.dicionario:
        assembly = parser.dicionario [ keyword ]

        if parser.custos[ keyword ][2] > 0:
            assembly = re.sub (r'<0xf([\+\-]\d+)>', calcula_endereco, assembly)
            parser.my_heap += parser.custos[ keyword ][2]

    return assembly
####################################
def calcula_endereco (match_object):

    endereco = parser.my_heap + int ( match_object.group (1) )
    
    return ( str (endereco) )
#+----------------------------------------------------------------------------------+

  #-#####-#
 # MAIN  ##
#_#####_#_#

parser = yacc.yacc()

####################
parser.exito = True
parser.erro = False
parser.stack_construtor = []
parser.stack_else_labels = []
parser.stack_then_labels = []
parser.stack_loop_labels = []
parser.erros = []
parser.banco = 0
parser.divida = 0
parser.banco_construtor = 0
parser.divida_construtor = 0
parser.label_else_n = 1
parser.label_then_n = 1
parser.label_loop_n = 1
parser.heap_alloc = 0
parser.my_heap = 0
parser.if_flag = False
parser.do_flag = False
parser.mais_loop_op = 0
parser.custos = {
    #token      : ( #consome, #produz)
    'INT'       :   (   0   ,   1   ),
    'I'         :   (   0   ,   1   ),
    'J'         :   (   0   ,   1   ),
    
    'ADD'       :   (   2   ,   1   ),
    'SUB'       :   (   2   ,   1   ),
    'MUL'       :   (   2   ,   1   ),
    'DIV'       :   (   2   ,   1   ),
    'MOD'       :   (   2   ,   1   ),

    'IGUAL'     :   (   2   ,   1   ),
    'DIFERENTE' :   (   2   ,   1   ),
    'MENOR'     :   (   2   ,   1   ),
    'SUPERIOR'  :   (   2   ,   1   ),

    'ZERO_IGUAL':   (   1   ,   1   ),
    'NEGATIVO'  :   (   1   ,   1   ),
    'POSITIVO'  :   (   1   ,   1   ),

    'PONTO'     :   (   1   ,   0   ),
    'EMIT'      :   (   1   ,   0   ),
    'DUP'       :   (   1   ,   2   ),
    'DROP'      :   (   1   ,   0   ),
    'IF'        :   (   1   ,   0   ),
    'DO'        :   (   2   ,   0   ),
    '+LOOP'     :   (   1   ,   0   ),
    'BEGIN'     :   (   1   ,   0   ),
    'INC'       :   (   1   ,   0   ),
}
parser.untreaceble_keywords = []
parser.dicionario = {}
parser.variaveis = {}
parser.arrays = {}
parser.compilacao = ""
####################