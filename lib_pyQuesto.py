# Parce qu'on aime les trucs déjà faits
import random
import json 
import re

###############################
#### Fonctions générales ######
###############################

### Ajouter une question dans le fichier json
def addToJson(nouvelle_entree):
    # Ouverture et sérialisation du fichier json
    with open('test.json', 'r') as jsonfile:
        mondict = json.load(jsonfile)
    #Ajout de la nouvelle entrée
    mondict["questionnaire"]["questions"].append(nouvelle_entree)
    # Retour en format json
    monjson = json.dumps(mondict, indent=2)
    # On écrase l'ancien fihcier json
    with open('test.json', 'w') as jsonfile:
        jsonfile.write(monjson)
    # On affiche un message de confirmation
    retour = input("Question bien ajoutée !\nAppuyer sur entrée pour revenir au menu")

# Mettre des zéros au début d'un mot binaire afin de compléter des octets par exemple
def completeWithZeros(mot, taillepqt,nbpaquets) :
    nb0 = taillepqt * int(nbpaquets) - len(mot)
    bin0 = "0"*nb0 + str(mot)
    return bin0

# Formater les mots binaires ou hexadécimaux avec des espaces : 11010101 devient 1101 0111 par exemple
def addSpaces(mot, paquet) :
    mot_formate = ""
    i=0
    for j in mot :
        if(i==paquet) :
            mot_formate += " "
            i = 0
        mot_formate += j
        i += 1
    return mot_formate

###############################
####### Question ouverte ######
###############################
def addQuestionSimple():
    # On évite des questions vides
    question, reponse = "", ""
    while question == "" :
        question = input("Saisissez la question : ")
    while reponse == "" :
        reponse = input("Saisissez la réponse : ")
    # Formatage des données
    nouvelle_question = {
        "intitule" : question,
        "type_question" : 0,
        "reponses" : {
            "ponderation" : 100,
            "feedback" : reponse,
            "contenu_reponse" : reponse
        }
    }
    # On rajoute au json
    addToJson(nouvelle_question)

###############################        
# Question à  choix multiples #
###############################
def addQCM():
    # On évite une question vide
    question = ""
    while question == "" :
        question = input("Saisissez la question : ")
    # On part du postulat qu'un QCM exige au moins deux réponses :D
    reponses_saisies = []
    for i in range(2) :
       reponses_saisies.append(addQCMReponse())
    
    # On ajoute éventuellemnt d'autres réponses en contrôlant qu'il y a au moins une réponse juste :
    arreter = False         # Pour sortir du while une fois que les réponses sont saisies
    cpt_true = 0            # Compteur de réponses justes
    while(not arreter):
        # On demande si on souhaite ajouter une réponse supplémentaire
        continuer = ""
        while(not re.match("^[onON]{1}$",continuer)) :
            continuer = input("Ajouter une autre réponse ? [O/N] ")
        # Si l'utilisateur répond non n OU N on vérifie qu'il existe au moins une bonne réponse parmi celles saisies
        if(re.search("^[nN]{1}$", continuer)) :
            # On parcourt les réponses
            for j in range(len(reponses_saisies)) :
                # Si une réponse est vraie on la compte
                if reponses_saisies[j]["bonne_reponse"] == True :
                    cpt_true += 1
            # On arrête si au moins une réponse
            if(cpt_true > 0) :
                arreter = True
            # Sinon on affiche un message et on retourne au début du while
            else :
                print("Vous n'avez aucune réponse valide !\n")
        else :
            reponses_saisies.append(addQCMReponse())

    # Calcul de la ponderation répartie sur toutes les réponses justes
    ponde = round(100 / cpt_true)
    # On repasse pour insérer la pondération
    for j in range(len(reponses_saisies)) :
        if  reponses_saisies[j]["bonne_reponse"] == True :
            reponses_saisies[j]["ponderation"] = ponde
        else :
            reponses_saisies[j]["ponderation"] = 0

    # Formatage de la nouvelle question
    nouvelle_question = {
        "intitule" : question,
        "type_question" : 1,
        "reponses" : reponses_saisies
        }
    addToJson(nouvelle_question)
