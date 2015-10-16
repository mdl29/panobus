###### PROTOCOLE ######
Ici sera décrit en langage naturel (plus ou moins...) les differents protocoles de communication 
#######################
##### Raspberry #####
On utilise un JSON pour savoir quel arret "implementer" dans le script. Le json est de la forme suivante:
[   
  {
    "name": Nom de l'arret,
    "route":[
        {"name":Chiffre ou lettre de la ligne,
        "dest": [
            Destionation 1,
            Destionation 2,
            Destionation 3
            ]
        },
        {"name":Chiffre ou lettre de la ligne",
        "dest": [
            Destionation 1,
            Destionation 2
        ]                
        }
    ]
  }
]
