#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <random>
#include <chrono>
#include <mutex>
#include <queue>
#include <thread>
#include <cassert>

using namespace std;
string absolutePath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema4/";

struct Node {
    int ID;
    int totalScore;
    Node* next;
    Node(const int id, const int score) : ID(id), totalScore(score), next(nullptr) {}
};

class LinkedList {
    Node* head;
    set<int> bannedIDs;
    mutex listMutex;

    void reposition(const int score, const int ID, Node *newNode) {
        Node** current = &head;
        while (*current && (*current)->totalScore >= score) {
            current = &(*current)->next;
        }
        while (*current && (*current)->totalScore == score && (*current)->ID > ID) {
            current = &(*current)->next;
        }
        newNode->next = *current;
        *current = newNode;
    }

    void remove(const int ID) {
        Node** current = &head;
        while (*current && (*current)->ID != ID) {
            current = &(*current)->next;
        }
        if (*current) {
            Node* temp = *current;
            *current = (*current)->next;
            delete temp;
        }
    }

public:
    LinkedList() : head(nullptr) {}

    void insertOrUpdate(const int ID, const int score) {
        lock_guard lock(listMutex); // comment in secvential variant
        if (bannedIDs.contains(ID)) return;

        if (score == -1) {
            remove(ID);
            bannedIDs.insert(ID);
            return;
        }

        Node** existingNode = &head;
        while (*existingNode && (*existingNode)->ID != ID) {
            existingNode = &(*existingNode)->next;
        }

        if (*existingNode) {
            (*existingNode)->totalScore += score;

            Node* temp = *existingNode;
            *existingNode = (*existingNode)->next;

            reposition(temp->totalScore, temp->ID, temp);
        } else {
            const auto newNode = new Node(ID, score);
            reposition(score, ID, newNode);
        }
    }

    void saveToFile(const string& filename) const {
        ofstream outFile(absolutePath + filename);
        Node* current = head;
        while (current) {
            outFile << current->ID << ", " << current->totalScore << "\n";
            current = current->next;
        }
        outFile.close();
    }

    ~LinkedList() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
};

void generateInputFiles(const int numCountries, const int minParticipants, const int maxParticipants, const int numProblems) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> scoreDis(1, 10);
    uniform_real_distribution<> probabilityDis(0.0, 1.0);

    for (int country = 1; country <= numCountries; ++country) {
        int numParticipants = uniform_int_distribution<>(minParticipants, maxParticipants)(gen);

        for (int problem = 1; problem <= numProblems; ++problem) {
            string fileName = "RezultateC" + to_string(country) + "_P" + to_string(problem) + ".txt";
            ofstream outFile(absolutePath + fileName);

            for (int id = 1; id <= numParticipants; ++id) {
                double skipChance = probabilityDis(gen);
                double fraudChance = probabilityDis(gen);

                if (fraudChance < 0.02) {
                    outFile << (100 * country) + id << " -1\n";
                } else if (skipChance > 0.10) {
                    int score = scoreDis(gen);
                    outFile << (100 * country) + id << " " << score << "\n";
                }
            }

            outFile.close();
        }
    }
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
                    leaderboard.insertOrUpdate(ID, score);
                }
                inFile.close();
            }
        }
    }

    leaderboard.saveToFile("Clasament.txt");
}

struct SharedQueue {
    queue<pair<int, int>> q;
    mutex queueMutex;
    counting_semaphore<> available{0};

    void push(const pair<int, int> &item) {
        lock_guard lock(queueMutex);
        q.push(item);
        available.release();
    }

    pair<int, int> pop() {
        available.acquire();
        lock_guard lock(queueMutex);
        auto item = q.front();
        q.pop();
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
                    sharedQueue.push({ID, score});
                }
                inFile.close();
            }
        }
    }
}

void workerFunction(SharedQueue& sharedQueue, LinkedList& leaderboard, const atomic<bool>& doneReading) {
    while (!doneReading || !sharedQueue.q.empty()) {
        auto item = sharedQueue.pop();
        leaderboard.insertOrUpdate(item.first, item.second);
    }
}

void processFilesParallel(int numCountries, int numProblems, int p_r, int p_w) {
    SharedQueue sharedQueue;
    LinkedList leaderboard;
    atomic doneReading{false};

    vector<thread> readers;
    readers.reserve(p_r);
    for (int i = 0; i < p_r; ++i) {
        readers.emplace_back(readerFunction, i, numCountries, numProblems, ref(sharedQueue), p_r);
    }

    vector<thread> workers;
    workers.reserve(p_w);
    for (int i = 0; i < p_w; ++i) {
        workers.emplace_back(workerFunction, ref(sharedQueue), ref(leaderboard), ref(doneReading));
    }

    for (auto& reader : readers) {
        reader.join();
    }
    doneReading = true;

    for (auto& worker : workers) {
        worker.join();
    }

    leaderboard.saveToFile("ClasamentP.txt");
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
    int numProc = 6;
    int numReaders = 2;

    // generateInputFiles(numCountries, minContestants, maxContestants, numProblems);
    auto startTime = chrono::high_resolution_clock::now();
    // 1. SECVENTIAL
    processFiles(numCountries, numProblems);
    // 2. PARALEL - BLOCARE TOATA LISTA
    // processFilesParallel(numCountries, numProblems, numReaders, numProc - numReaders);
    auto endTime = chrono::high_resolution_clock::now();
    double elapsed_time_ms = chrono::duration<double, std::milli>(endTime - startTime).count();

    cout << elapsed_time_ms << endl;
    return 0;
}
