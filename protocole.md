###### PROTOCOLE ######
Ici sera décrit en langage naturel (plus ou moins...) les differents protocoles de communication
#######################
##### Raspberry #####
On utilise un JSON pour savoir quel arret "implementer" dans le script. Le json est de la forme suivante:

```
[
    {
        "name": "Liberte", //exemple
        "time2Go": 120,    //exemple
        "route": [
            {
                "name": "A",
                "dest": [
                    {
                        "name": "porte de plouzane",
                        "id": 0
                    },
                    {
                        "name": "porte de gouesnou",
                        "id": 1
                    },
                    {
                        "name": "porte de guipavas",
                        "id": 2
                    }
                ]
            }
        ]
    }
]
```

####################
En bon français : keskonva fer?
-la raspi récupère dans le Json :
    *Nombre de Station
    *l'ID de chaque arrêt
    *Le temps qu'on met pour aller à chaque station

Toutes les minutes :
    -La raspi :
        *récupère via l'API le temps restant avant le passage des deux bus suivant pour chaque destination du panneau
        *"temps de passage - temps pour rejoindre" pour chaque temps
            -Si le temps obtenu est inférieur à 0min ET que le temps du bus suivant est inférieur à 5min : ignore le bus 1 et traite les données du bus 2
            -Si le temps de passage x (j'ai bien dit temps de passage, et pas temps obtenu!) est inférieur à 1min, programmer un refresh au bout x secondes
        *la raspi map les temps sur un octet (600s => 0s; 254=>0)
        *la raspi envoit les résultats dans l'ordre des ID à l'arduino

    - l'arduino:
        * stocke les valeurs dans un tableau
        * calcule dans un autre tableau la correspondance en couleur:
            -255 : bleu = 255
            -entre 254 et 127 : bleu map(254=> 127; 255 => 0) || vert map(254=>127; 0=>255)
            -entre 127 et 0 : vert map(127=>0; 255=>0) || rouge map(127=>0; 0=>255)
        * toutes les map(600=>0; 255=>0) secondes, val_couleur-1 SAUF si tmp = 255

Rpi -> Arduino : 
1 *  x: nbr de destinations/directions/leds/(mettre ici ce qui passe)
x *  temps échelonnée entre 0 et 255
