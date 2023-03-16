grammar Expression;

start_rule: (print|expr|dec|comments)*;

print   : PRINT LBRAK (char_pri | pri) RBRAK ;
comments: ML_COMMENT | SL_COMMENT;
typed_var: INT| DOUBLE | FLOAT |CHAR;

const : CONST;
pointer_variable: (pointer)* var=ID;
pointer:MULT;

to_pointer: (pointer)* pri ;
to_reference: REF pri ;

dec:(const)? typed_var (pointer)* ID EQ (char_expr|expr) |(pointer)* ID EQ (char_expr|expr);
variable_dec:typed_var ID;

binop:MIN | PLUS ;
binop_md: MULT| DIV | MOD;
equality: ISEQ | NEQ;
comparator: LOE | GOE | LT | GT;
or_and: OR | AND ;

expr: expr or_and term_1 | term_1;
term_1: term_1 equality term_2 | term_2;
term_2: term_2 comparator term_3 | term_3;
term_3: term_3 binop term_4 | term_4 ;
term_4: term_4 binop_md fac | term_5;
term_5: NOT term_5 | term_6;
term_6: PP term_6 | MM term_6 | term_7;
term_7: term_7 PP | term_7 MM | fac;
fac:LBRAK expr RBRAK|pri;
pri:  ID | num+ '.' num* | '.' num+ | num;
fnum: num | num+ '.' num* | '.' num+ ;
num: NUM;

//term: fac |term binop_md fac;

char_op: PLUS | MIN;
char_expr: char_pri| char_expr char_op char_expr;
//char_pri:CHAR_ID SEARCH_TYPE CHAR_ID ;
char_pri:CHAR_ID (ID | NUM)* CHAR_ID ;

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;
CONST   : 'const'   ;
REF     : '&'       ;
PRINT   : 'printf'  ;

//SEARCH_TYPE: '"' ~'"'* '"';
PT   : '.' ;
MULT : '*' ;
NUM  : [0-9]+ ;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;
WS   : [ \t\n\r\f]+ -> skip ;
NEQ  : '!=';
PP   : '++';
MM   : '--';
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
ML_COMMENT:  '/*' .* '*/';
SL_COMMENT:  '//' ~('\r' | '\n')*;


EOL: ';' -> skip;
NLINE:';' .*? '\n' -> skip;




