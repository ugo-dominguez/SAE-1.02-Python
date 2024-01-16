"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module case.py
        Ce module contient l'implémentation des cases du plateau de jeu
"""

import const



def Case(mur=False, objet=const.AUCUN, pacmans_presents=None, fantomes_presents=None):
    """Permet de créer une case du plateau

    Args:
        mur (bool, optional): un booléen indiquant si la case est un mur ou un couloir.
                Defaults to False.
        objet (str, optional): un caractère indiquant l'objet qui se trouve sur la case.
                const.AUCUN indique qu'il n'y a pas d'objet sur la case. Defaults to const.AUCUN.
        pacmans_presents (set, optional): un ensemble indiquant la liste des pacmans
                se trouvant sur la case. Defaults to None.
        fantomes_presents (set, optional): un ensemble indiquant la liste des fantomes
                se trouvant sur la case. Defaults to None.

    Returns:
        dict: un dictionnaire représentant une case du plateau
    """

    return {"mur": mur,
            "objet": objet, 
            "pacmans_presents": pacmans_presents,
            "fantomes_presents": fantomes_presents}


def est_mur(case):
    """indique si la case est un mur ou non

    Args:
        case (dict): la case considérée

    Returns:
        bool: True si la case est un mur et False sinon
    """

    return case["mur"]


def get_pacmans(case):
    """retourne l'ensemble des pacmans qui sont sur la case
    else:
        return None
        case (dict): la case considérée

    Returns:
        set: l'ensemble des identifiants de pacmans présents su la case.
    """

    return set() if case["pacmans_presents"] is None else case["pacmans_presents"]


def get_fantomes(case):
    """retourne l'ensemble des fantomes qui sont sur la case

    Args:
        case (dict): la case considérée

    Returns:
        set: l'ensemble des identifiants de fantomes présents su la case.
    """

    return set() if case["fantomes_presents"] is None else case["fantomes_presents"]


def get_nb_pacmans(case):
    """retourne le nombre de pacmans présents sur la case

    Args:
        case (dict): la case considérée

    Returns:
        int: le nombre de pacmans présents sur la case.
    """

    return 0 if case["pacmans_presents"] is None else len(case["pacmans_presents"])


def get_nb_fantomes(case):
    """retourne le nombre de fantomes présents sur la case

    Args:
        case (dict): la case considérée

    Returns:
        int: le nombre de fantomes présents sur la case.
    """

    return 0 if case["fantomes_presents"] is None else len(case["fantomes_presents"])


def get_objet(case):
    """retourne l'objet qui est sur la case.
        Si aucun objet ne s'y trouve la fonction retourne const.AUCUN

    Args:
        case (dict): la case considérée
    """

    return case["objet"]


def poser_objet(case, objet):
    """Pose un objet sur la case. Si un objet était déjà présent ce dernier disparait.
        Si la case est un mur, l'objet n'est pas mis dans la case.

    Args:
        case (dict): la case considérée
        objet (str): identifiant d'objet. const.AUCUN indiquant que plus aucun objet se
                trouve sur la case.
    """

    if not est_mur(case):
        case["objet"] = objet


def prendre_objet(case):
    """Enlève l'objet qui se trouve sur la case et retourne l'identifiant de cet objet.
        Si aucun objet se trouve sur la case la fonction retourne const.AUCUN.

    Args:
        case (dict): la case considérée

    Returns:
        char: l'identifiant de l'objet qui se trouve sur la case.
    """

    objet_pris = case["objet"]
    case["objet"] = const.AUCUN

    return objet_pris
    

def poser_pacman(case, pacman):
    """Pose un nouveau pacman sur la case.
    Si le pacman était déjà sur la case la fonction ne fait rien
    Si la case est un mur, le pacman est quand-même posé (pouvoir de passe-muraille)

    Args:
        case (dict): la case considérée
        pacman (str): identifiant du pacman à ajouter sur la case
    """

    pacmans_set = get_pacmans(case)
    pacmans_set.add(pacman)

    case["pacmans_presents"] = pacmans_set


def prendre_pacman(case, pacman):
    """Enlève le pacman dont l'identifiant est passé en paramètre de la case.
        La fonction retourne True si le joueur était bien sur la case et False sinon.

    Args:
        case (dict): la case considérée
        pacman (str): l'identifiant du pacman à enlever

    Returns:
        bool: True si le joueur était bien sur la case et False sinon.
    """

    pacmans_set = get_pacmans(case)

    if pacmans_set is None:
        pacmans_set = set()
        return False
    
    if pacman in pacmans_set:
        pacmans_set.remove(pacman)
        return True


def poser_fantome(case, fantome):
    """Pose un nouveau fantome sur la case
        si le fantome était déjà sur la case, la fonction ne fait rien
        si la case est un mur la fonction ne fait rien

    Args:
        case (dict): la case considérée
        fantome (str): identifiant du fantome à ajouter sur la case
    """

    fantomes_set = get_fantomes(case)

    if fantomes_set is None:
        fantomes_set = set()

    if not est_mur(case):
        fantomes_set.add(fantome)

    case["fantomes_presents"] = fantomes_set


def prendre_fantome(case, fantome):
    """Enlève le fantome dont l'identifiant est passé en paramètre de la case.
        La fonction retourne True si le fantome était bien sur la case et False sinon.

    Args:
        case (dict): la case considérée
        fantome (str): l'identifiant du fantome à enlever

    Returns:
        bool: True si le fantome était bien sur la case et False sinon.
    """

    fantomes_set = get_fantomes(case)

    if fantomes_set is None:
        fantomes_set = set()
        return False
    
    if fantome in fantomes_set:
        fantomes_set.remove(fantome)
        return True
