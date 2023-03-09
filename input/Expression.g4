grammar Expression;

start_rule: (dec)*(expr)*;

typed_var: INT| DOUBLE | FLOAT |CHAR;

const : CONST;
pointer_variable: (pointer)* var=ID;
pointer:MULT;

to_pointer: (pointer)* pri ;
to_reference: REF pri ;

//dec :variable_dec EQ expr ;
dec:(const)? typed_var (pointer)* ID EQ (char_expr|expr) |(pointer)* ID EQ (char_expr|expr);
variable_dec:typed_var ID;
//variable_dec:const typed_var pointer_variable | typed_var pointer_variable;

binop:MIN | PLUS | GT | LT | AND | OR | ISEQ | GOE | LOE ;


binop_md: MULT| DIV ;

expr: term| expr binop term ;

term: fac |term binop_md fac;

fac:LBRAK expr RBRAK|pri;

pri: NUM | ID;
char_expr: char_pri| char_expr PLUS char_expr | char_expr MIN char_expr;
char_pri:CHAR_ID ID CHAR_ID ;

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;
CONST   : 'const'   ;
REF     : '&'       ;

MULT : '*' ;
NUM  : [0-9]+ ;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;
WS   : [ \t\n\r\f]+ -> skip ;
GT   : '>' ;
LT   : '<' ;
DIV  : '/' ;
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
CHAR_ID:'\'';

EOL: ';' -> skip;
NLINE:';' .*? '\n' -> skip;





