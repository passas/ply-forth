import re
import sys 

from yac import parser

if __name__ == "__main__":


    ## Bad Usage ########
    if len(sys.argv) < 2:
        print ("bad usage: try: pyhton3 main.py --h")
       
    ## Help ####################################################
    elif len(sys.argv) == 2 and re.search (r'--h', sys.argv[1]):
        print ("python3 main.py <input file> [-o <output name>]")  
       
    ## Compile #
    else:  
        ## Concatenação ####################
        argumentos = ' '.join (sys.argv[1:])
        ####################################
        
        ## Named Output ###################################
        output_name = re.search ( r'-o (\w+)', argumentos )
        if output_name:
            output_name = output.group(1) + ".vm"
        ############################################
        
        ## Default Output #########
        else:
            output_name = "a.vm"
        ###########################
        
        ## Ficheiro Forth ################################
        input_file = re.sub ( r'(-o \w+)', "", argumentos)
        ##################################################
        
        ## Forth Code ###########
        f = open(input_file, "r")
        #########################
        
        ## Parse Forth #######################
        parser.parse (f.read(), tracking=True)
        ######################################

        ## Close Forth #
        f.close()
        ################
        
        ## Sucesso ######################################
        if parser.exito == True and parser.erro == False:
           
            ## Warnings ######################
            if parser.banco > 0 :   print ( '\n'.join (parser.erros) )
            ##################################
        
            ## VM Assembly ###########
            f = open(output_name, "w")
            f.write(parser.compilacao)
            f.close()
            ##########################

        ## Insucesso #################################
        else:
            print ( '\n'.join (parser.erros) )
            print (f"\nSTOP: Ficheiro não compilado!  ")