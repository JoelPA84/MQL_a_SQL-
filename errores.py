import re
import tkinter as tk
from tkinter import ttk
import ply.lex as lex
import ply.yacc as yacc

# Tokens
tokens = (
    'SELECT', 'FROM', 'WHERE', 'AND', 'INSERT', 'INTO', 'VALUES',
    'UPDATE', 'SET', 'DELETE', 'IDENTIFIER', 'STRING'
)

t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_AND = r'AND'
t_INSERT = r'INSERT'
t_INTO = r'INTO'
t_VALUES = r'VALUES'
t_UPDATE = r'UPDATE'
t_SET = r'SET'
t_DELETE = r'DELETE'
t_IDENTIFIER = r'\w+'
t_STRING = r'\'[^\']*\'|\"[^\"]*\"'

t_ignore = ' \t\n'

def t_error(t):
    print("Error léxico: Carácter inesperado '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Grammar rules
def p_query(p):
    '''query : select_query
             | insert_query
             | update_query
             | delete_query'''
    p[0] = p[1]

def p_select_query(p):
    '''select_query : SELECT '*' FROM IDENTIFIER WHERE conditions'''
    p[0] = f"SELECT * FROM {p[4]} WHERE {p[6]}"

def p_conditions(p):
    '''conditions : condition
                  | condition AND conditions'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]} AND {p[3]}"

def p_condition(p):
    '''condition : IDENTIFIER '=' STRING'''
    p[0] = f"{p[1]} = {p[3]}"

def p_insert_query(p):
    '''insert_query : INSERT INTO IDENTIFIER '(' IDENTIFIER ')' VALUES '(' values ')' '''
    p[0] = f"INSERT INTO {p[3]} ({p[5]}) VALUES ({p[8]})"

def p_values(p):
    '''values : STRING
              | STRING ',' values'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"

def p_update_query(p):
    '''update_query : UPDATE IDENTIFIER SET set_values WHERE conditions'''
    p[0] = f"UPDATE {p[2]} SET {p[4]} WHERE {p[6]}"

def p_set_values(p):
    '''set_values : IDENTIFIER '=' STRING
                  | IDENTIFIER '=' STRING ',' set_values'''
    if len(p) == 4:
        p[0] = f"{p[1]} = {p[3]}"
    else:
        p[0] = f"{p[1]} = {p[3]}, {p[5]}"

def p_delete_query(p):
    '''delete_query : DELETE FROM IDENTIFIER WHERE conditions'''
    p[0] = f"DELETE FROM {p[3]} WHERE {p[5]}"

def p_error(p):
    print("Error sintáctico en la entrada")

parser = yacc.yacc()

def on_convert_button_click():
    mql_query = mql_query.get()
    try:
        sql_query = parser.parse(mql_query, lexer=lexer)
        sql_query.config(text="SQL Query: " + sql_query)
    except:
        pass

root = tk.Tk()
root.title("Transpilador MQL a SQL")

# Resto del código para la interfaz gráfica...
