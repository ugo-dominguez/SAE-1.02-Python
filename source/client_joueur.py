# coding: utf-8
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module client_joueur.py
        Ce module contient le programme principal d'un joueur
        il s'occupe des communications avec le serveur
            - envois des ordres
            - recupération de l'état du jeu
        la fonction mon_IA est celle qui contient la stratégie de
        jeu du joueur.

"""
import argparse
import random
import client
import const
import plateau as p
import joueur as j
import case as c

prec='X'

def mon_IA(ma_couleur, carac_jeu, plan, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                   de la partie séparées par des ;
             duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet           
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;nb_cases_peintes;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """

    # decodage des informations provenant du serveur
    joueurs = {}

    for ligne in les_joueurs.split('\n'):
        lejoueur = j.joueur_from_str(ligne)
        joueurs[j.get_couleur(lejoueur)] = lejoueur

    le_plateau = p.Plateau(plan)


    # IA Tom

    def get_analyse(pos, skip=None):
        """retourne les différentes analyses en fonction des directions possibles

        Args:
            pos (tuple): une paire (lig,col) d'int
            skip (dict, optional): un objet, fantome ou joueur à ne pas prendre en compte dans l'analyse. Defaults to None.

        Returns:
            dict: un dictionnaire de directions, contenant des analyses
        """

        directions = p.directions_possibles(le_plateau, pos, const.PASSEMURAILLE in j.get_objets(joueurs[ma_couleur]))
        distance = p.get_nb_lignes(le_plateau) + p.get_nb_colonnes(le_plateau)
        res = dict()

        for card in directions:
            analyse = p.analyse_plateau(le_plateau, pos, card, distance, skip)

            if analyse is not None:
                res[card] = analyse
            
        return res


    def get_direction(analyse, entity, func=min):
        """retourne une direction choisie

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses
            entity (str): une entité
            func (callable, optional): une fonction à appliquer sur les analyses. Defaults to min.

        Returns:
            str: la direction choisie
        """

        return func(analyse, key = lambda d: analyse[d][entity]) if len(analyse) > 0 else random.choice(const.DIRECTIONS)
    

    def suivre_fantomes(analyse):
        """permet au pacman de suivre des fantomes en prenant le plus court chemin

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            str: la direction choisie
        """

        return get_direction(analyse, 'fantomes')


    def cherche_objets(analyse):
        """permet au pacman d'aller vers des objets en prenant le plus court chemin

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            str: la direction choisie
        """

        return get_direction(analyse, 'objets')
    

    def a_glouton(player):
        """permet de savoir si un joueur a un glouton

        Args:
            player (dict): un dictionnaire représentant un joueur

        Returns:
            bool: un booléen indiquant si un joueur a un glouton
        """

        return const.GLOUTON in j.get_objets(player) and j.get_duree(player, const.GLOUTON) > 5
    
    
    def tp_si_danger(analyse):
        """retourne un direction vers un mur, pour que le joueur se téléporte si des fantomes sont trop proches

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            str: la direction choisie
        """

        res, tp = const.DIRECTIONS, False

        for d in analyse:
            res = res.replace(d, '')
            for fantome in analyse[d]['fantomes']:
                if fantome[0] <= 5:
                    tp = True

        return res[0] if len(res) > 0 and tp else None


    def ia_pacman():
        """l'ia du pacman

        Returns:
            str: la direction choisie
        """

        pos_pacman = j.get_pos_pacman(joueurs[ma_couleur])
        analyse = get_analyse(pos_pacman, ma_couleur.lower())

        if a_glouton(joueurs[ma_couleur]):
            return suivre_fantomes(analyse)
        
        en_danger = tp_si_danger(analyse)
        return cherche_objets(analyse) if en_danger is None else en_danger


    def fuir(analyse):
        """permet au fantome de fuir les pacmans

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            str: la direction choisie
        """

        return get_direction(analyse, 'pacmans', max)


    def poursuivre(analyse):
        """permet au fantome de poursuivre les pacmans en prenant le plus court chemin

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            str: la direction choisie
        """

        return get_direction(analyse, 'pacmans')
    

    def pacmans_proximite(analyse):
        """retourne les pacmans présent à moins de 6 cases du fantome

        Args:
            analyse (dict): un dictionnaire de directions, contenant des analyses

        Returns:
            set: l'ensemble des pacmans présent à moins de 6 cases du fantome
        """

        res = set()

        for d in analyse:
            for pacman in analyse[d]["pacmans"]:
                if pacman[0] <= 5:
                    res.add(pacman[1])

        return res


    def ia_fantome():
        """l'ia du fantome

        Returns:
            str: la direction choisie
        """

        pos_fantome = j.get_pos_fantome(joueurs[ma_couleur])
        analyse = get_analyse(pos_fantome, ma_couleur)

        for couleur in pacmans_proximite(analyse):
            if a_glouton(joueurs[couleur]):
                return fuir(analyse)

        return poursuivre(analyse)
    
    
    # Directions choisies
    dir_p = ia_pacman()
    dir_f = ia_fantome()

    return dir_p + dir_f


if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            carac_jeu,le_plateau,les_joueurs=le_jeu.split("--------------------\n")   
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")
