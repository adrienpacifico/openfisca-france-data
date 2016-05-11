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


from openfisca_core import periods
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
        collection = "openfisca_monthly", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_data_monthly{}".format(year))
    dataframe_by_periods = dict()
    for period in openfisca_survey.tables:
        input_data_frame = openfisca_survey.get_values(table = period)
        input_data_frame.rename(
            columns = dict(
                alr = 'pensions_alimentaires_percues',
                choi = 'cho',
                cho_ld = 'chomeur_longue_duree',
                fra = 'frais_reels',
                rsti = 'rst',
                sali = 'salaire_imposable', #TODO : changer le salaire imposable mensualisé ici
                ),
            inplace = True,
            )
        input_data_frame.reset_index(inplace = True)
        dataframe_by_periods[periods.period(period[7::])] = input_data_frame.copy()
    return dataframe_by_periods