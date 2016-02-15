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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.rename(
        columns = dict(
            alr = 'pensions_alimentaires_percues',
            choi = 'chomage_imposable',
            cho_ld = 'chomeur_longue_duree',
            fra = 'frais_reels',
            rsti = 'retraite_imposable',
            sali = 'salaire_imposable',
            ),
        inplace = True,
        )
    input_data_frame.reset_index(inplace = True)
    return input_data_frame



def get_monthly_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input_mensualized")
    input_data_frame.rename(
        columns = dict(
            alr = 'pensions_alimentaires_percues',
            choi = 'cho',
            cho_ld = 'chomeur_longue_duree',
            fra = 'frais_reels',
            rsti = 'rst',
            sali = 'salaire_imposable', #TODO : changer le salaire imposable mensualisé ici
            sali1 = 'salaire_imposable1',
            sali2 = 'salaire_imposable2',
            sali3 = 'salaire_imposable3',
            sali4 = 'salaire_imposable4',
            sali5 = 'salaire_imposable5',
            sali6 = 'salaire_imposable6',
            sali7 = 'salaire_imposable7',
            sali8 = 'salaire_imposable8',
            sali9 = 'salaire_imposable9',
            sali10 = 'salaire_imposable10',
            sali11 = 'salaire_imposable11',
            sali12 = 'salaire_imposable12',
            ),
        inplace = True,
        )
    input_data_frame.reset_index(inplace = True)
    return input_data_frame