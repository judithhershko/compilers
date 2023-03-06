grammar Expression;

start_rule: (dec)*(expr)*;

dec : ID EQ expr
    ;
binop:
     MULT
     | DIV
     | MIN
     | PLUS
     | GT
     | LT
     | AND
     | OR
     | ISEQ
     | GOE
     | LOE
     ;

expr:
     LBRAK expr RBRAK
    | expr binop expr
    | NOT  expr
    | expr MIN  MIN NLINE
    | PLUS PLUS expr NLINE
    | MIN MIN expr NLINE
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
ISEQ : '==';
AND  : '&&';
OR   : '||';
NOT  :  '!';
GOE  :  '>=';
LOE  :  '<=';
MOD  :  '%' ;
NLINE:';' .*? '\n' -> skip;



