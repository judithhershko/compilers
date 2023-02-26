grammar Expression;

start_rule: (dec)*(expr)*;

dec : ID EQ NUM;

expr: expr PLUS expr
    | expr MIN expr
    | expr MULT expr
    | LBRAK expr RBRAK
    | expr DIV expr
    | expr GT expr
    | expr LT expr
    | ID
    | NUM
    ;

ID   : [a-zA-Z_][a-zA-Z_0-9]*;
NUM  : [0-9]+ ;
WS   : [ \t\n\r\f]+ -> skip ;
GT   : '>' ;
LT   : '<' ;
DIV  : '/' ;
MULT : '*' ;
MIN  : '-' ;
PLUS : '+' ;
EQ   : '=' ;
LBRAK: '(' ;
RBRAK: ')' ;
NLINE:';' .*? '\n' -> skip;

