from consolemenu import *
from consolemenu.items import *

import lib_pyQuesto as pq # ^_^

def main():
    # Un fichier a-t-il été choisi ?
    try :
        jsonFile
    except NameError :
        jsonFile = pq.choisirFichier()

 ######################## Menu principal ########################
    # Création du menu principal
    main_menu = ConsoleMenu("pyQuesto", "Le QCM c'est du gâteau !")
 
    # Menu principal : ajout d'une entrée question ouverte
    main_menu_open = FunctionItem("Ajouter une question ouverte", pq.addQuestionSimple)
    main_menu.append_item(main_menu_open)

    # Menu principal : ajout d'une question à choix multiple
    main_menu_qcm = FunctionItem("Ajouter une question à choix multiple", pq.addQCM)
    main_menu.append_item(main_menu_qcm)

    # Menu principal : création du sous-menu pour les questions aléatoires
    submenu_alea = ConsoleMenu("Générer une question aléatoire", "Choisir la thématique")

    # Menu principal : ajout de l'option "Générer une question aléatoire" au menu principal
    submenu_alea_main_item = SubmenuItem("Générer une question aléatoire", submenu=submenu_alea)
    submenu_alea_main_item.set_menu(main_menu)
    main_menu.append_item(submenu_alea_main_item)

######################## Questions aléatoires  ########################
    # Création des sous-menus dans les questions aléatoires
    submenu_alea_conv = ConsoleMenu("Faire une conversion")
    submenu_alea_add = ConsoleMenu("Faire une addition", "Choisir une base")

    # Ajout de l'option "Faire une conversion" dans les questions aléatoires
    submenu_alea_conv_item = SubmenuItem("Faire une conversion", submenu=submenu_alea_conv)
    submenu_alea_conv_item.set_menu(submenu_alea)
    submenu_alea.append_item(submenu_alea_conv_item)

    # Ajout de l'option "Faire une addition" dans les questions aléatoires
    submenu_alea_add_item = SubmenuItem("Faire une addition", submenu=submenu_alea_add)
    submenu_alea_add_item.set_menu(submenu_alea)
    submenu_alea.append_item(submenu_alea_add_item)

    # Ajout de l'option "Faire un complément à 2" dans les questions aléatoires
    submenu_alea_comp2 = FunctionItem("Faire un complément à 2", pq.addAleaComp2)
    submenu_alea.append_item(submenu_alea_comp2)


######################## Faire une conversion  ########################
    # Ajout des entrées pour la conversion
    submenu_alea_conv_1 = FunctionItem("Décimal vers binaire", pq.addAleaConv, args=["d_b"])
    submenu_alea_conv_2 = FunctionItem("Binaire vers héxadécimal", pq.addAleaConv, args=["b_h"])
    submenu_alea_conv_3 = FunctionItem("Décimal vers octal", pq.addAleaConv, args=["d_o"])
    submenu_alea_conv.append_item(submenu_alea_conv_1)
    submenu_alea_conv.append_item(submenu_alea_conv_2)
    submenu_alea_conv.append_item(submenu_alea_conv_3)

######################## Faire une addition  ########################
    # Ajout des entrées pour les additions
    submenu_alea_add_1 = FunctionItem("Additionner en binaire sur deux octets", pq.addAleaAddi, args=["bin2"])
    submenu_alea_add_2 = FunctionItem("Additionner en héxadécimal sur deux octets", pq.addAleaAddi, args=["hexa16"])
    submenu_alea_add.append_item(submenu_alea_add_1)
    submenu_alea_add.append_item(submenu_alea_add_2)

######################## Affichage ########################
    main_menu.start()
    main_menu.join()

# Permet un import depuis l'extérieur sans exécuter le code
if __name__ == "__main__":
    main()