# Ajouter une réponse au QCM
def addQCMReponse():
    # On évite une saisie vide
    saisie_reponse = ""
    while saisie_reponse == "" :
        saisie_reponse = input("Saisissez une réponse : ")
    # On demande si c'est la bonne réponse
    bonne_reponse = ""
    while(not re.match("^[onON]{1}$",bonne_reponse)) :
        bonne_reponse = input("S'agit-il de la bonne réponse ? [O/N] ")
    # Si c'est une réponse négative  on propose de faire un commentaire
    # avec reformatage de bonne_reponse en booléen
    feedback = ""
    if(re.search("^[nN]{1}$", bonne_reponse)) :
        feedback = input("Saisir un commentaire pour cette mauvaise réponse (peut-être laissé vide)\n",)
        bonne_reponse = False
    else:
        bonne_reponse = True
    # On renvoie le dictionnaire
    return {
        "bonne_reponse" : bonne_reponse,
        "feedback" : feedback,
        "contenu_reponse" : saisie_reponse
    }

###############################
##### Questions aléatoires ####
############################### 
def addAleaConv(choix):
    ### Conversion Décimal vers binaire
    if choix == "d_b" :
        # On récupère le nombre d'octets
        octets = ""
        while not re.search("^[0-9]{1,}$", octets) :
            octets = input("Indiquer le nombre d'octets attendus pour la réponse (1 minium) : ")
        # On génère un nombre aléatoire >= 128, en-dessous c'est trop facile !
        val_decimal = random.randint(128,(2**(8*int(octets))-1))
        # On transtype en binaire
        val_binaire = format(val_decimal, "b")
        # On rajoute des 0 au début pour faire des octets complets
        val_binaire = completeWithZeros(str(val_binaire), 8, octets)
        # On rajoute des espaces pour séparer les octets
        val_bin_format = addSpaces(val_binaire, 8)
        # Formatage des données
        nouvelle_question = {
            "intitule" : "Convertir le nombre décimal "+ str(val_decimal) +" en binaire sur "+ octets +" octets (mettre un espace pour séparer chaque octet).",
            "type_question" : 2,
            "nature" : choix,
            "reponses" : {
                "ponderation" : 100,
                "feedback" : val_bin_format,
                "contenu_reponse" : val_bin_format
            }
        }
        # On nourrit le json
        addToJson(nouvelle_question)
    ### Conversion Binaire vers Hexadécimal
    elif choix == "b_h" :
        # On récupère le nombre d'octets
        octets = ""
        while not re.search("^[0-9]{1,}$", octets) :
            octets = input("Indiquer le nombre d'octets à générer (1 minium) : ")
        # On génère un nombre aléatoire >= 128, en-dessous c'est trop facile !
        val_decimal = random.randint(128,(2**(8*int(octets))-1))
        # On transtype en binaire
        val_binaire = format(val_decimal, "b")
        # On transtype en hexadécimal
        val_hexa = format(val_decimal, "X")
        # On rajoute des 0 au début pour faire des octets complets
        val_binaire = completeWithZeros(str(val_binaire), 8, octets)
        # On rajoute des espaces pour séparer les octets
        val_bin_format = addSpaces(val_binaire, 8)
        # On rajoute des espaces pour séparer les octets en hexa
        val_hexa_format = addSpaces(val_hexa, 2)

        # Formatage des données
        nouvelle_question = {
            "intitule" : "Convertir le nombre binaire "+ str(val_bin_format) +" en hexadécimal (mettre un espace pour séparer chaque octet).",
            "type_question" : 2,
            "nature" : choix,
            "reponses" : {
                "ponderation" : 100,
                "feedback" : val_hexa_format,
                "contenu_reponse" : val_hexa_format
            }
        }    
        # On nourrit le json
        addToJson(nouvelle_question)
    ### Conversion décimal vers octal
    elif choix == "d_o" :
        # On génère un nombre aléatoire >= 64, en-dessous c'est trop facile et <= 1000 !
        val_decimal = random.randint(64,1000)
        # On transtype en octal
        val_octal = format(val_decimal, "o")
        # Formatage des données
        nouvelle_question = {
            "intitule" : "Convertir le nombre décimal "+ str(val_decimal) +" en octal.",
            "type_question" : 2,
            "nature" : choix,
            "reponses" : {
                "ponderation" : 100,
                "feedback" : val_octal,
                "contenu_reponse" : val_octal
            }
        }
        # On nourrit le json
        addToJson(nouvelle_question)
    else :
        retour = input("Vous ne devriez pas être là :)\nAppuyer sur entrée pour revenir au menu")


