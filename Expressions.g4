
grammar Expressions;


program
    : stat EOF
    | def EOF
    ;

stat: ID '=' expr ';'
    | expr ';'
    ;

def : ID '(' ID (',' ID)* ')' '{' stat* '}' ;

expr: ID
    | INT
    | func
    | expr PLUS expr
    | expr MINUS expr
    | expr MULT expr
    | expr DEV expr
    ;

func : ID '(' expr (',' expr)* ')' ;

// DELETE THIS CONTENT IF YOU PUT COMBINED GRAMMAR IN Parser TAB


PLUS : '+' ;
MINUS : '-' ;
EQ : '=' ;
MULT : '*' ;
DEV : '/' ;
LPAREN : '(' ;
RPAREN : ')' ;

INT : [0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;

