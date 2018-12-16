import requests
import matplotlib.pyplot as plt
import csv
import codecs # lib d'encodage 

# API => codes espèces poisson (codification AFB versus codification Sandre)
api_poissons = requests.get("https://hubeau.eaufrance.fr/api/v0/etat_piscicole/code_espece_poisson")
data_poissons = api_poissons.json()

poisson_code = None
poisson_nom_commun = None

dict_poissons = {}

# Vérifié: 195 espèces de poisson
for poisson in data_poissons["data"]:
    poisson_code = poisson["code"]
    poisson_nom_commun = poisson["nom_commun"]
    # On crée un dictionnaire des codes/noms des poissons à parcourir pour nos futurs WebServices
    dict_poissons[poisson_code] = poisson_nom_commun

print (len(dict_poissons)) # 195 espèces de poissons recencées

# API => lieux de pêches répertoriés procédant à la pêche électrique
code_station = None
nom_station = None
nom_cours_eau = None
nombre_operations = None
coordonnees_station = []

list_code_station = []
list_nom_station = []
list_nom_cours_eau = []
list_nombre_operations = []
list_coordonnees_station = []

# Ouverture du ficier excel
en_tetes = [u"nom commun du poisson", u"nom de la station de pêche", u"nombre d'operations menées", u"nom du cours d'eau", u"coordonnées de la station"]
csv_file = codecs.open('test.csv', mode='w', encoding='iso-8859-1')
ligneEntete = ";".join(en_tetes) + "\n"
csv_file.write(ligneEntete)

# Il s'agit de données sans restriction d'année, s'agit-il de l'année en cours?
for code in dict_poissons.keys():
    # Pour chaque sorte de poisson, on récupère les lieux où celui-ci est pêché
    api_lieu = requests.get("https://hubeau.eaufrance.fr/api/v0/etat_piscicole/lieux_peche?code_espece_poisson="+code+"&format=json")
    data_lieu = api_lieu.json()

    if data_lieu["count"] != 0 and dict_poissons[code] != '': # si pas de pêche, la station ne nous intéresse pas ici
        poisson = dict_poissons[code]
        
        for index in data_lieu["data"]:
            code_station = index["code_station"]
            nom_station = index["localisation"]
            code_cours_eau = index["code_cours_eau"]
            nom_cours_eau = index["nom_cours_eau"]
            nombre_operations = index["nombre_operations"]
            coordonnees_station = index["geometry"]["coordinates"]

            # récupération des listes parallèles codes/noms/operations/coordonnées des stations + nom du cours d'eau concerné (si dispo)
            if nom_station not in list_nom_station and code_station not in list_code_station:
                list_code_station.append(code_station)
                list_nom_station.append(nom_station)
                list_nombre_operations.append(nombre_operations)
                list_nom_cours_eau.append(nom_cours_eau)
                list_coordonnees_station.append(coordonnees_station)
                donnees = str(poisson) + "; " + str(nom_station) + "; " + str(nombre_operations)+ "; " + str(nom_cours_eau)+ "; " + str(coordonnees_station) + "\n"
                # On écrit nos données ainsi obtenues dans un fichier excel (csv)
                csv_file.write(donnees)

#print (len(list_nom_station)) # 8778
csv_file.close()

'''# Pour l'API suivante
list_code_station.sort()
list_nom_station.sort()
for nom in list_nom_station:
    print(list_nom_station)'''

'''
# API => poissons décomptés par pêche électrique dans une rivière /!\ Périodes de temps  
nombre = 0
for station in list_code_station: # 10203 stations en tout
    nombre += 1
    # Pour chaque annee
    # Pour chaque mois de l'annee (1-12)
    api_infos = requests.get("https://hubeau.eaufrance.fr/api/v0/etat_piscicole/poissons?code_station="+ station +"&annee=2017&mois_debut=1&mois_fin=12&format=json")
    data_infos = api_infos.json()
    #print(data_infos["count"])'''



