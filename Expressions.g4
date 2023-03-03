grammar Expression;

start_rule: (dec)*(expr)*;

dec : ID EQ NUM;

expr:
    term
    | expr PLUS term
    | expr MIN term
    ;
term:
    fac
    | term MULT fac
    | term DIV fac
fac:

    pri
    | LBRAK expr RBRAK
pri:
    ID
    | NUM






ID          : [a-zA-Z_][a-zA-Z_0-9]*;
INT_ID      : [0-9]+ ;
FLOAT_ID    : [0-9]+[.]?[0-9]*;
VAR_NAME    : [a-zA-Z_0-9.]+;
STRING_ID   : '"' .*? '\\00"';

INT: 'i32';
BIG_INT: 'i64';
FLOAT: 'float';
DOUBLE: 'double';
BOOL: 'i1';
CHAR: 'i8';

PTR         : '*';

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

