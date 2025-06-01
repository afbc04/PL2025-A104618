from lexical.lex import lexer
import syntax.syn as syn
import semantic.semantic as sem
import machine_code_generator.code_generator as mcg
import errors.error_handler as eh
import sys
import time
import argparse


def main():

    args_parser = argparse.ArgumentParser(add_help=False,prog="main.py",description="Pascal Compiler - Processamento de Linguagens 2025",formatter_class=lambda prog: argparse.HelpFormatter(prog, width=200))
    
    try:
        args_parser.add_argument("input_file", type=str,help="File path of Pascal file to be compiled")
        args_parser.add_argument("--name",help="Define a custom name to output file", type=str, default="output_code.vmcode")
        args_parser.add_argument("--no-opt", action="store_true", help="Disable optimizations in VM Code")
        args_parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

        args = args_parser.parse_args()

    except SystemExit:
        sys.exit(1)
    
    filepath = args.input_file
    output_name = args.name
    do_optimizations = not args.no_opt
    
    start_time = time.perf_counter()
    compiling_time = None
    lex_time = None
    syntax_time = None
    semantic_time = None
    
    pascalCode = "" 
        
    try:
        file = open(filepath,"r")

        for line in file:
            pascalCode += line

        lexer.input(pascalCode)
        lex_time = time.perf_counter()
        
        #Forcing the lexical analysis
        while lexer.token():
            pass 

        if eh.how_many_lexical_errors() == 0:
                        
            ast = syn.SyntaxParser(pascalCode,lexer)
            syntax_time = time.perf_counter()
                        
            if eh.how_many_syntax_errors() == 0 and eh.how_many_lexical_errors() == 0:
                        
                is_semantically_valid,semantic_ast,semantic_table = sem.run_semantic_analysis(ast,do_optimizations)
                semantic_time = time.perf_counter()
                
                if is_semantically_valid is True:
                    
                    mcg.generate_code(output_name,semantic_ast,semantic_table)
                    compiling_time = time.perf_counter()
                
        eh.print_compilation_summary(output_name,pascalCode,start_time,compiling_time,lex_time,syntax_time,semantic_time)

    except FileNotFoundError:
        print(f"Error: Pascal File {filepath} not found.")
        
    except PermissionError:
        print(f"Error: No permission to read {filepath} file.")
        
    except Exception as e:
        print(f"Error: {e}")
        
        
        
main()
