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


import logging
import os


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.input_data_builders.build_openfisca_mensualized_survey_data import (  # analysis:ignore
    step_01_monthly_basis_pre_processing as pre_processing,
    #step_02_monthly_basis_imputation_loyer as imputation_loyer,
    step_03_monthly_basis_fip as fip,
    step_04_monthly_basis_famille as famille,
    step_05_monthly_basis_foyer as foyer,
    step_06_monthly_basis_rebuild as rebuild,
    step_07_monthly_basis_invalides as invalides,
    step_08_monthly_basis_final as final,
    )
from openfisca_france_data.temporary import get_store

from openfisca_survey_manager.surveys import Survey
from openfisca_survey_manager.survey_collections import SurveyCollection


log = logging.getLogger(__name__)


def run_all(year = None, check = False):

    assert year is not None
    pre_processing.create_indivim_menagem(year = year)
    pre_processing.create_enfants_a_naitre(year = year)
    #    try:
    #        imputation_loyer.imputation_loyer(year = year)
    #    except Exception, e:
    #        log.info('Do not impute loyer because of the following error: \n {}'.format(e))
    #        pass
    fip.create_fip(year = year)
    famille.famille(year = year)
    foyer.sif(year = year)
    foyer.foyer_all(year = year)
    rebuild.create_totals_first_pass(year = year)
    rebuild.create_totals_second_pass(year = year)
    rebuild.create_final(year = year)
    invalides.invalide(year = year)
    final.final(year = year, check = check)

    temporary_store = get_store(file_name = 'erfs_mensualized')
    data_frame = temporary_store['input_{}'.format(year)]
    import pdb ; pdb.set_trace()
    #Saving the data_frame
    openfisca_survey_collection = SurveyCollection(name = "openfisca", config_files_directory = config_files_directory)
    output_data_directory = openfisca_survey_collection.config.get('data', 'output_directory')
    survey_name = "openfisca_data_{}".format(year)
    table = "input_mensualized"
    hdf5_file_path = os.path.join(os.path.dirname(output_data_directory), "{}.h5".format(survey_name))
    survey = Survey(
        name = survey_name,
        hdf5_file_path = hdf5_file_path,
        )
    survey.insert_table(name = table, data_frame = data_frame)
    openfisca_survey_collection.surveys.append(survey)
    collections_directory = openfisca_survey_collection.config.get('collections', 'collections_directory')
    json_file_path = os.path.join(collections_directory, 'openfisca.json')
    openfisca_survey_collection.dump(json_file_path = json_file_path)


if __name__ == '__main__':
    import time
    start = time.time()
    logging.basicConfig(level = logging.INFO, filename = 'run_all.log', filemode = 'w')
    run_all(year = 2009, check = False)
    log.info("Script finished after {}".format(time.time() - start))
    print time.time() - start
