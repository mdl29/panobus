###### PROTOCOLE ######
Voici l'amgorythme utilisé pour le panobus
#######################
##### Json #####
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
##### Code #####
* la raspi récupère dans le Json :

    * Nombre de Station
    * l'ID de chaque arrêt
    * Le temps qu'on met pour aller à chaque station

* Toutes les n secondes la raspberryPy:

        * récupère via l'API le temps restant avant le passage des deux bus suivant pour chaque destination du panneau
        * calcule : "temps de passage - temps pour rejoindre" pour chaque temps
        => Si le temps obtenu est inférieur à 0min ET que le temps du bus suivant est inférieur au temps nécessaire pour rejoindre l'arrêt : ignore le bus qui arrive et traite les données du bus suivant
        * actualise la couleur des leds en fonction du résultat obtenu
