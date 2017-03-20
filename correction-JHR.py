#coding: utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

# Il faut importer plusieurs modules afin de faire fonctionner le script, incluant BeautifulSoup.
import csv
import requests
from bs4 import BeautifulSoup
#J'importe le module time maintenant au-cas où j'en ai de besoin plus tard.
import time

#Le guide d'utilisation de BeautifulSoup: http://jhroy.ca/uqam/edm5240/BeautifulSoup-DocAbregee.pdf

#Pour ce travail, je vais moissoner sur le site des affaires étrangères. Je regarderai les contrats octroyés lors du troisième trimeste de 2016-2017.
url= 'http://w03.international.gc.ca/dc/index_fa-ae.aspx?lang=fra&p=3&r=51'

fichier = "contrats-AffEtrangeres-JHR.csv"

#On va créer une entête enfin de s'identifier sur le site où nous allons prendre nos donnés. Cela va leur permettre de savoir qui nous sommes et un peu notre motif à savoir pourquoi nous regardons leurs donnés. 
entetes={
    'User-Agent':'David Beaulieu - Étudiant en journalisme à l UQAM', 
    'From':'beaulieu.david.4@courrier.uqam.ca'
}

### Un trimestre, c'est bien
### Tous les trimestres, c'est mieux! :)
### Ici, la fin de l'URL était un nombre séquentiel où 1 correspond au premier trimestre disponible
### On est rendu au 51e trimestre
### Donc, il suffit de se créer une boucle comme suit:

for trimestre in range(1,52):
	url = "http://w03.international.gc.ca/dc/index_fa-ae.aspx?lang=fra&p=3&r={}".format(trimestre)

### On indente tout le reste pour le faire entrer dans cette boucle

	#Cette formule permet de dire à notre script d'aller chercher l'information sur l'url.
	contenu = requests.get(url, headers=entetes)

	#Ensuite, on demande d'extraire le code HTML du site que nous moissonons.
	page = BeautifulSoup(contenu.text,'html.parser')

	#On va créer différentes listes afin d'isoler les différents éléments que nous allons mettre dans le print final. 
	# date=[]
	# vendeur=[]
	# montant=[]

	# #Les éléments que nous avons besoin se trouvent dans un tableau sur le site des affaires étrangères.
	# #Les données qui nous intéresse se trouvent dans des <td>. Chacun des éléments nécessaire sont dans des classes spécifiques. Ici, on utilise la classe 'cdReportDate'
	# #Dans cette première ligne, nous allons prendre tous les dates qui se trouvent dans la classe appropriée. 
	# for ligne in page.find_all('td',class_='cdReportDate'):
	# #Après cette manipulation, les dates seront regroupés pour la liste.
	# #J'ai aussi mis le .text ici afin de ne prendre que le texte, pour ne pas avoir les <td>, </td>, etc.
	#     date.append(ligne.text)

	# #Ici, nous faisons la même chose afin d'avoir les éléments des vendeurs, qui se trouvent dans la classe 'cdVendor'
	# for ligne in page.find_all('td',class_='cdVendor'):
	#     vendeur.append(ligne.text)

	# #Même chose avec la classe 'cdReportContractValue'    
	# for ligne in page.find_all('td',class_='cdReportContractValue'):
	#     montant.append(ligne.text)
	  
	# #Pour le script final, nous associons les informations nécessaires ensemble afin d'associer le bon élément à la bonne place. 
	# #Les currents vont prendre les donnés ligne par ligne afin de former la phrase déterminer par le print. 
	# #Dans le format, on place dans l'ordre les currents dans l'ordre qu'on les veut.
	# for index in range(len(date)):
	#     currentdate=date[index]
	#     currentvendeur=vendeur[index]
	#     currentmontant=montant[index]
	#     print('En date du {}, un contrat a été attribué à {} pour un montant de {}.'.format(currentdate,currentvendeur,currentmontant))

#Dans le cas que j'ai pris, je ne voulais qu'avoir les dates, les vendeurs et les montants. Il y avait aussi la catégorie description, mais le nombre de caractère est vaste et je ne trouvais pas l'information particulièrement nécessaire. 
#Aussi, dans les montants, il arrive que nous avons (a) devant le nombre dans le script. Ceci avise qu'il y a eu une modification du contrat, que nous pouvons retrouver, avec une explication, sur le site d'origine. 

### [...]

#Le travail est terminé! Tout est fonctionnel, alors j'espère avoir une bonne note fonctionnelle aussi ;)
#BYE

### Script fonctionnel, en effet, qui ramasse des infos intéressantes

### En fait, tu t'es un peu compliqué la vie en recueillant l'info du tableau une colonne à la fois
### Il aurait été plus simple de recueillir une ligne à la fois, puisque c'est comme ça (une ligne à la fois) qu'on peut créer un CSV à la fin, CSV, d'ailleurs, qui manque dans ton script

### Voici, donc, faire d'une pierre deux coups : se simplifier la vie et créer un CSV

### D'abord, on ramasse tous les <tr>

	for ligne in page.find("table", class_="cdReport").find("tbody").find_all("tr"):
		# print(ligne)

		date = ligne.find("td",class_="cdReportDate").text.strip()
		fournisseur = ligne.find("td",class_="cdVendor").text.strip()
		description = ligne.find("td", class_="cdDescription").text.strip() ### Je trouve que c'est une info pertinente :)
		montant = ligne.find("td",class_="cdReportContractValue").text.strip()
		if montant[0:3] == "(a)": ### Je crée une variable pour identifier les cas où le contrat est en fait un ajustement à un contrat précédent
			ajout = "Oui"
			montant = montant[4:] ### Pour enlever le «(a)» s'il est là
		else:
			ajout = "Non"
		montant = montant[:-2] ### Pour enlever le signe «$»
		montant = montant.replace("\xa0", "").replace(",",".") ### Pour enlever les espaces insécables des montants et remplacer la virgule par un point (pour les décimales)
		montant = float(montant) ### Pour transformer le montant (une chaîne de caractères) en «float» (nombre avec décimales) afin, dans une étape suivante, de faire des calculs sur ces données

		contrat = [trimestre,date,fournisseur,description,ajout,montant] ### Je place les infos recueillies sur un contrat dans une liste

		print(contrat) ### Affichage pour vérifier

		### Puis, j'écris cette liste dans un CSV
		### En fait, ça ne va faire qu'ajouter une ligne à mon CSV

		achille = open(fichier,"a")
		talon = csv.writer(achille)
		talon.writerow(contrat)

### Au final, ça nous permet de récolter 35000 contrats!
