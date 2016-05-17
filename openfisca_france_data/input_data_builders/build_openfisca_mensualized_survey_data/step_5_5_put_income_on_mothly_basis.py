#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import gc
import logging

from pandas import Series, concat
import numpy as np
from numpy import where

from openfisca_france_data.temporary import temporary_store_decorator
from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.input_data_builders.build_openfisca_mensualized_survey_data.base import (
    year_specific_by_generic_data_frame_name
    )
from openfisca_france_data.input_data_builders.build_openfisca_mensualized_survey_data.utils import print_id, control
from openfisca_survey_manager.survey_collections import SurveyCollection


log = logging.getLogger(__name__)



@temporary_store_decorator(config_files_directory = config_files_directory, file_name = "erfs_mensualized")
def put_income_on_monthly_basis(temporary_store = None, year = None):
    assert temporary_store is not None
    assert year is not None

    log.info(u"Put income on monthly basis")

    indivi = temporary_store['indivim_{}'.format(year)] #TODO: Rename all indivi to indivim


# ######
# # TODO : Supprimer prochaines lignes, crade juste pour faire un essai de mensualisation
#
#     for month in range(1,13):
#         pass
#
#
#     situation_mois_string_list = []
#     for month in range(1,13):
#         sali_mois_string_list.append("sali_mois{}".format(month))
#
#
#
# #################





    # Crée les variables mois à garder
    actrec_mois_string_list = []
    for month in range(1,13):
        actrec_mois_string_list.append("actrec_mois{}".format(month))
    sit_mois_list = ["situation_mois{}".format(month) for month in range(1,13)]
    salaire_mois_list = ["sali_mois{}".format(month) for month in range(1,13)]
    chomage_mois_list = ["choi_mois{}".format(month) for month in range(1,13)]
    retraite_mois_list = ["rsti_mois{}".format(month) for month in range(1,13)]
    revenu_mois_list = ["revi_mois{}".format(month) for month in range(1,13)]


######## Perte d'emploi #########  #Contient les passage à la retraite, en inactivité, etc
    for month in range(2,13):
        changement_situation_mois = "perte_emploi_mois{}".format(month)
        sitmois_minus_one = "situation_mois{}".format(month-1)
        sitmois = "situation_mois{}".format(month)

        indivi[changement_situation_mois] = ((indivi[sitmois]!=1) & (indivi[sitmois_minus_one]==1))


###### Fin Perte d'emploi#####



######## Gagne d'emploi #########
    for month in range(2,13):
        changement_situation_mois = "gain_emploi_mois{}".format(month)
        sitmois_minus_one = "situation_mois{}".format(month-1)
        sitmois = "situation_mois{}".format(month)

        indivi[changement_situation_mois] = ((indivi[sitmois]==1) & (indivi[sitmois_minus_one]!=1))


###### Fin Gagne emploi#####



##### Passage à la retraite ####
    for month in range(2,13):
        changement_situation_mois = "passage_retraite_mois{}".format(month)
        sitmois_minus_one = "situation_mois{}".format(month-1)
        sitmois = "situation_mois{}".format(month)

        indivi[changement_situation_mois] = ((indivi[sitmois]==4) & (indivi[sitmois_minus_one]==1)) # TODO: voir si on loupe pas d'autre retaité (voir actrec et rsti ?)


##### Fin Passage à la retraite ####


##### Passage au chomage ####
    for month in range(2,13):
        changement_situation_mois = "passage_chomage_mois{}".format(month)
        sitmois_minus_one = "situation_mois{}".format(month-1)
        sitmois = "situation_mois{}".format(month)

        indivi[changement_situation_mois] = ((indivi[sitmois]==3) & (indivi[sitmois_minus_one]==1)) # TODO: voir si on loupe pas d'autre retaité (voir actrec et rsti ?)


##### Fin Passage au chomage####




##### Sortie du chomage vers l'emploi####
    for month in range(2,13):
        changement_situation_mois = "sortie_chomage_to_emploi_mois{}".format(month)
        sitmois_minus_one = "situation_mois{}".format(month-1)
        sitmois = "situation_mois{}".format(month)

        indivi[changement_situation_mois] = ((indivi[sitmois]==1) & (indivi[sitmois_minus_one]==3)) # TODO: voir si on loupe pas d'autre retaité (voir actrec et rsti ?)


##### Fin Sortie du chomage vers l'emploi####




    sit_mois_list = ["situation_mois{}".format(month) for month in range(1,13)]
