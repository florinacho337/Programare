%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>
    #include <stdbool.h>

    #define MAX 1000

    void yyerror(const char *s);
    extern int yylineno;
    extern FILE *yyin; 
    int yylex();
    char declarations[MAX][MAX], sourceCode[MAX][MAX], imports[MAX][MAX];
    int lenDeclarations = 0, lenSourceCode = 0, lenImports = 0;
    char expressions[MAX][MAX];
    int lenExpressions = 0;
    bool found(char col[][MAX], int n, char* s);
    void parseExpression(char* s);
    void printDeclarationSegment();
    void printCodeSegment();
    void printImports();
    FILE *outputFile;
%}

%token INT_CONST ID
%token INT_KEYWORD CIN_KEYWORD COUT_KEYWORD INCLUDE NAMESPACE
%token '+' '-' '*' '='
%token SHIFT_LEFT SHIFT_RIGHT

%union {
    char *value;
}

%%
program:
    | INCLUDE NAMESPACE INT_KEYWORD ID '(' ')' '{' instructiuni '}'
    ;

instructiuni:
    instructiune
    | instructiune instructiuni
    ;

instructiune:
    instr_declarare
    | atribuire
    | citire
    | afisare
    ;

instr_declarare:
    INT_KEYWORD declarare

declarare:
    ID ';' {
        char tmp[100];
        strcpy(tmp, " ");
        strcat(tmp, $<value>1);
        if (!found(declarations, lenDeclarations, tmp)) {
			strcpy(declarations[lenDeclarations], strcat(tmp, " times 4 db 0"));
			lenDeclarations++;
		}
    }
    ;

atribuire:
    ID '=' expresie ';' {
        char tmp[MAX];
        strcpy(tmp, $<value>3);
        char* token = strtok(tmp, " ");
        while (token != NULL) {
            strcpy(expressions[lenExpressions++], token);
            token = strtok(NULL, " ");
        }
        parseExpression($<value>1);
    }
    ;

citire:
    CIN_KEYWORD SHIFT_RIGHT ID ';' {
        if (!found(imports, lenImports, "scanf")) {
            strcpy(imports[lenImports], "scanf");
            lenImports++;
        }
        if (!found(declarations, lenDeclarations, "format")) {
            strcpy(declarations[lenDeclarations], " format db \"%d\", 0");
        }

        strcpy(sourceCode[lenSourceCode], "push ");
        strcat(sourceCode[lenSourceCode++], $<value>3);
        strcpy(sourceCode[lenSourceCode++], "push format");
        strcpy(sourceCode[lenSourceCode++], "call scanf");
        strcpy(sourceCode[lenSourceCode++], "add ESP, 4 * 2\n");
    }
    ;

afisare:
    COUT_KEYWORD SHIFT_LEFT ID ';' {
        if (!found(imports, lenImports, "printf")) {
            strcpy(imports[lenImports], "printf");
            lenImports++;
        }
        if (!found(declarations, lenDeclarations, "format")) {
            strcpy(declarations[lenDeclarations], " format db \"%d\", 0");
            lenDeclarations++;
        }
        strcpy(sourceCode[lenSourceCode], "push dword [");
        strcat(sourceCode[lenSourceCode], $<value>3);
        strcat(sourceCode[lenSourceCode++], "]");
        strcpy(sourceCode[lenSourceCode++], "push format");
        strcpy(sourceCode[lenSourceCode++], "call printf");
        strcpy(sourceCode[lenSourceCode++], "add ESP, 4 * 2\n");
    }
    ;

expresie:
    any
    | any op_aritmetic expresie {
        char tmp[MAX];
        strcpy(tmp, $<value>1);
        strcat(tmp, " ");
        strcat(tmp, $<value>2);
        strcat(tmp, " ");
        strcat(tmp, $<value>3);
        $<value>$ = strdup(tmp);
    }
    ;

op_aritmetic:
    '+'
    | '-'
    | '*'
    ;

any:
    ID
    | INT_CONST
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Eroare sintactică la linia %d: %s\n", yylineno, s);
    exit(0);
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Utilizare: %s <nume_fisier> <nume_fisier_asm>\n", argv[0]);
        return 1;
    }

    FILE *fisier = fopen(argv[1], "r");
    if (!fisier) {
        perror("Eroare la deschiderea fișierului");
        return 1;
    }

    yyin = fisier;
    yyparse();
    fclose(fisier);

    strcpy(imports[lenImports++], "exit");

    outputFile = fopen(argv[2], "w+");
    
    fprintf(outputFile, "bits 32\nglobal main\n\n");
    printImports();
    fprintf(outputFile, "section .data\n");
    printDeclarationSegment();

    fprintf(outputFile, "\nsection .text\n\tmain:\n");
    strcpy(sourceCode[lenSourceCode++], "push 0");
    strcpy(sourceCode[lenSourceCode++], "call exit");
    printCodeSegment();

    printf("Fișier ASM generat cu succes!\n");

    fclose(outputFile);
    return 0;
}

