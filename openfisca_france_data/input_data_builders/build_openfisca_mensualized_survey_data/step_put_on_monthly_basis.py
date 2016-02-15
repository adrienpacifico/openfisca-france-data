


month_list = []

for mois in range(1,13):
    month_list.append("situation_mois{}".format(mois))

(indivi[month_list]== 3).sum(1) #Somme le nombre de valeurs égale à 3 pour chaque individus
(indivi[month_list]== 3).sum(1).value_counts()



for month in month_list :
    indivi.loc(indivi == 3, [revenu_cho_mois{}.format(mois)]) = indivi.choi/(indivi[month_list]== 3).sum(1)  #pour répartir les allocations chomages sur chaque mois.






#Non fonctionnel mais peut êtrte une piste pour trouver des pattern

for mois in range(1,13):

     indivi.loc(indivi["situation_mois{}".format(mois) - 1] == 3,'coucou') = 3
     indivi.loc(indivi["situation_mois{}".format(mois) - 1] == 3,'coucou') = 3


#Par exemple trouver retraité

for mois in range(1,13):
     indivi.loc(indivi["situation_mois{}".format(mois)] == 6,'parti_retraite') = True
for mois in range(1,13):
     indivi.loc(indivi['parti_retraite'] == True
                & indivi.isnull("situation_mois{}".format(mois))
                ,"situation_mois{}".format(mois)) = 6


