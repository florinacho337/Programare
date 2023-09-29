#include <assert.h>
#include <stdio.h>
#include "service.h"
#include "MyList.h"
#include "domain.h"
#include "teste.h"
#include <malloc.h>
#include <string.h>

//ruleaza testele pt domain
void teste_domain()
{
    printf("start teste domain...\n");
    char *tip = (char*)malloc(3);
    char *descriere = (char*)malloc(3);
    strncpy(tip, "ok", 3);
    strncpy(descriere, "ok", 3);
    Tranzactie* test = creeazaTranzactie(2, 3, tip, descriere);
    assert(test->zi==2);
    assert(test->suma==3);
    assert(strcmp(test->tip, tip) == 0);
    assert(strcmp(test->descriere, descriere) == 0);
    free(tip);
    free(descriere);
    destroyTranzactie(test);
    printf("finish teste domain...\n");
}

//ruleaza testele pt functiile din repo
void teste_repo()
{
    printf("start teste repo...\n");
    testCreateList();
    testIterateList();
    testCopyList();
    testResize();
    testListOfLists();
    testListOfInts();
    testRemoveLast();
    printf("finish teste repo...\n");

}

//ruleaza testele pt functiile din service
void  teste_service()
{
    printf("start teste service...\n");
    Service repo_test_service;
    repo_test_service = createService();
    service_add(&repo_test_service, 2, 3, "ok", "ok");
    Tranzactie *tr = (Tranzactie*)get(repo_test_service.listaTranzactii, 0);
    assert(tr->zi==2);
    assert(tr->suma==3);
    assert(strcmp(tr->tip,"ok") == 0);
    assert(strcmp(tr->descriere,"ok")==0);
    service_undo(&repo_test_service);
    assert(size(repo_test_service.listaTranzactii) == 0);
    assert(service_undo(&repo_test_service) == 1);
    service_add(&repo_test_service, 2, 3, "ok", "ok");
    service_modify(&repo_test_service, 0, 3, 10, "notok", "maiok");
    tr = (Tranzactie*)get(repo_test_service.listaTranzactii, 0);
    assert(tr->zi==3);
    assert(tr->suma==10);
    assert(strcmp(tr->tip,"notok")==0);
    assert(strcmp(tr->descriere,"maiok")==0);
    service_undo(&repo_test_service);
    tr = (Tranzactie*)get(repo_test_service.listaTranzactii, 0);
    assert(tr->zi==2);
    assert(tr->suma==3);
    assert(strcmp(tr->tip,"ok") == 0);
    assert(strcmp(tr->descriere,"ok")==0);
    service_delete(&repo_test_service, 0);
    assert(size(repo_test_service.listaTranzactii) == 0);
    service_undo(&repo_test_service);
    assert(size((repo_test_service.listaTranzactii)) == 1);
    service_delete(&repo_test_service, 0);
    service_add(&repo_test_service, 2, 3, "intrare", "ok");
    service_add(&repo_test_service, 52, 123, "iesire", "ok");
    service_add(&repo_test_service, 12, 34, "iesire", "ok");
    MyList* repo_nou;
    repo_nou = service_view_type(&repo_test_service, "intrare");
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(strcmp(tr->tip,"intrare") == 0);
    destroyList(repo_nou);
    repo_nou = service_view_type(&repo_test_service, "iesire");
    tr = (Tranzactie*)get(repo_nou, 1);
    assert(strcmp(tr->tip,"iesire")==0);
    destroyList(repo_nou);
    repo_nou = service_view_sum(&repo_test_service, 90, 1);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->suma==123);
    destroyList(repo_nou);
    repo_nou = service_view_sum(&repo_test_service, 90, 2);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->suma==3);
    destroyList(repo_nou);
    repo_nou = service_select_sort(&repo_test_service, 1, 1);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->zi==2);
    tr = (Tranzactie*)get(repo_nou, 1);
    assert(tr->zi==12);
    tr = (Tranzactie*)get(repo_nou, 2);
    assert(tr->zi==52);
    destroyList(repo_nou);
    repo_nou = service_select_sort(&repo_test_service, 1, 2);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->zi==52);
    tr = (Tranzactie*)get(repo_nou, 1);
    assert(tr->zi==12);
    tr = (Tranzactie*)get(repo_nou, 2);
    assert(tr->zi==2);
    destroyList(repo_nou);
    repo_nou = service_select_sort(&repo_test_service, 2, 1);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->suma==3);
    tr = (Tranzactie*)get(repo_nou, 1);
    assert(tr->suma==34);
    tr = (Tranzactie*)get(repo_nou, 2);
    assert(tr->suma==123);
    destroyList(repo_nou);
    repo_nou = service_select_sort(&repo_test_service, 2, 2);
    tr = (Tranzactie*)get(repo_nou, 0);
    assert(tr->suma==123);
    tr = (Tranzactie*)get(repo_nou, 1);
    assert(tr->suma==34);
    tr = (Tranzactie*)get(repo_nou, 2);
    assert(tr->suma==3);
    destroyList(repo_nou);
    destroyService(&repo_test_service);
    printf("finish teste service...\n");
}

void run_teste()
{
    teste_domain();
    teste_repo();
    teste_service();
}