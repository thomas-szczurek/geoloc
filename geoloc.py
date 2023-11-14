# -*- coding: utf8 -*-

# TODO LIST

import csv
import unicodedata
from qgis.core import *
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from PyQt5.QtWidgets import QFileDialog

# Fonction servant à supprimer les accents d'un texte
def suppr_accents(chaine):
    chaine = unicodedata.normalize('NFD', chaine)\
    .encode('ascii', 'ignore')\
    .decode("utf-8")
    return chaine

#  Fonction servant à charger un csv en tant que liste
def open_list_csv(file):
    reader = csv.reader(open("\\"+file), delimiter =";")
    result = []
    for row in reader:
        result.append(row[0])
    return result

#  Fonction servant à charger un dico de listes csv : clé = liste, en lignes (ex : dico de correspondances)
def open_dico_csv(file):
    reader = csv.reader(open("\\"+file), delimiter =";")
    result = {}
    for row in reader:
        key = row[0]
        result[key] = row[1:]
    return result

# Fonction de suppression des valeurs vides dans un dico de listes chargé à partir d'un csv
def clean_dico(dico):
    for key, value in dico.items():
        temp_list = value
        while ("" in temp_list) is True:
            temp_list.remove("")
        else:
            pass
    return dico

# Fonction vérifiant la présence dans une chaine de texte de mots présent dans un dico et renvois sa clef
def key_dico(dico, chaine):
    for key, value in dico.items():
        for i, elements in enumerate(value):
            word_checked = value[i]
            if (word_checked in chaine) == True:
                return key
            else:
                pass
                
 # Fonction vérifiant la présence dans une chaine de texte de mots présent dans une liste
def check_list(liste, chaine):
    for i, elements in enumerate(liste):
        word_checked = liste[i]
        if (word_checked in chaine) == True:
                return word_checked.strip()

                
# Fonction supprimant les mots d'une liste dans une chaine
def del_list (liste, chaine):
    for i, elements in enumerate(liste):
        word_checked = liste[i]
        if (word_checked in adresse) == True:
            chaine_part = chaine.partition(word_checked)
            chaine = chaine_part[0]+chaine_part[2]
            return chaine
        else:
            pass
            
# Fonction recupérant les x (dans un champ) d'une selection d'une couche Qgis
def getx(couche):
    couche.selectByExpression("\"Adresse\" like '{}'".format(adresse_true), QgsVectorLayer.SetSelection)
    features = couche.selectedFeatures()
    for f in features:
        x = f.attribute(3)
        return x

# Fonction recupérant les x (dans un champ) d'une selection d'une couche Qgis  
def gety(couche):
    couche.selectByExpression("\"Adresse\" like '{}'".format(adresse_true), QgsVectorLayer.SetSelection)
    features = couche.selectedFeatures()
    for f in features:
        y = f.attribute(4)
        return y

# Définition des chemins de fichiers
file_path = QFileDialog().getExistingDirectory(None, "Selectionnez le dossier des adresses")
if file_path == '':
    iface.messageBar().pushMessage("Geocodage annulé","Pas de dossier selectionné", level=Qgis.Critical)
    raise ValueError
adresses_path = file_path+"/adresses.csv"
export_path = file_path+"/export.csv"
dico_type_voie_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\dico_type_voies.csv"
dico_nom_voie_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\dico_nom_voies.csv"
dico_repet_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\dico_repetitions.csv"
dico_courees_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\dico_courees.csv"
dico_mots_suff_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\liste_mots_a_suff.csv"
dico_mots_del_path = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Scripts\geoloc\csv_files\liste_mots_a_del.csv"

# Chargement des listes et dictionnaires csv
type_voie = open_dico_csv(dico_type_voie_path)
type_voie = clean_dico(type_voie)
nom_voie = open_dico_csv(dico_nom_voie_path)
nom_voie = clean_dico(nom_voie)
repetition = open_dico_csv(dico_repet_path)
repetition = clean_dico(repetition)
courees = open_dico_csv(dico_courees_path)
courees = clean_dico(courees)
mots_a_suff = open_list_csv(dico_mots_suff_path)
mots_a_del = open_list_csv(dico_mots_del_path)

