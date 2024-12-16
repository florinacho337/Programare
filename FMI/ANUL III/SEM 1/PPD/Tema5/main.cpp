#include <fstream>
#include <thread>
#include <condition_variable>
#include <set>
#include <chrono>
#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <cassert>

using namespace std;

string absolutePath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema5/";

struct Node {
    int ID;
    int totalScore;
    int country;
    Node* next;
    mutex nodeMutex;

    Node(int id, int score, int c) : ID(id), totalScore(score), country(c), next(nullptr) {}
};

class LinkedList {
    Node* head;
    Node* tail;
    mutable set<int> bannedIDs;
    mutable mutex bannedMutex;

public:
    LinkedList() {
        head = new Node(-1, 0, 0);
        tail = new Node(-1, 0, 0);
        head->next = tail;
    }

    static void removeNode(Node* prev, const Node* current) {
        prev->nodeMutex.lock();
        prev->next = current->next;
        delete current;
        prev->nodeMutex.unlock();
    }

    void insertOrUpdate(const int ID, const int score, const int country) const {
        bannedMutex.lock();
        if (bannedIDs.contains(ID)) {
            bannedMutex.unlock();
            return;
        }
        bannedMutex.unlock();

        Node* prev = head;
        Node* current = head->next;

        while (current != tail) {
            if (current->ID == ID) {
                current->nodeMutex.lock();
                if (score == -1) {
                    {
                        bannedMutex.lock();
                        bannedIDs.insert(ID);
                        bannedMutex.unlock();
                    }
                    removeNode(prev, current);
                } else {
                    current->totalScore += score;
                }
                current->nodeMutex.unlock();
                return;
            }
            prev = current;
            current = current->next;
        }

        if (score == -1) {
            bannedMutex.lock();
            bannedIDs.insert(ID);
            bannedMutex.unlock();
            return;
        }

        auto newNode = new Node(ID, score, country);
        newNode->nodeMutex.lock();
        prev->nodeMutex.lock();
        newNode->next = prev->next;
        prev->next = newNode;
        newNode->nodeMutex.unlock();
        prev->nodeMutex.unlock();
    }

    static void sortListHelper(Node** sortedList, Node* newNode) {
        Node temp(-1, 0, 0);
        Node* current = &temp;
        temp.next = *sortedList;

        while (current->next != nullptr && current->next->totalScore > newNode->totalScore) {
            current = current->next;
        }

        while (current->next != nullptr && current->next->totalScore == newNode->totalScore
            && current->next->ID < newNode->ID) {
            current = current->next;
        }

        newNode->next = current->next;
        current->next = newNode;
        *sortedList = temp.next;
    }

    void sortList() const {
        Node* sortedList = nullptr;

        Node* current = head->next;

        while (current != nullptr) {
            Node *next = current->next;
            sortListHelper(&sortedList, current);
            current = next;
        }

        head->next = sortedList;
    }

    void saveToFile(const string& filename) const {
        ofstream outFile(absolutePath + filename);
        Node* current = head->next;

        while (current != tail) {
            outFile << current->ID << ", " << current->totalScore << ", " << current->country << "\n";
            current = current->next;
        }
        outFile.close();
    }

    ~LinkedList() {
        Node* current = head;
        while (current) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
};

struct SharedQueue {
    queue<pair<int, int>> q;
    mutex queueMutex;
    condition_variable conditionNotEmpty;
    condition_variable conditionNotFull;
    const size_t MAX_CAPACITY = 100;

    void push(const pair<int, int>& item) {
        unique_lock lock(queueMutex);
        conditionNotFull.wait(lock, [&]() { return q.size() < MAX_CAPACITY; });
        q.push(item);
        lock.unlock();
        conditionNotEmpty.notify_one();
    }

