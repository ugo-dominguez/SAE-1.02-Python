# SAE-1.02-Python

### Exemple de plateau
```python
{
'nb_lignes': 20,
'nb_colonnes': 30, 
'nb_joueurs': 5, 
'nb_fantomes': 5, 
'cases': [
          [{'mur': True, 'objet': ' ', 'pacmans_presents': None, 'fantomes_presents': None}, {'mur': True, 'objet': ' ', 'pacmans_presents': None, 'fantomes_presents': {'d', 'a'}}],
          [{'mur': True, 'objet': ' ', 'pacmans_presents': None, 'fantomes_presents': None}, {'mur': True, 'objet': ' ', 'pacmans_presents': None, 'fantomes_presents': {'c'}}],
          ]
'joueurs': {'A': (1, 2), 'B': (1, 22), 'C': (3, 6), 'D': (10, 21), 'E': (16, 1)},
'fantomes': {'a': (7, 5), 'b': (10, 1), 'c': (10, 12), 'd': (7, 5), 'e': (3, 6)}
}
```

### Exemple de plateau
```python
{
'mur': False,
'objet': '&',
'pacmans_presents': {'A','B'},
'fantomes_presents': {'a','b','c'}
}
```
