import random

valeur_offres = [random.randint(1,10) for i in range(random.randint(1,15))]
print(valeur_offres)

#Tri qui permet de classer les valeurs des offres dans l'ordre décroissant (afin de ne pas laisser dépasser une personne qui a une offre plus élevée que la sienne)
N=len(valeur_offres)
for i in range(N):
    minimum = valeur_offres[i]
    i_min = i
    for j in range(i,N):
        while valeur_offres[j] > minimum:
            minimum = valeur_offres[j]
            i_min = j
    tmp = valeur_offres[i]
    valeur_offres[i] = minimum
    valeur_offres[i_min] = tmp
print("\nListe triée :")
print(valeur_offres)
