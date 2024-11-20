%{
typedef struct Node {
    char *value;
    int index;
    struct Node *prev_node;
    struct Node *next;
} Node;

typedef struct SymbolTable {
    Node *head;
    Node *tail;
    int size;
} SymbolTable;

typedef struct TokenCode {
    char token[32];
    int code;
} TokenCode;

TokenCode *token_codes = NULL;
int token_count = 0;

SymbolTable identifiers_table = {NULL, NULL, 0};
SymbolTable constants_table = {NULL, NULL, 0};

int line_number = 1;

typedef struct FIPEntry {
    int code;
    int index;  // -1 dacă nu are index
} FIPEntry;

FIPEntry *fip = NULL;
int fip_size = 0;

void load_token_codes(const char *filename);
int insert_into_table(SymbolTable *table, const char *value);
void save_symbol_table(const char *filename, SymbolTable *table);
void add_to_fip(int code, int index);
void print_fip();
void print_error(const char *message);
%}

%option noyywrap

ID      [a-zA-Z_][a-zA-Z0-9_]{0,254}       
CONST   0|-?[1-9][0-9]*(\.[0-9]+)?                
OP_SEP  \+\+|\-\-|[+\-\*/%]=?|>>|<<|[=!<>]=|<|>|=|[;,(){}]|int|float|while|if|cin|cout   
WS      [ \t\r]+                          
NEWLINE \n                                  

%%
{CONST}     { 
                int index = insert_into_table(&constants_table, yytext);
                add_to_fip(1, index);
            }
{OP_SEP}    { 
                for (int i = 0; i < token_count; ++i) {
                    if (strcmp(token_codes[i].token, yytext) == 0) {
                        add_to_fip(token_codes[i].code, -1);
                        break;
                    }
                }
            }
{ID}        { 
                int index = insert_into_table(&identifiers_table, yytext);
                add_to_fip(0, index);
            }
{WS}        { /* Ignore */ }
{NEWLINE}   { line_number++; }
.           { 
                print_error(yytext);
                free(token_codes);
                free(fip);
                fip_size = token_count = 0;
                return 0;
            }
%%


void load_token_codes(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Eroare la deschiderea fișierului: %s\n", filename);
        exit(1);
    }

    char line[128];
    while (fgets(line, sizeof(line), file)) {
        char token[32];
        int code;
        if (sscanf(line, "%s %d", token, &code) == 2) {
            token_codes = realloc(token_codes, (token_count + 1) * sizeof(TokenCode));
            strcpy(token_codes[token_count].token, token);
            token_codes[token_count].code = code;
            token_count++;
        }
    }

    fclose(file);
}

int insert_into_table(SymbolTable *table, const char *value) {
    Node *new_node = malloc(sizeof(Node));
    new_node->value = strdup(value);
    new_node->index = table->size;
    new_node->prev_node = new_node->next = NULL;

    if (!table->head) {
        table->head = table->tail = new_node;
    } else {
        Node *current = table->head, *prev_node = NULL;
        while (current && strcmp(current->value, value) < 0) {
            prev_node = current;
            current = current->next;
        }

        if (current && strcmp(current->value, value) == 0) {
            free(new_node->value);
            free(new_node);
            return current->index;
        }

        if (!current) {
            prev_node->next = new_node;
            new_node->prev_node = prev_node;
            table->tail = new_node;
        } else if (!prev_node) {
            new_node->next = table->head;
            table->head->prev_node = new_node;
            table->head = new_node;
        } else {
            prev_node->next = new_node;
            new_node->prev_node = prev_node;
            new_node->next = current;
            current->prev_node = new_node;
        }
    }

    table->size++;
    return new_node->index;
}

void save_symbol_table(const char *filename, SymbolTable *table) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "Eroare la salvarea fișierului: %s\n", filename);
        return;
    }

    Node *current = table->head;
    while (current) {
        fprintf(file, "%d: %s, prev: %d, next: %d\n", 
                current->index, 
                current->value, 
                current->prev_node ? current->prev_node->index : -1, 
                current->next ? current->next->index : -1);
        current = current->next;
    }

    fclose(file);
}

void add_to_fip(int code, int index) {
    fip = realloc(fip, (fip_size + 1) * sizeof(FIPEntry));
    fip[fip_size].code = code;
    fip[fip_size].index = index;
    fip_size++;
}

void print_fip() {
    for (int i = 0; i < fip_size; ++i) {
        printf("%d ", fip[i].code);
        if (fip[i].index != -1) {
            printf("%d ", fip[i].index);
        }
        printf("\n");
    }
    printf("\n");
}

void print_error(const char *message) {
    fprintf(stderr, "Eroare lexicală: '%s' pe linia %d\n", message, line_number);
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        fprintf(stderr, "Utilizare: %s <fisier_coduri_tokeni> <fisier_program> <fisier_tabela_identificatori> <fisier_tabela_constante>\n", argv[0]);
        return 1;
    }

    load_token_codes(argv[1]);
    FILE *file = fopen(argv[2], "r");
    if (!file) {
        fprintf(stderr, "Eroare la deschiderea fișierului: %s\n", argv[2]);
        return 1;
    }

    yyin = file;
    yylex();
    fclose(file);

    save_symbol_table(argv[3], &identifiers_table);
    save_symbol_table(argv[4], &constants_table);
    print_fip();

    return 0;
}
