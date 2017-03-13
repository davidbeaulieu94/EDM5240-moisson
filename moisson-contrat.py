#coding: utf-8

# Il faut importer plusieurs modules afin de faire fonctionner le script, incluant BeautifulSoup.
import csv
import requests
from bs4 import BeautifulSoup
#J'importe le module time maintenant au-cas où j'en ai de besoin plus tard.
import time

#Le guide d'utilisation de BeautifulSoup: http://jhroy.ca/uqam/edm5240/BeautifulSoup-DocAbregee.pdf

#Pour ce travail, je vais moissoner sur le site des affaires étrangères. Je regarderai les contrats octroyés lors du troisième trimeste de 2016-2017.
url= 'http://w03.international.gc.ca/dc/index_fa-ae.aspx?lang=fra&p=3&r=51'

#On va créer une entête enfin de s'identifier sur le site où nous allons prendre nos donnés. Cela va leur permettre de savoir qui nous sommes et un peu notre motif à savoir pourquoi nous regardons leurs donnés. 
entetes={
    'User-Agent':'David Beaulieu - Étudiant en journalisme à l UQAM', 
    'From':'beaulieu.david.4@courrier.uqam.ca'
}


#Cette formule permet de dire à notre script d'aller chercher l'information sur l'url.
contenu = requests.get(url, headers=entetes)

#Ensuite, on demande d'extraire le code HTML du site que nous moissonons.
page = BeautifulSoup(contenu.text,'html.parser')

#On va créer différentes listes afin d'isoler les différents éléments que nous allons mettre dans le print final. 
date=[]
vendeur=[]
montant=[]

#Les éléments que nous avons besoin se trouvent dans un tableau sur le site des affaires étrangères.
#Les données qui nous intéresse se trouvent dans des <td>. Chacun des éléments nécessaire sont dans des classes spécifiques. Ici, on utilise la classe 'cdReportDate'
#Dans cette première ligne, nous allons prendre tous les dates qui se trouvent dans la classe appropriée. 
for ligne in page.find_all('td',class_='cdReportDate'):
#Après cette manipulation, les dates seront regroupés pour la liste.
#J'ai aussi mis le .text ici afin de ne prendre que le texte, pour ne pas avoir les <td>, </td>, etc.
    date.append(ligne.text)

#Ici, nous faisons la même chose afin d'avoir les éléments des vendeurs, qui se trouvent dans la classe 'cdVendor'
for ligne in page.find_all('td',class_='cdVendor'):
    vendeur.append(ligne.text)

#Même chose avec la classe 'cdReportContractValue'    
for ligne in page.find_all('td',class_='cdReportContractValue'):
    montant.append(ligne.text)
  
#Pour le script final, nous associons les informations nécessaires ensemble afin d'associer le bon élément à la bonne place. 
#Les currents vont prendre les donnés ligne par ligne afin de former la phrase déterminer par le print. 
#Dans le format, on place dans l'ordre les currents dans l'ordre qu'on les veut.
for index in range(len(date)):
    currentdate=date[index]
    currentvendeur=vendeur[index]
    currentmontant=montant[index]
    print('En date du {}, un contrat a été attribué à {} pour un montant de {}.'.format(currentdate,currentvendeur,currentmontant))
#Dans le cas que j'ai pris, je ne voulais qu'avoir les dates, les vendeurs et les montants. Il y avait aussi la catégorie description, mais le nombre de caractère est vaste et je ne trouvais pas l'information particulièrement nécessaire. 
#Aussi, dans les montants, il arrive que nous avons (a) devant le nombre dans le script. Ceci avise qu'il y a eu une modification du contrat, que nous pouvons retrouver, avec une explication, sur le site d'origine. 

#En-dessous, il y a diverse démarche que j'ai entrepris afin d'élaborer mon script, certaines ont été un échec et d'autres ont été des étapes afin de trouver des informations avec BeautifulSoup

#Les prints suivant me permettaient d'identifier certains éléments dans le code HTML comme nous l'avons vu en classeé
# print(page.find('div', id='TDReport'))

#Ce print a été le plus utile afin de m'aider à isoler les informations que j'avais de besoin
# print(page.find_all('td', class_='cdReportDate'))

#En faisant des tests, je me suis rendu compte qu'on ne peut pas associer .find_all et .text. J'avais des erreurs à chaque fois, alors j'ai rogné l'idée. 
# print(page.find_all('td', class_=cdReportDate).text)

#Autres éléments de BeautifulSoup.
# print(page.find('a')['href'])

#Initiealement, je ne trouvais pas comment aller chercher mes éléments pour les inclures dans des listes. En fait, je me suis rendu compte qu'il fallait que j'inclue la class_ dans mon for ligne in _________.
#J'avais la liste donnee en plus dans cette tentative ratée.
# donnee=[]
# print(page.find('td'))

# for ligne2 in donnee: 
#     if ligne2=='cdReportDate':
#         date.append('')

# for ligne2 in donnee:
#     if ligne2=='cdVendor':
#         vendeur.append('')

# for ligne2 in donnee:
#     if ligne2=='cdReportContractValue':
#         montant.append('')


#Une autre tentative, où je ne comprennais pas le problème avant de me rendre compte que je ne précisais pas la class au bon endroit.
# for ligne in page.find_all('td',class_):
#     if class_=='cdReportDate':
#         date.append(ligne)

# for ligne in page.find_all('td'):
#     if class_=='cdVendor':
#         vendeur.append(ligne)

# for ligne in page.find_all('td'):
#     if class_=='cdReportContractValue':
#         montant.append(ligne)
        
#Les deux prints suivants sont aussi des tests que j'ai fait après avoir discuté de mes problèmes avec Shannon. Toutefois, ils ne furent pas concluant. 
# print(page.find_all('td')[1:]) (Temporaire)
# for ligne in page.find_all('tr')[1:]

#La boucle ici est fonctionnelle, comme nous l'avions vu en classe. J'aurais pu l'utiliser afin d'avoir toute les informations et je peux toujours l'utiliser séparément de mon print final pour avoir les sites de chacun des éléments.
#Toutefois, je préférais faire un print plus propre avec seulement quelques informations plus essentielles à mon avis. 
# for ligne in page.find_all('tr')[1:]:
#     # print(ligne.a['href']) (Sauf luiiii)
#     debut = 'http://w03.international.gc.ca/dc/'
#     lien = debut + ligne.a['href']
#     print(lien)
#     contenu2 = requests.get(lien, headers=entetes)
#     page2 = BeautifulSoup(contenu2.text,'html.parser')
#     for rang in page2.find_all('tr'):
#         try:
#             print(rang.td.text)
#         except:
#             print('Ya rien icitte')

#Le travail est terminé! Tout est fonctionnel, alors j'espère avoir une bonne note fonctionnelle aussi ;)
#BYE
