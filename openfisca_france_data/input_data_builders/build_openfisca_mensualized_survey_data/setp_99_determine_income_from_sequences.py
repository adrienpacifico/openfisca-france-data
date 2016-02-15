__author__ = 'adrienpacifico'


# Determine monthly income from working sequences



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
def determine_sequences(temporary_store = None, year = None):
    assert temporary_store is not None
    assert year is not None

    # On part de la table individu de l'ERFS
    # on renomme les variables
    log.info(u"Creating Totals")
    log.info(u"Etape 1 : Chargement des données")

    tot3 = temporary_store['tot3_{}'.format(year)]
    return tot3


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = "erfs_mensualized")
def passage_a_la_retraite(temporary_store = None, year = None):
    assert temporary_store is not None
    assert year is not None

    # On part de la table individu de l'ERFS
    # on renomme les variables
    log.info(u"Creating Totals")
    log.info(u"Etape 1 : Chargement des données")

    indivim = temporary_store['final_{}'.format(year)]





if __name__ == '__main__':
    year = 2009
    logging.basicConfig(level = logging.INFO, filename = 'step_06.log', filemode = 'w')
    create_totals_first_pass(year = year)
    create_totals_second_pass(year = year)
    create_final(year = year)
    log.info(u"étape 06 remise en forme des données terminée")