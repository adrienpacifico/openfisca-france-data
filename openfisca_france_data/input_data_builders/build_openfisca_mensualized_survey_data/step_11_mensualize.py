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



import logging
import pandas as pd


from openfisca_core import periods
from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.temporary import temporary_store_decorator


log = logging.getLogger(__name__)

revi_month_list = ["revi_mois{}".format(month) for month in range(1,13)]



@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'erfs_mensualized')
def store_variables_by_periods(year = None, input_df = None,
                               monthly_variable_list = ["sali", 'rsti', 'choi'], temporary_store = None):
    dataframe_by_period = dict()
    for month in range(1, 13):
        dataframe = pd.DataFrame()
        for var in monthly_variable_list:
            period = periods.period("{}-{}".format(year, month))
            variable = var + "_mois{}".format(month)
            dataframe[var] = input_df[variable].copy()

        dataframe_by_period[period] = dataframe.copy()

    for period, dataframe in dataframe_by_period.iteritems():
        period_str = unicode(period)
        print period_str, dataframe.describe()
        dataframe.to_hdf(temporary_store, 'input_mensualized/period_{}'.format(period_str))





@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'erfs_mensualized')
def put_on_monthly_basis(temporary_store = None, year = None, check = True):

    assert temporary_store is not None
    assert year is not None

    log.info(u'11_final: derniers réglages')

    final = temporary_store['input_{}'.format(year)]
    mensualized_variables = ['sali','rsti','choi']
    store_variables_by_periods(input_df= final,
                               monthly_variable_list = ["sali"], year = year)



if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, filename = 'step_11.log', filemode = 'w')
    put_on_monthly_basis(year = year)