# Création du csv d'export
with open(export_path,'w', newline='') as exportcsv:
    export_file = csv.writer(exportcsv, delimiter = ';')
    export_file.writerow(['ident', 'adresse', 'num_true', 'repet_true', 'type_true', 'nom_true', 'adresse_true', 'commune_true', 'Xl93', 'Yl93'])

# Chargement des adresses
reader = csv.reader(open(adresses_path), delimiter =";")
adresses_file = {}
for row in reader:
    key = row[0]
    adresses_file[key] = row[1]
    
# Ouverture des couches de seuils
seuils_gpkg = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Replicat equipmnt\FONDS DE PLAN\Voie\Seuils\seuils_pour_geoloc.gpkg|layername=seuils_Lille"
vlayerl = iface.addVectorLayer("\\"+seuils_gpkg, "Seuils_Lille", "ogr")
seuils_gpkg = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Replicat equipmnt\FONDS DE PLAN\Voie\Seuils\seuils_pour_geoloc.gpkg|layername=seuils_Hellemmes"
vlayerh = iface.addVectorLayer("\\"+seuils_gpkg, "Seuils_Hell", "ogr")
seuils_gpkg = "\eureka\commun\equipemt\SIG Data Lille\QGIS\Replicat equipmnt\FONDS DE PLAN\Voie\Seuils\seuils_pour_geoloc.gpkg|layername=seuils_Lomme"
vlayerlo = iface.addVectorLayer("\\"+seuils_gpkg, "Seuils_Lomme", "ogr")

# MessageBar progression
len_adresses = len(adresses_file)
progressMessageBar = iface.messageBar().createMessage("Geocodage...")
progress = QProgressBar()
progress.setMaximum(len_adresses)
progressMessageBar.layout().addWidget(progress)
iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
av = 0

