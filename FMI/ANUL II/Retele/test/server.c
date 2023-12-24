#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>

char* get_adresa(struct in_addr in){
        static char b[18];
        unsigned char *bytes = (unsigned char *) &in;
        snprintf(b, sizeof(b), "%d.%d.%d.%d", bytes[0], bytes[1], bytes[2], bytes[3]);
        return b;
}

int main(int argc, char** argv) {
    if(argc < 2){
            printf("Introduceti un port!\n");
            return 1;
    }

    //initializare date
    int s;
    struct sockaddr_in server, client;
    int c;
    socklen_t l;
    uint16_t port;

    //creare socket
    s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        printf("Eroare la crearea socketului server\n");
        return 1;
    }

    //setare bytes la 0
    memset(&server, 0, sizeof(server));

    //validare port
    port = atoi(argv[1]);
    if(!(port > 1024 && port < 65356)){
            printf("Port invalid!\n");
            return 1;
    }

    //initializare date server
    server.sin_port = htons(port);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;

if (bind(s, (struct sockaddr*)&server, sizeof(server)) < 0) {
        printf("Eroare la bind\n");
        return 1;
    }

    listen(s, 5);

    //setare bytes la 0
    l = sizeof(client);
    memset(&client, 0, sizeof(client));

    while(1){
            uint16_t deimpartit, impartitor, p;
            char* adresa;

            //acceptare clienti
            c = accept(s, (struct sockaddr*)&client, &l);


            if(fork() == 0){
                    //primire si convertire date
                    recv(c, &deimpartit, sizeof(deimpartit), MSG_WAITALL);
                    recv(c, &impartitor, sizeof(impartitor), MSG_WAITALL);
                    recv(c, &p, sizeof(p), MSG_WAITALL);
                    deimpartit = ntohs(deimpartit);
                    impartitor = ntohs(impartitor);
                    p = ntohs(p);

                    //afisare date primite + adresa ip si portul clientului
                    printf("Deimpartit: %hu\n", deimpartit);
                    printf("Impartitor: %hu\n", impartitor);
                    printf("Port primit: %hu\n", p);
                    adresa = get_adresa(client.sin_addr);
                    printf("Adresa clientului este: %s\n", adresa);
                    printf("Port client: %hu\n", port);

                    //prelucrare date
                    uint16_t cat, rest, cod_eroare;
                    if(impartitor == 0){
                            cod_eroare = 1;
                            cat = 0;
                            rest = 0;
                    } else{
                            cod_eroare = 0;
                            cat = deimpartit / impartitor;
                            rest = deimpartit - cat*impartitor;
                    }

                    //TRANSFORMARE SERVER IN CLIENT UDP
                    //initializare date
                    int c_nou;
struct sockaddr_in server_nou;

                    //creare socket
                    c_nou = socket(AF_INET, SOCK_DGRAM, 0);
                    if (c_nou < 0) {
                            printf("Eroare la crearea socketului client\n");
                            return 1;
                    }

                    //setare bytes la 0 si initializare date server
                    memset(&server_nou, 0, sizeof(server_nou));
                    server_nou.sin_port = htons(p);
                    server_nou.sin_family = AF_INET;
                    server_nou.sin_addr.s_addr = inet_addr(adresa);

                    //convertire si trimitere date
                    cod_eroare = htons(cod_eroare);
                    cat = htons(cat);
                    rest = htons(rest);
                    sendto(c_nou, &cod_eroare, sizeof(cod_eroare), 0, (struct sockaddr *) &server_nou, sizeof(server_nou));
                    sendto(c_nou, &cat, sizeof(cat), 0, (struct sockaddr *) &server_nou, sizeof(server_nou));
                    sendto(c_nou, &rest, sizeof(rest), 0, (struct sockaddr *) &server_nou, sizeof(server_nou));

                    close(c_nou);
                    close(c);
                    exit(0);
            }

    }
    return 0;
}
