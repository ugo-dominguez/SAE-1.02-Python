import plateau as P
import case
import const
#Partie Pacman
def Echappatoir(plateau, pos):
    """Permet de s'échapper s'il y a des fantomes dans toutes les directions à 5 cases ou moins.

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) d'int
    
    Return : un tuple, d'un booléen qui dit si le joueur doit partir et une direction. Si le booléen est faux alors la direction est None
    """
    # Pour améliorer il faudrait une fonction qui prend le calque et qui regarde les 5 cases autours de la position (mieux que de regarder pour chaque direction)
    escape = False
    for direc in 'NESO':
        cpt = 0
        need_escape = [False,False,False,False]
        # False signifie que je ne suis pas bloquer et que je peux me 
        # déplacer dans au moins une direction qui à + de 5 cases sans recontrer de fantomes
        analyse = P.analyse_plateau(plateau, pos, direc, P.distance_max(plateau, pos, direc))
        # Prend une analyse du plateau pour chaque directions autour du joueur
        for dist,ident in analyse['fantomes']:
            if direc in P.directions_possibles(plateau, pos, passemuraille=False):
                if dist <= 5 :
                    need_escape[cpt]=True
                    # Si je suis à 5 cases ou moins d'un fantome je suis bloqué, donc True
            else:
                bug_mur = direc
                need_escape[cpt]=True
                # Sinon c'est que je suis bloqué par un mur donc je suis bloqué
        if need_escape == [True,True,True,True]:
            escape = True
        else:
            return(escape, None)
        cpt += 1
    return(escape, bug_mur)



def meilleur_chemin(plateau, pos):
    """Prend le chemin qui rapporte le plus de 

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) d'int
        
    Returns:
        direc : Renvoi la direction qui donne le plus de points
    """
    res = None
    maximum = 0
    # max de somme direction
    for direc in 'NESO':
        somme_direction = 0
        # On regarde toutes les directions et on initialise la somme de la direction à 0
        
        chemin = P.analyse_plateau(plateau,pos,direc,P.distance_max(plateau,pos,direc))
        if chemin != None:
            somme_direction -= len(chemin['fantomes'])*20
            # On enlève 20 points pour chaque fantome dans la ligne ( On peut faire mieux en retirant le reste de la ligne s'il y a un fantome )
            
            somme_direction -= len(chemin['pacmans'])*50
            # On enlève 50 points par joueur présent dans le couloir
            
            for position in chemin['objets'][0]:
                obj = case.get_objet(P.get_case(plateau,position))
                if obj != const.AUCUN:
                    somme_direction += const.PROP_OBJET[obj][0]
                    # Pour chaque position du couloir, on regarde l'objet et on ajoute la valeur à somme direction
                    
        if somme_direction > maximum:
            somme_direction = maximum
            res = direc
            # On vérifie que la somme du couloir est plus petite ou plus grande que celles précédemment vues
    return res