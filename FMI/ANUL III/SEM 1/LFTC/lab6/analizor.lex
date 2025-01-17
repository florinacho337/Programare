%{
    #include "y.tab.h"
    extern int yylineno;
%}
      
CONST   0|-?[1-9][0-9]*(\.[0-9]+)?                                                                           

%%
"#include <iostream>"             { return INCLUDE; }
"using namespace std;"            { return NAMESPACE; }
"int"                             { return INT_KEYWORD; }
"cin"                             { return CIN_KEYWORD; }
"cout"                            { return COUT_KEYWORD; }
0|-?[1-9][0-9]*                   { yylval.value = strdup(yytext); return INT_CONST; }
[a-zA-Z_][a-zA-Z0-9_]{0,254}      { yylval.value = strdup(yytext); return ID; }
"<<"                              { return SHIFT_LEFT; }
">>"                              { return SHIFT_RIGHT; }
"+"                               { yylval.value = strdup(yytext); return '+'; }
"-"                               { yylval.value = strdup(yytext); return '-'; }
"*"                               { yylval.value = strdup(yytext); return '*'; }
"("                               { return '('; }
")"                               { return ')'; }
","                               { return ','; }
";"                               { return ';'; }
"{"                               { return '{'; }
"}"                               { return '}'; }
"="                               { return '='; }
[ \t\r]+                          { /* Ignore */ }
\n                                { yylineno++; }
.                                 {     
                                      fprintf(stderr, "Eroare lexicală la linia %d: caracter nevalid '%s'\n", yylineno, yytext);
                                      exit(0);
                                  }
%%