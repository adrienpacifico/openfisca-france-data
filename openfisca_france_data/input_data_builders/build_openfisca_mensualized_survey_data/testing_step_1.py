import logging
import os


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.input_data_builders.build_openfisca_mensualized_survey_data import (  # analysis:ignore
    step_01_pre_processing as pre_processing,
    step_02_imputation_loyer as imputation_loyer,
    step_03_fip as fip,
    step_04_famille as famille,
    step_05_foyer as foyer,
    step_06_rebuild as rebuild,
    step_07_invalides as invalides,
    step_08_final as final,
    )
from openfisca_france_data.temporary import get_store

from openfisca_survey_manager.surveys import Survey
from openfisca_survey_manager.survey_collections import SurveyCollection


log = logging.getLogger(__name__)


if __name__ == '__main__':
    import time
    start = time.time()
    logging.basicConfig(level = logging.INFO, filename = 'run_all.log', filemode = 'w')
    import ipdb
    ipdb.set_trace()

    pre_processing.create_indivim_menagem(year = 2009)

    log.info("Script finished after {}".format(time.time() - start))