# Ajoute une question aléatoire d'addition
# Addition de deux mots binaires sur deux octets
def addAleaAddi(choix) :
    if choix == "bin2" :
        mot1 = random.randint(0,40000)  # Le choix des limites permet de ne pas dépasser 65535=2^16-1
        mot2 = random.randint(255,25535)
        resultat = mot1 + mot2
        # On transtype tout le monde et on ajoute les zéros et les espaces
        mot1 = format(mot1, "b")
        mot1 = completeWithZeros(mot1, 8, 2)
        mot1 = addSpaces(mot1, 8)
        mot2 = format(mot2, "b")
        mot2 = completeWithZeros(mot2, 8, 2)
        mot2 = addSpaces(mot2, 8)
        resultat = format(resultat, "b")
        resultat = completeWithZeros(resultat, 8, 2)
        resultat = addSpaces(resultat, 8)
        # Formatage de la question pour le json
        nouvelle_question = {
            "intitule" : "Additionner les deux mots binaires suivants en n'oubliant pas l'espace !\n "+mot1+"\n+"+mot2+"\n",
            "type_question" : 2,
            "nature" : choix,
            "reponses" : {
                "ponderation" : 100,
                "feedback" : resultat,
                "contenu_reponse" : resultat
            }
        }
        # On nourrit le json
        addToJson(nouvelle_question)
    elif choix == "hexa16" :
        mot1 = random.randint(0,40000)  # Le choix des limites permet de ne pas dépasser 65535=2^16-1
        mot2 = random.randint(255,25535)
        resultat = mot1 + mot2
        # On transtype tout le monde et on ajoute les zéros et les espaces
        mot1 = format(mot1, "X")
        mot1 = completeWithZeros(mot1, 2, 2)
        mot1 = addSpaces(mot1, 2)
        mot2 = format(mot2, "X")
        mot2 = completeWithZeros(mot2, 2, 2)
        mot2 = addSpaces(mot2, 2)
        resultat = format(resultat, "X")
        resultat = completeWithZeros(resultat, 2, 2)
        resultat = addSpaces(resultat, 2)
        # Formatage de la question pour le json
        nouvelle_question = {
            "intitule" : "Additionner les deux mots héxadécimaux suivants en n'oubliant pas les espace !\n "+mot1+"\n+"+mot2+"\n",
            "type_question" : 2,
            "nature" : choix,
            "reponses" : {
                "ponderation" : 100,
                "feedback" : resultat,
                "contenu_reponse" : resultat
            }
        }
        # On nourrit le json
        addToJson(nouvelle_question)
    else :
        retour = input("Vous ne devriez pas être là :)\nAppuyer sur entrée pour revenir au menu")

## Complément à 2
def addAleaComp2() :
    # On récupère le nombre de bits en vérifiant qu'il s'agit d'un chiffre supérieur à 0
    nbbits = ""
    while nbbits != "0" and not re.search("^[0-9]{1,}$",nbbits) :
        nbbits = input("Nombre de bits (MSB compris) : ")
    # On passe en entier
    nbbits = int(nbbits)
    # On générère un entier strcitement négatif dans la limite d nombre de bits définis
    val_decimal = random.randint(-2**(nbbits-1),-1)
    # Python ne gérant les mots binaires pour faire un complément à deux académiques,
    # on bricole en ajoutant la valeur maximale positive sur nbbits-1 (car on enlève 1 bit pour le signe).
    # # Par exemple sur 4 bits la valeur -5 sera calculée ainsi :
    # -5 + 2^(4-1) = 3 --> En binaire 011 puis on signe en négatif : 1_011
    # On a bien (-5)d = (1011)b
    val_binaire = val_decimal + 2**(nbbits-1)
    val_binaire = format(val_binaire, "b")
    val_binaire = "1" + completeWithZeros(val_binaire, nbbits-1, 1)
    # Formatage de la question pour le json
    nouvelle_question = {
        "intitule" : "Convertir la valeur décimale suivante en un mot binaire signé sur "+ str(nbbits) +" bits : "+ str(val_decimal),
        "type_question" : 2,
        "nature" : "comp2",
        "reponses" : {
            "ponderation" : 100,
            "feedback" : val_binaire,
            "contenu_reponse" : val_binaire
        }
    }
    # On nourrit le json
    addToJson(nouvelle_question)