from infrastructura.repo_filme_file import RepoFilmeFile
from infrastructura.repo_clienti_file import RepoClientiFile
from infrastructura.repo_inchirieri_file import RepoInchirieriFile
from validare.validator_film import ValidareFilm
from validare.validator_client import ValidareClient
from validare.validator_inchiriere import ValidareInchiriere
from infrastructura.repo_filme import RepoFilme
from infrastructura.repo_clienti import RepoClienti
from infrastructura.repo_inchirieri import RepoInchirieri
from business.service_film import ServiceFilm
from business.service_inchiriere import ServiceInchiriere
from business.service_client import ServiceClient
from prezentare.UI import UI
from testare.teste import teste
import unittest


if __name__ == '__main__':
    validator_client = ValidareClient()
    validator_film = ValidareFilm()
    validator_inchiriere = ValidareInchiriere()
    repo_filme = RepoFilme()
    repo_clienti = RepoClienti()
    repo_inchirieri = RepoInchirieri()
    repo_filme_file = RepoFilmeFile("filme.txt")
    repo_clienti_file = RepoClientiFile("clienti.txt")
    repo_inchirieri_file = RepoInchirieriFile("inchirieri.txt")
    service_film = ServiceFilm(validator_film, repo_filme)
    service_client = ServiceClient(validator_client, repo_clienti)
    service_inchiriere = ServiceInchiriere(validator_inchiriere, repo_inchirieri, repo_clienti, repo_filme)
    consola = UI(service_client, service_film, service_inchiriere)
    testare = teste()
    testare.ruleaza_toate_testele()
    consola.run()
    unittest.main()