    pair<int, int> pop() {
        unique_lock lock(queueMutex);
        conditionNotEmpty.wait(lock, [&]() { return !q.empty(); });
        auto item = q.front();
        q.pop();
        lock.unlock();
        conditionNotFull.notify_one();
        return item;
    }
};

void readerFunction(int threadID, int numCountries, int numProblems, SharedQueue& sharedQueue, int p_r) {
    for (int country = threadID + 1; country <= numCountries; country += p_r) {
        for (int problem = 1; problem <= numProblems; ++problem) {
            string filename = "RezultateC" + to_string(country) + "_P" + to_string(problem) + ".txt";
            ifstream inFile(absolutePath + filename);

            if (inFile.is_open()) {
                int ID, score;
                while (inFile >> ID >> score) {
                    {
                        unique_lock lock(sharedQueue.queueMutex);
                        sharedQueue.conditionNotFull.wait(lock, [&sharedQueue]() {
                            return sharedQueue.q.size() < sharedQueue.MAX_CAPACITY;
                        });

                        sharedQueue.q.emplace(ID, score);
                        lock.unlock();
                    }
                    sharedQueue.conditionNotEmpty.notify_one();
                }
                inFile.close();
            }
        }
    }
}

void workerFunction(SharedQueue& sharedQueue, const LinkedList& leaderboard) {
    while (true) {
        pair<int, int> item;
        {
            unique_lock lock(sharedQueue.queueMutex);
            sharedQueue.conditionNotEmpty.wait(lock, [&sharedQueue]() {
                return !sharedQueue.q.empty();
            });

            item = sharedQueue.q.front();
            sharedQueue.q.pop();
            lock.unlock();
        }

        sharedQueue.conditionNotFull.notify_one();

        if (item.first == -1 && item.second == -1) {
            break;
        }

        leaderboard.insertOrUpdate(item.first, item.second, item.first / 100); // ID / 100 pentru țară
    }
}

void processFilesParallel(int numCountries, int numProblems, int p_r, int p_w) {
    SharedQueue sharedQueue;
    LinkedList leaderboard;

    vector<thread> readers;
    readers.reserve(p_r);
    for (int i = 0; i < p_r; ++i) {
        readers.emplace_back(readerFunction, i, numCountries, numProblems, ref(sharedQueue), p_r);
    }

    vector<thread> workers;
    workers.reserve(p_w);
    for (int i = 0; i < p_w; ++i) {
        workers.emplace_back(workerFunction, ref(sharedQueue), ref(leaderboard));
    }

    for (auto& reader : readers) {
        reader.join();
    }

    for (int i = 0; i < p_w; ++i) {
        {
            unique_lock lock(sharedQueue.queueMutex);
            sharedQueue.q.emplace(-1, -1);
        }
        sharedQueue.conditionNotEmpty.notify_all();
    }

    for (auto& worker : workers) {
        worker.join();
    }

    leaderboard.sortList();
    leaderboard.saveToFile("ClasamentP.txt");
}


void processFiles(const int numCountries, const int numProblems) {
    LinkedList leaderboard;

    for (int country = 1; country <= numCountries; ++country) {
        for (int problem = 1; problem <= numProblems; ++problem) {
            string filename = "RezultateC" + to_string(country) + "_P" + to_string(problem) + ".txt";
            ifstream inFile(absolutePath + filename);

            if (inFile.is_open()) {
                int ID, score;
                while (inFile >> ID >> score) {
                    leaderboard.insertOrUpdate(ID, score, ID / 100);
                }
                inFile.close();
            }
        }
    }

    leaderboard.sortList();
    leaderboard.saveToFile("Clasament.txt");
}

bool compareResults()
{
    FILE *fp1 = fopen((absolutePath + "Clasament.txt").c_str(), "r"),
    *fp2 = fopen((absolutePath + "ClasamentP.txt").c_str(), "r");
    char ch1 = getc(fp1);
    char ch2 = getc(fp2);

    int line = 1;

    while (ch1 != EOF && ch2 != EOF)
    {
        if (ch1 == '\n' && ch2 == '\n')
            line++;

        if (ch1 != ch2) {
            cout << "error " << line << " " << ch1 << " " << ch2 << endl;
            fclose(fp1);
            fclose(fp2);
            return false;
        }

        ch1 = getc(fp1);
        ch2 = getc(fp2);
    }

    fclose(fp1);
    fclose(fp2);
    return true;
}

int main() {
    int numCountries = 5;
    int minContestants = 80;
    int maxContestants = 100;
    int numProblems = 10;
    int numWorkers = 2;
    int numReaders = 4;

    // generateInputFiles(numCountries, minContestants, maxContestants, numProblems);
    auto startTime = chrono::high_resolution_clock::now();
    // 1. SECVENTIAL
    // processFiles(numCountries, numProblems);
    // 2. PARALEL - BLOCARE NOD
    processFilesParallel(numCountries, numProblems, numReaders, numWorkers);
    auto endTime = chrono::high_resolution_clock::now();
    double elapsed_time_ms = chrono::duration<double, std::milli>(endTime - startTime).count();

    assert(compareResults());

    cout << elapsed_time_ms << endl;
    return 0;
}