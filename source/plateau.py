"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""

import const
import case
import random


def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """

    return plateau['nb_lignes']


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """

    return plateau['nb_colonnes']


def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position

    Returns:
        int: un tuple d'entiers
    """

    west_pos = pos[1] - 1
    if west_pos < 0:
        west_pos = get_nb_colonnes(plateau) - 1
        
    return pos[0], west_pos


def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position

    Returns:
        int: un tuple d'entiers
    """

    east_pos = pos[1] + 1
    if east_pos >= get_nb_colonnes(plateau):
        east_pos = 0

    return pos[0], east_pos

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position

    Returns:
        int: un tuple d'entiers
    """

    north_pos = pos[0] - 1
    if north_pos < 0:
        north_pos = get_nb_lignes(plateau) - 1

    return north_pos, pos[1]


def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position

    Returns:
        int: un tuple d'entiers
    """

    south_pos = pos[0] + 1
    if south_pos >= get_nb_lignes(plateau):
        south_pos = 0

    return south_pos, pos[1]


def pos_arrivee(plateau, pos, direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """

    next_pos = None

    if direction == 'O':
        next_pos = pos_ouest(plateau, pos)

    elif direction == 'E':
        next_pos = pos_est(plateau, pos)

    elif direction == 'N':
        next_pos = pos_nord(plateau, pos)

    elif direction == 'S':
        next_pos = pos_sud(plateau, pos)

    return next_pos


def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """

    return plateau['cases'][pos[0]][pos[1]]


def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """

    return case.get_objet(get_case(plateau, pos))


def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """

    case.poser_pacman(get_case(plateau, pos), pacman)


def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """

    case.poser_fantome(get_case(plateau, pos), fantome)


def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """

    case.poser_objet(get_case(plateau, pos), objet)


def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir non peint)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """

    # Crée un tuple contenant les informations du plan
    list_plateau = plan.split('\n')
    for i in range(len(list_plateau)):
        if ';' in list_plateau[i]:
            list_plateau[i] = list_plateau[i].split(';')
    list_plateau = tuple(list_plateau)


    # Permet d'obtenir un dictionnaire contenant les positions d'entités, comme les joueurs ou les fantomes
    def positions(nb_entite, ind_entite):
        """Créer un dictionnaire contenant les noms des entités en clé, et leurs positions en valeurs

        Args:1000//
            nb_entite (int): le nombre d'entité à prendre en compte
            ind_entite (int): l'indice de début d'informations des entités

        Returns:
            dict: un dictionnaire contenant les noms des entités en clé, et leurs positions en valeurs
        """

        dico = {}
        for i in range(ind_entite, ind_entite + nb_entite, 1):
            dico[list_plateau[i][0]] = int(list_plateau[i][1]), int(list_plateau[i][2])
        
        return dico
    
    
    # Calculs simples des informations
    nb_lignes, nb_colonnes = int(list_plateau[0][0]), int(list_plateau[0][1])
    nb_joueurs = int(list_plateau[nb_lignes + 1])
    nb_fantomes = int(list_plateau[nb_lignes + nb_joueurs + 2])
    joueurs = positions(nb_joueurs, nb_lignes + 2)
    fantomes = positions(nb_fantomes, nb_lignes + nb_joueurs + 3)
    cases = []


    # Création de la matrice contenant les cases du plateau
    for y in range(nb_lignes):
        cases.append([])

        for elt in list_plateau[y + 1]:
            if elt == const.AUCUN:
                cases[y].append(case.Case())

            elif elt in const.LES_OBJETS:
                cases[y].append(case.Case(objet=elt))

            else:
                cases[y].append(case.Case(mur=True))


    # Création du dictionnaire représentant un plateau
    res = {'nb_lignes': nb_lignes,
            'nb_colonnes': nb_colonnes,
            'nb_joueurs': nb_joueurs,
            'nb_fantomes': nb_fantomes,
            'cases': cases,
            'joueurs': joueurs,
            'fantomes': fantomes}


    # Ajout des entités dans les cases du plateau.
    for pacman in joueurs:
        poser_pacman(res, pacman, joueurs[pacman])

    for fantom in fantomes:
        poser_fantome(res, fantom, fantomes[fantom])


    return res


def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """

    plateau['cases'][pos[0]][pos[1]] = une_case


