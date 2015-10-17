###### PROTOCOLE ######
Ici sera décrit en langage naturel (plus ou moins...) les differents protocoles de communication
#######################
##### Raspberry #####
On utilise un JSON pour savoir quel arret "implementer" dans le script. Le json est de la forme suivante:
<pre><code>
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
</code></pre>

####################
En bon français : keskonva fer?
-la raspi récupère dans le Json :
    *Nombre de Station
    *Nom de chaque Station
    *Nom de chaque destination
    *l'ID de chaque arrêt
    *Le temps qu'on met pour aller à chaque station

Toutes les minutes :
    -La raspi récupère via l'API le temps restant avant le passage des deux bus suivant pour chaque destination du panneau
    -La raspi fait : "temps de passage - temps pour rejoindre" pour chaque temps
        -Si le temps obtenu est inférieur à 0min ET que le temps du bus suivant est inférieur à 5min : ignore le bus 1 et traite les données du bus 2
        -Si le temps de passage x (j'ai bien dit temps de passage, et pas temps obtenu!) est inférieur à 1min, programmer un refresh au bout x secondes
    -la raspi map les temps sur un octet (+10min => 0s; 255=>0)
    -la raspi envoit les résultats dans l'ordre des ID à l'arduino

    -l'arduino stocke les valeurs dans un tableau
    -l'arduino calcule dans un autre tableau la correspondance en couleur:
        -255 : bleu = 255
        -entre 255 et 127 : bleu map(255=>0; 255=> 127) || vert map(0=>255; 10'=>5')
        -entre 127 et 0 : vert map(255=>0; 5'=>0') || rouge map(0=>255; 5'=>0')
