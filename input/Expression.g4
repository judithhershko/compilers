grammar Expression;

start_rule : (includes (';')* )? s_rule ;
s_rule: (print ';'|scan ';'|expr ';'|dec ';'|comments|line|loop|scope (';')?| function_definition | function_dec| includes)*;

includes: INCLUDE|INCLUDEH (';')?;
line:NLINE;

print : PRINT '(' format_string (',' ('*')* expr)* ')';
scan  : SCAN '(' format_string (',' pri)* ')';
format_string: STRING_LITERAL (',' STRING_LITERAL)*;

comments: ML_COMMENT | SL_COMMENT;
typed_var: INT| DOUBLE | FLOAT |CHAR | BOOL;

scope : '{' rule (return)? rule'}' (';')?;
rule  : (print ';'|scan ';' |expr ';'|dec ';'|comments|line|loop|scope | function_dec)*;
lrules: (print ';' |scan ';' |expr ';' |dec ';' |comments |line |loop (';')? |break |continue | lscope | function_dec )*;
lscope: '{' lrules '}' ;
loop  : while | for | if;
while : WHILE '(' expr ')' lscope;
for   : FOR LBRAK dec ';' expr ';' (expr|dec) RBRAK lscope ;
if    : IF LBRAK expr RBRAK lscope |  ELSE  lscope | ELSE IF  LBRAK expr RBRAK lscope;
break : BREAK ';';
continue: CONTINUE ';';

function_dec: function_name '(' (f_variables)?  (',' f_variables )* ')';
return_type: (CONST)? (INT| DOUBLE | FLOAT |CHAR | BOOL | VOID);
parameters: (const)? typed_var (pointer)* (ref)? ID ;
f_variables: pri;
ref: REF;
function_definition: return_type function_name LBRAK (parameters)? (',' parameters )* RBRAK scope ;
function_name: ID;
return: RETURN (expr | char_expr)? ';' ;

const : CONST;
pointer:MULT;
ref_ref: (REF)? ID;
pointers: (pointer)+ ID (EQ ref_ref)? |  REF (EQ ref_ref)?;
suf_dec: pointers | ID EQ (char_expr|expr);
pointer_val: (pointer)+ ID;

array : ID '[' num ']' ;
array_content : '{' array_ci (',' array_ci)* '}';
array_ci      : pri | (pointer)* (ID|array) ;
dec:(const)? typed_var (pointer)* (ID|array) EQ (function_dec|pointer_val|ref_ref|char_expr|expr|array_content|array) |(pointer)* (ID|array) EQ (function_dec|pointer_val|ref_ref|char_expr|expr|array)
| (const)? typed_var (pointer)* (ID|array);

binop:MIN | PLUS ;
binop_md: MULT| DIV | MOD;
equality: ISEQ | NEQ;
comparator: LOE | GOE | LT | GT;
or_and: OR | AND ;
prefix_op: NOT | PP | MM ;
suffix_op: PP | MM ;

expr: expr suffix_op | prefix_op expr | expr binop_md expr | expr binop expr | expr comparator expr |  expr equality expr | expr or_and expr  | fac;
fac : brackets|pri ;
brackets: LBRAK expr RBRAK;
pri: function_dec | array | ID | ('-' | '+') ? num+ '.' num* |('-' | '+') ? '.' num+ | ('-' | '+') ? num;

fnum: num | num+ '.' num* | '.' num+ ;
num: NUM;

char_op: PLUS | MIN;
char_expr: char_pri| char_expr char_op char_expr;

char_pri: CHAR_ID ( . )? CHAR_ID ;
//'\\' 'n' | '\\' 'r' | '\\' 't' | '\\' '0'

INT     : 'int'     ;
DOUBLE  : 'double'  ;
FLOAT   : 'float'   ;
CHAR    : 'char'    ;
BOOL    : 'bool'    ;
CONST   : 'const'   ;
REF     : '&'       ;
PRINT   : 'printf'  ;
SCAN    : 'scanf'   ;
VOID    : 'void'    ;
RETURN  : 'return'  ;
INCLUDE : '#include <stdio.h>' ;
INCLUDEH: '#include "stdio.h"' ;

PT   : '.' ;
WHILE:'while';
FOR  :'for' ;
IF   : 'if' ;
ELSE : 'else';
BREAK: 'break';
CONTINUE: 'continue';
MULT : '*' ;
NUM  : [0-9]+ ;
ID   : [a-zA-Z_][a-zA-Z_0-9]*;
ALPHANUM : [A-Za-z0-9] ;
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
ONE_LINE_COMMENT:'//';
STRT_COMMENT:'/**';
END_COMMENT:'**/' ;
ML_COMMENT:  '/*' .* '*/';
SL_COMMENT:  '//' ~('\r' | '\n')*;

STRING_LITERAL: '"' (ESC_SEQ |~('%'|'"'|'\n'|'\r'))* '"';
fragment ESC_SEQ: '%' ('d'|'i'|'s'|'c');
NLINE: '\n';