def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """

    return case.prendre_pacman(get_case(plateau, pos), pacman)


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """

    return case.prendre_fantome(get_case(plateau, pos), fantome)


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """

    return case.prendre_objet(get_case(plateau, pos))

        
def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """

    if pacman not in plateau["joueurs"] or plateau["joueurs"][pacman] != pos:
        return
    
    next_pos = pos_arrivee(plateau, pos, direction)
    if next_pos is None:
        return

    if passemuraille or not case.est_mur(get_case(plateau, next_pos)):
        enlever_pacman(plateau, pacman, pos)
        poser_pacman(plateau, pacman, next_pos)
        plateau['joueurs'][pacman] = next_pos
        return next_pos


def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """

    if fantome not in plateau["fantomes"]:
        return
    
    next_pos = pos_arrivee(plateau, pos, direction)
    if next_pos is None:
        return

    if not case.est_mur(get_case(plateau, next_pos)):
        enlever_fantome(plateau, fantome, pos)
        poser_fantome(plateau, fantome, next_pos)
        plateau['fantomes'][fantome] = next_pos
        return next_pos
    

def case_vide(plateau):
    """choisi aléatoirement sur le plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    
    get_random_pos = lambda: random.randint(0, get_nb_lignes(plateau) - 1), random.randint(0, get_nb_colonnes(plateau) - 1)
    pos, case_choisie = get_random_pos(), get_case(plateau, pos)
    
    while case.est_mur(case_choisie) or case.get_objet(case_choisie) != const.AUCUN or case.get_pacmans(case_choisie) or case.get_fantomes(case_choisie):
        pos, case_choisie = get_random_pos(), get_case(plateau, pos)

    return pos


def directions_possibles(plateau, pos, passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """

    directions = ""
    for direction in const.DIRECTIONS:
        next_pos = pos_arrivee(plateau, pos, direction)
        next_case = get_case(plateau, next_pos)

        if not case.est_mur(next_case) or passemuraille:
            directions += direction

    return directions


def analyse_plateau(plateau, pos, direction, distance_max, skip=None):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distanceschoix["joueur"][0]
        distance_max (int): un entier indiquant la distance limite de la recherche

    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 

    def add_case_in_res(res, pos, distance):
        """_summary_

        Args:
            plateau (dict)): Le plateau considéré
            res (dict): un dictionnaire de listes
            pos (tuple): une paire (lig,col) d'int
            distance (int): une distance
        """

        case_actuelle = get_case(plateau, pos)
        objet = case.get_objet(case_actuelle)

        if objet != skip and objet in const.LES_OBJETS:
            res["objets"].append((distance, objet))
            
        res["pacmans"] += [(distance, pacman) for pacman in case.get_pacmans(case_actuelle) if skip != pacman]
        res["fantomes"] += [(distance, fantome) for fantome in case.get_fantomes(case_actuelle) if skip != fantome]

    
    next_pos = pos_arrivee(plateau, pos, direction)
    if case.est_mur(get_case(plateau, next_pos)):
        return 

    res = {'objets': [], 
           'pacmans': [], 
           'fantomes': []}
    
    parcourues, next_cases = set(), [(next_pos, 1)]

    while next_cases:
        case_actuelle = min(next_cases, key = lambda cas: cas[1])

        if case_actuelle[1] > distance_max:
            return res
        
        add_case_in_res(res, case_actuelle[0], case_actuelle[1])
        parcourues.add(case_actuelle[0])

        for direction in directions_possibles(plateau, case_actuelle[0]):
            next_pos = pos_arrivee(plateau, case_actuelle[0], direction)
            if next_pos not in parcourues:
                next_cases.append((next_pos, case_actuelle[1] + 1))
        
        next_cases.remove(case_actuelle)

    return res


def prochaine_intersection(plateau, pos, direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """

    distance = 0
    next_pos = pos_arrivee(plateau, pos, direction)

    while not len(directions_possibles(plateau, next_pos)) > 2:
        distance += 1
        next_pos = pos_arrivee(plateau, next_pos, direction)

        if next_pos == pos:
            return -1

    return distance


# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res
