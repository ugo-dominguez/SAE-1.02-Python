def fabrique_le_calque(le_plateau, position_depart):
    """fabrique le calque d'un labyrinthe en utilisation le principe de l'inondation :
       
    Args:
        le_plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        matrice: une matrice qui a la taille du plateau dont la case qui se trouve à la
       position_de_depart est à 0 les autres cases contiennent la longueur du
       plus court chemin pour y arriver (les murs et les cases innaccessibles sont à None)
    """

    calque = matrice.new_matrice(matrice.get_nb_lignes(le_plateau), matrice.get_nb_colonnes(le_plateau), None)
    matrice.set_val(calque, *position_depart, 0)
    cases = voisins(le_plateau, position_depart)
    cpt = 0

    while cases:
        cpt += 1
        for voisin in cases.copy():
            if matrice.get_val(calque, *voisin) is None:
                matrice.set_val(calque, *voisin, cpt)
                cases |= voisins(le_plateau, voisin)

            cases.remove(voisin)

    return calque