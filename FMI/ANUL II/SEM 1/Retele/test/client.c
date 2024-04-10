#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdbool.h>
#include <time.h>

bool validateIpAdress(char* adr){
        char* p;
        bool valid = true;
        p = strtok(adr, ".");
        while(p && valid){
                if(atoi(p) > 255)
                        valid = false;
                p = strtok(NULL, ".");
        }
        return valid;
}

int generatePort(){
        int num;
        num = (rand() % (65535 - 1024 + 1)) + 1024;
        return num;
}

int main(int argc, char** argv) {
    if(argc < 3){
            printf("Introduceti o adresa si un port!\n");
            return 1;
    }

    //initializare date
    int c;
    struct sockaddr_in server;
    uint16_t deimpartit, impartitor, port, p;

    //creare socket
    c = socket(AF_INET, SOCK_STREAM, 0);
    if (c < 0) {
        printf("Eroare la crearea socketului client\n");
        return 1;
    }

    //validare port si adresa
    //copy of IP Adress
    char ipAdress[17];
    strcpy(ipAdress, argv[1]);
if(!validateIpAdress(ipAdress)){
            printf("Adresa IP invalida!\n");
            return 1;
    }

    port = atoi(argv[2]);
    if(!(port > 1024 && port < 65535)){
            printf("Port invalid!\n");
            return 1;
    }

    //setare bytes to 0
    memset(&server, 0, sizeof(server));

    //initializare date server
    server.sin_port = htons(port);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(argv[1]);
    if (connect(c, (struct sockaddr*)&server, sizeof(server)) < 0) {
        printf("Eroare la conectarea la server\n");
        return 1;
    }

    //generare port
    srand(time(0));
    p = generatePort();

    //citire date
    printf("Introduceti deimpartitul: ");
    scanf("%hu", &deimpartit);
    printf("Introduceti impartitorul: ");
    scanf("%hu", &impartitor);

    //convertire si trimitere date
    deimpartit = htons(deimpartit);
    impartitor = htons(impartitor);
    p = htons(p);
    send(c, &deimpartit, sizeof(deimpartit), 0);
    send(c, &impartitor, sizeof(impartitor), 0);
    send(c, &p, sizeof(p), 0);

    //TRANSFORMARE CLIENT IN SERVER UDP
    //initializare date
    int s;
    struct sockaddr_in server_nou, client_nou;
    socklen_t l_nou;

    //creare socket
    s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s < 0) {
        printf("Eroare la crearea socketului server\n");
        return 1;
}

    //setare bytes la 0 si initializare date server
    memset(&server_nou, 0, sizeof(server_nou));
    server_nou.sin_port = p;
    server_nou.sin_family = AF_INET;
    server_nou.sin_addr.s_addr = INADDR_ANY;

    if (bind(s, (struct sockaddr *) &server_nou, sizeof(server_nou)) < 0) {
        printf("Eroare la bind\n");
        return 1;
    }

    //setare bytes clienti la 0
    l_nou = sizeof(client_nou);
    memset(&client_nou, 0, sizeof(client_nou));

    //primire si convertire date
    uint16_t cod_eroare, cat, rest;
    recvfrom(s, &cod_eroare, sizeof(cod_eroare), MSG_WAITALL, (struct sockaddr *) &client_nou, &l_nou);
    recvfrom(s, &cat, sizeof(cat), MSG_WAITALL, (struct sockaddr *) &client_nou, &l_nou);
    recvfrom(s, &rest, sizeof(rest), MSG_WAITALL, (struct sockaddr *) &client_nou, &l_nou);
    cod_eroare = ntohs(cod_eroare);
    cat = ntohs(cat);
    rest = ntohs(rest);

    if(cod_eroare == 1){
            printf("Nu se poate imparti la 0!\n");
            return 1;
    }

    printf("Rezultatul impartirii este: %hu rest %hu\n", cat, rest);
    close(s);
    close(c);


    return 0;
}
