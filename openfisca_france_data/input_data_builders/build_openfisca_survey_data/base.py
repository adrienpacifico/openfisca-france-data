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


def year_specific_by_generic_data_frame_name(year):
    yr = str(year)[2:]
    yr1 = str(year + 1)[2:]
    yr2 = str(year + 2)[2:]
    yr_1 = str(year - 1)[2:]
    return dict(
        erf_menage = "menage" + yr,  # Enquête revenu fiscaux, table ménage
        eec_menage = "mrf" + yr + "e" + yr + "t4",  # Enquête emploi en continu, table ménage
        foyer = "foyer" + yr,  # Enquête revenu fiscaux, table foyer # compressed file for 2006
        erf_indivi = "indivi{}".format(yr),  # Enquête revenu fiscaux, table individu
        eec_indivi = "irf" + yr + "e" + yr + "t4",  # Enquête emploi en continue, table individu (mois de référence de l'ERFS)
        eec_cmp__4 = "icomprf" + yr + "e" + yr_1 + "t1",  # Enquête emploi en continue, table complémentaires de l'année précédente
        eec_cmp__3 = "icomprf" + yr + "e" + yr_1 + "t2",
        eec_cmp__2 = "icomprf" + yr + "e" + yr_1 + "t3",
        eec_cmp__1 = "icomprf" + yr + "e" + yr_1 + "t4",
        eec_cmp1 = "icomprf" + yr + "e" + yr + "t1",  # Enquête emploi en continue, table complémentaires de l'année en cours
        eec_cmp2 = "icomprf" + yr + "e" + yr + "t2",
        eec_cmp3 = "icomprf" + yr + "e" + yr + "t3",
        eec_cmp5 = "icomprf" + yr + "e" + yr1 + "t1",  # Enquête emploi en continue, table complémentaire de l'année suivante
        eec_cmp6 = "icomprf" + yr + "e" + yr1 + "t2",
        eec_cmp7 = "icomprf" + yr + "e" + yr1 + "t3",
        eec_cmp8 = "icomprf" + yr + "e" + yr1 + "t4",
        eec_cmp9 = "icomprf" + yr + "e" + yr2 + "t4", # EEC 2 ans apres.
        )