void parseExpression(char*  element) {
    if (isdigit(expressions[0][0])) {
        strcpy(sourceCode[lenSourceCode], "mov BL, ");
        strcat(sourceCode[lenSourceCode++], expressions[0]);
    } else {
        strcpy(sourceCode[lenSourceCode], "mov BL, [");
        strcat(sourceCode[lenSourceCode], expressions[0]);
        strcat(sourceCode[lenSourceCode++], "]");
    }
    int i = 1;
	while (i < lenExpressions - 1) {
		switch(expressions[i][0]) {
            case '*':
                strcpy(sourceCode[lenSourceCode++], "mov AL, BL");
                while (i < lenExpressions - 1 && expressions[i][0] == '*') {
                    if (isdigit(expressions[i + 1][0])) {
                        strcpy(sourceCode[lenSourceCode], "mov DL, ");
                        strcat(sourceCode[lenSourceCode++], expressions[i + 1]);
                        strcpy(sourceCode[lenSourceCode++], "mul DL");
                    } else {
                        strcpy(sourceCode[lenSourceCode], "mul byte [");
                        strcat(sourceCode[lenSourceCode], expressions[i + 1]);
                        strcat(sourceCode[lenSourceCode++], "]");
                    }
                    i += 2;
                }
                strcpy(sourceCode[lenSourceCode++], "mov BL, AL");
                break;
            case '+':
                int j = i + 2;
                if (isdigit(expressions[i + 1][0])) {
                    strcpy(sourceCode[lenSourceCode], "mov AL, ");
                    strcat(sourceCode[lenSourceCode++], expressions[i + 1]);
                } else {
                    strcpy(sourceCode[lenSourceCode], "mov AL, byte [");
                    strcat(sourceCode[lenSourceCode], expressions[i + 1]);
                    strcat(sourceCode[lenSourceCode++], "]");
                }
                while (j < lenExpressions - 1 && expressions[j][0] == '*') {
                    if (isdigit(expressions[j + 1][0])) {
                        strcpy(sourceCode[lenSourceCode], "mov DL, ");
                        strcat(sourceCode[lenSourceCode++], expressions[j + 1]);
                        strcpy(sourceCode[lenSourceCode++], "mul DL");
                    } else {
                        strcpy(sourceCode[lenSourceCode], "mul byte [");
                        strcat(sourceCode[lenSourceCode], expressions[j + 1]);
                        strcat(sourceCode[lenSourceCode++], "]");
                    }
                    j += 2;
                }
                strcpy(sourceCode[lenSourceCode++], "add BL, AL");
                i = j;
                break;
            case '-':
                j = i + 2;
                if (isdigit(expressions[i + 1][0])) {
                    strcpy(sourceCode[lenSourceCode], "mov AL, ");
                    strcat(sourceCode[lenSourceCode++], expressions[i + 1]);
                } else {
                    strcpy(sourceCode[lenSourceCode], "mov AL, byte [");
                    strcat(sourceCode[lenSourceCode], expressions[i + 1]);
                    strcat(sourceCode[lenSourceCode++], "]");
                }
                while (j < lenExpressions - 1 && expressions[j][0] == '*') {
                    if (isdigit(expressions[j + 1][0])) {
                        strcpy(sourceCode[lenSourceCode], "mov DL, ");
                        strcat(sourceCode[lenSourceCode++], expressions[j + 1]);
                        strcpy(sourceCode[lenSourceCode++], "mul DL");
                    } else {
                        strcpy(sourceCode[lenSourceCode], "mul byte [");
                        strcat(sourceCode[lenSourceCode], expressions[j + 1]);
                        strcat(sourceCode[lenSourceCode++], "]");
                    }
                    j += 2;
                }
                strcpy(sourceCode[lenSourceCode++], "sub BL, AL");
                i = j;
        }
 	}

	strcpy(sourceCode[lenSourceCode], "mov [");
	strcat(sourceCode[lenSourceCode], element);
	strcat(sourceCode[lenSourceCode++], "], BL\n");
	lenExpressions = 0;
}

bool found(char col[][MAX], int n, char* var) {
	char tmp[MAX];
	strcpy(tmp, var);
	strcat(tmp, " ");
	for (int i = 0; i < n; i++) {
		if (strstr(col[i], tmp) != NULL) {
			return true;
		}
	}
	return false;
}

void printImports() {
	for (int i = 0; i < lenImports; i++) {
		fprintf(outputFile, "extern %s\n\n", imports[i]);
	}
}

void printDeclarationSegment() {
	for (int i = 0; i < lenDeclarations; i++) {
		fprintf(outputFile, "\t%s\n", declarations[i] + 1);
	}
}

void printCodeSegment() {
	for (int i = 0; i < lenSourceCode; i++) {
		fprintf(outputFile, "\t\t%s\n", sourceCode[i]);
	}
}