##### Assigniation des sali choi et rsti mensuel####

    nb_mois_actif = (indivi[sit_mois_list]==1).sum(1)
    nb_mois_chomeur = (indivi[sit_mois_list]==3).sum(1)
    nb_mois_ss_rev_act = ((indivi[sit_mois_list]== 2) | (indivi[sit_mois_list]== 4)| (indivi[sit_mois_list]== 5) |  (indivi[sit_mois_list]== 6)).sum(1)


    nb_mois_retraite = (indivi[sit_mois_list]==4).sum(1)  #les séquences des retraités sont bisare, parfois renségnées parfois non


    # Nb de mois de retraite : si retraité == 4 sur un mois et jamais égal à 1,3,5,6 alors nb_mois = 12

    est_retraite_during_year = ((indivi[sit_mois_list]==4).sum(1) <12) & ((indivi[sit_mois_list]==4).sum(1) >0)



    is_in_target_sample = (indivi.rga == 6) | (indivi.rga == 5) | (indivi.rga == 4)
    indivi["is_in_target_sample"] = is_in_target_sample


    nest_pas_retraite_during_year = (((indivi[sit_mois_list]==4).sum(1) >1)                 #TODO : regarder la différence entre NaN et 0 dans situation_mois
                                        | ((indivi[sit_mois_list]==3).sum(1) >1)
                                        | ((indivi[sit_mois_list]==5).sum(1) >1)
                                        | ((indivi[sit_mois_list]==6).sum(1) >1))

    indivi[est_retraite_during_year & nest_pas_retraite_during_year & is_in_target_sample]==0 #TODO : le matin, mettre les is_in_target_sample dans le step one !

    for month in range(1,13):
        sitmois = "situation_mois{}".format(month)
        salaire_mois = "sali_mois{}".format(month)
        chomage_mois = "choi_mois{}".format(month)
        retraite_mois = "rsti_mois{}".format(month)
        revenu_mois = "revi_mois{}".format(month)


        indivi[salaire_mois] = indivi[(indivi[sitmois] == 1)]['sali']/nb_mois_actif
        #indivi[salaire_mois] = indivi[(indivi[sitmois] == 1) & (indivi[nb_mois_actif>0 ])]['sali']/nb_mois_actif
        indivi[chomage_mois] = indivi[indivi[sitmois] == 3]['choi']/nb_mois_chomeur
        indivi[retraite_mois] = indivi[indivi[sitmois] == 4]['rsti']/nb_mois_retraite
        indivi[retraite_mois] = indivi[indivi[sitmois] == 2]['rsti']/nb_mois_retraite

        indivi[revenu_mois] = indivi[salaire_mois].fillna(0) + indivi[chomage_mois].fillna(0) + indivi[retraite_mois].fillna(0)

#        indivi[(nb_mois_actif == 0)&(indivi.sali>0)& is_in_target_sample] =


        ###indivi[(nb_mois_actif == 0)&(indivi.sali>0)& is_in_target_sample].sort('sali', ascending = False).sali
        ### Il y a 1681  personnes dont le salaire déclaré est positif

        ### indivi[(nb_mois_actif == 0)&(indivi.sali>0)& is_in_target_sample].sort('sali', ascending = False).sali.hist()
        ### indivi[(nb_mois_actif == 0)&(indivi.sali>0)& is_in_target_sample & (indivi.sali<25000)].sort('sali', ascending = False).sali.hist()
        #### la majorité sont sur des salaires faibles

    #import ipdb; ipdb.set_trace()



##### Fin Assigniation des sali mensuel####

### Controle que l'on a pas perdu de revenu ####

    #assert indivi[salaire_mois_list].sum(1) == indivi.sali #TODO : avoir ça en place !
    #assert indivi[chomage_mois_list].sum(1) == indivi.choi
    #assert indivi[retraite_mois_list].sum(1) == indivi.rsti

    indivi["difference_sum_sali"] = indivi[salaire_mois_list].sum(1) - indivi.sali
    indivi["difference_sum_choi"] = indivi[chomage_mois_list].sum(1) - indivi.choi
    indivi["difference_sum_rsti"] = indivi[retraite_mois_list].sum(1) - indivi.rsti


    temporary_store['indivim_monthly{}'.format(year)] = indivi






if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, filename = 'step_5.5.log', filemode = 'w')
    put_income_on_monthly_basis(year = year)