# \\\\\\\\\\\ TRAITEMENT DES ADRESSES \\\\\\\\\\
for ident_s, adresse_s in adresses_file.items():
    adresse = adresse_s
    ident = ident_s
    # Formatage de baseseuil
    adresse = adresse.upper()
    adresse = adresse.replace(","," ")
    adresse = adresse.replace("'"," ")
    adresse = adresse.replace('\'',' ')
    adresse = suppr_accents(adresse)
    adresse = " ".join(adresse.split())
    adresse = " " + adresse + " "
    num_true = ""
    # Detection commune
    commune_true = "LILLE"
    if ("HELLEMMES" or "59260") in adresse:
        commune_true = "HELLEMMES"
    elif ("LOMME" or "59160") in adresse:
        commune_true = "LOMME"
    else:
        pass
    if "MARAIS DE LOMME" in adresse:
        commune_true = "LILLE"
    else:
        pass
    # Détection cours et courées
    if key_dico(courees, adresse) is None:
        # Détection du type de voie
        type_true = "non ident"
        if key_dico(type_voie, adresse) is None:
            pass
        else:
            type_true = key_dico(type_voie, adresse)
        # Détection du nom de voie
        nom_true = "non ident"
        if key_dico(nom_voie, adresse) is None:
            pass
        else:
            nom_true = key_dico(nom_voie, adresse)
        if nom_true == "GHESQUIERES" and commune_true == "HELLEMMES":
            nom_true = "HENRI GHESQUIERES"
        else:
            pass
        if nom_true == "GHESQUIERES" and commune_true == "LOMME":
            nom_true = "HENRI GHESQUIERE"
        else:
            pass
        if nom_true == "GHESQUIERES" and commune_true == "LILLE":
            nom_true = "VIRGINIE GHESQUIERE"
        else:
            pass
        if nom_true == "ALBERT" and commune_true == "LOMME" and ("THOMAS" in adresse):
            nom_true = "ALBERT THOMAS"
        elif nom_true == "ALBERT" and commune_true == "LOMME" and ("CAMUS" in adresse):
            nom_true = "ALBERT CAMUS"
        else:
            pass
        if nom_true == "DELESALLE" and commune_true == "HELLEMMES":
            nom_true = "DELESALLE"
        elif nom_true == "DELESALLE" and ("EDOUARD" in adresse):
            nom_true = "EDOUARD DELESALLE"
        elif nom_true == "DELESALLE" and ("CHARLES" in adresse):
            nom_true = "CHARLES DELESALLE"
        else:
            pass
        if nom_true == "DU MARAIS" and commune_true == "LILLE":
            nom_true = "DU MARAIS DE LOMME"
        else:
            pass
        if nom_true == "DU MARAIS" and commune_true == "LOMME":
            nom_true = "DU MARAIS"
        else:
            pass
        if nom_true == "ALBERT" and ("THOMAS" in adresse):
            nom_true = "ALBERT THOMAS"
        else:
            pass
        if nom_true == "FERRER" and (("FRANCESCO" in adresse) or ("FRANCISCO" in adresse)):
            nom_true = "FRANCISCO FERRER"
        else:
            pass
        if nom_true == "LEGRAND" and ("PIERRE" in adresse):
            nom_true = "PIERRE LEGRAND"
        else:
            pass
        if nom_true == "LEGRAND" and ("GERY" in adresse):
            nom_true = "GERY LEGRAND"
        else:
            pass
        if nom_true == "DU TEMPLE" and ("HAYE" in adresse):
            nom_true = "DE LA HAYE DU TEMPLE"
        else:
            pass
        if nom_true == "ADOLPHE" and ("CASSE" in adresse):
            nom_true = "ADOLPHE CASSE"
        else:
            pass
        if nom_true == "LEROUX" and ("FAUQUEMONT" in adresse):
            nom_true = "LEROUX DE FAUQUEMONT"
        else:
            pass
        if nom_true == "LEFEBVRE" and ("JULES" in adresse):
            nom_true = "JULES LEFEBVRE"
        else:
            pass
        if nom_true == "SAINT LOUIS" and ("EGLISE" in adresse):
            nom_true = "DE L EGLISE-SAINT-LOUIS"
        else:
            pass
        if nom_true == "DES JARDINS" and ("CAULIER" in adresse):
            nom_true = "DES JARDINS CAULIER"
        else:
            pass    
        if nom_true == "DU PONT NEUF" and ("RUE" in adresse):
            type_true = "RUE"
        elif nom_true == "DU PONT NEUF" and ("SQUARE" in adresse):
            type_true = "SQUARE"
        else:
            pass
        if nom_true == "PONT A FOURCHON":
            type_true = "RUE"
        else:
            pass
        if nom_true == "DU PONT A RAISNES":
            type_true = "RUE"
        else:
            pass
        if nom_true == "DE PONT NOYELLES":
            type_true = "RUE"
        else:
            pass
        if nom_true == "DU PONT A FOURCHON":
            type_true = "RUE"
        else:
            pass
        if nom_true == "ANDRE" and ("SAINT" in adresse):
            nom_true = "SAINT ANDRE"
        else:
            pass
        if nom_true == "ANDRE" and ("BASTION" in adresse):
            nom_true = "BASTION SAINT-ANDRE"
        else:
            pass
        if nom_true == "DES MARTYRS" and ("RESISTANCE" in adresse):
            nom_true = "DES MARTYRS DE LA RESISTANCE"
        else:
            pass
        if nom_true == "CASTEL" and ("FERME" in adresse):
            nom_true = "DE LA FERME CASTEL"
        else:
            pass
        if nom_true == "ROUBAIX" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG DE ROUBAIX"
        else:
            pass
        if nom_true == "NOTRE DAME" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG NOTRE DAME"
        else:
            pass
        if nom_true == "BETHUNE" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG DE BETHUNE"
        else:
            pass
        if nom_true == "DE DOUAI" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG DE DOUAI"
        else:
            pass
        if nom_true == "DES POSTES" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG DES POSTES"
        else:
            pass
        if nom_true == "DE ROUBAIX" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG DE ROUBAIX"
        else:
            pass
        if nom_true == "D ARRAS" and ("FAUBOURG" in adresse):
            nom_true = "DU FAUBOURG D ARRAS"
        else:
            pass
        if nom_true == "LEFEBVRE" and ("HIPPOLYTE" in adresse):
            nom_true = "HYPPOLITE LEFEBVRE"
        else:
            pass
        if nom_true == "JACQUARD" and commune_true == "LOMME":
            nom_true = "JACQUART"
        else:
            pass
        # Détection des repetitions
        if key_dico(repetition, adresse) is None:
            repet_true = ""
            pass
        else:
            repet_true = key_dico(repetition, adresse)
        if (repet_true is None) == True:
            repet_true = " "
        else:
            pass
        # mots à supprimer (identification ville, rues avec numéros...)
        if check_list(mots_a_del, adresse) != None:
            adresse = del_list(mots_a_del, adresse)
        else:
            pass
        # Détection du numéro de voie
        adresse_list = adresse.split()
        for i, elements in enumerate(adresse_list):
            num_temp = adresse_list[i]
            if (num_temp.isnumeric()) == True:
                if len(num_true) < 1:
                    num_true = num_temp
                else:
                    pass
            else:
                pass
        if num_true == '':
            num_true = 0
        adresse_true = str(num_true)+repet_true+" "+type_true+" "+nom_true
        adresse_true = " ".join(adresse_true.split())
        if 'ARGILIERE' in adresse:
            adresse_true = '2 RESIDENCE ANDRE GIDE'
        else:
            pass
    else:
        adresse_true = key_dico(courees, adresse)
        num_true = "0"
        repet_true = "0"
        type_true = "0"
        nom_true = "0"
    if commune_true == "LILLE":
        xl93 = getx(vlayerl)
        yl93 = gety(vlayerl)
        if xl93 is None and num_true != 0:
            adresse_true = str(num_true)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerl)
            yl93 = gety(vlayerl)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerl)
            yl93 = gety(vlayerl)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerl)
            yl93 = gety(vlayerl)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerl)
            yl93 = gety(vlayerl)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerl)
            yl93 = gety(vlayerl)
        else:
            pass
    else:
        pass
    if commune_true == "HELLEMMES":
        xl93 = getx(vlayerh)
        yl93 = gety(vlayerh)
        if xl93 is None and num_true != 0:
            adresse_true = str(num_true)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerh)
            yl93 = gety(vlayerh)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerh)
            yl93 = gety(vlayerh)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerh)
            yl93 = gety(vlayerh)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerh)
            yl93 = gety(vlayerh)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerh)
            yl93 = gety(vlayerh)
        else:
            pass
    else:
        pass
    if commune_true == "LOMME":
        xl93 = getx(vlayerlo)
        yl93 = gety(vlayerlo)
        if xl93 is None and num_true != 0:
            adresse_true = str(num_true)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerlo)
            yl93 = gety(vlayerlo)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerlo)
            yl93 = gety(vlayerlo)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 2
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerlo)
            yl93 = gety(vlayerlo)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) + 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerlo)
            yl93 = gety(vlayerlo)
        else:
            pass
        if xl93 is None and num_true != 0:
            num_temp = int(num_true) - 4
            adresse_true = str(num_temp)+" "+type_true+" "+nom_true
            adresse_true = " ".join(adresse_true.split())
            xl93 = getx(vlayerlo)
            yl93 = gety(vlayerlo)
        else:
            pass
    else:
        pass
    with open(export_path,'a', newline='') as exportcsv:
        export_file = csv.writer(exportcsv, delimiter = ';')
        export_file.writerow([ident, adresse_s, num_true, repet_true, type_true, nom_true, adresse_true, commune_true, xl93, yl93])


iface.messageBar().clearWidgets()
QgsProject.instance().removeMapLayer(vlayerl)
QgsProject.instance().removeMapLayer(vlayerh)
QgsProject.instance().removeMapLayer(vlayerlo)
iface.messageBar().pushMessage("Geolocalisation des adresses réussie !", level=Qgis.Success)