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


from openfisca_core import reforms

import openfisca_france
from openfisca_france.model.base import (BoolCol, CHEF, ENFS, Enum, EnumCol, Familles, FloatCol, FoyersFiscaux,
    Individus, IntCol, Menages, QUIFAM, QUIFOY, PART, VOUS)


__all__ = [
    'BoolCol',
    'CHEF',
    'DatedVariable',
    'ENFS',
    'EntityToPersonColumn',
    'Enum',
    'EnumCol',
    'Familles',
    'FloatCol',
    'FoyersFiscaux',
    'Individus',
    'IntCol',
    'Menages',
    'openfisca_france_tax_benefit_system',
    'PART',
    'PersonToEntityColumn',
    'QUIFAM',
    'QUIFOY',
    'TaxBenefitSystem',
    'Variable',
    'VOUS',
    ]

OpenFiscaFranceTaxBenefitSystem = openfisca_france.init_country()
openfisca_france_tax_benefit_system = OpenFiscaFranceTaxBenefitSystem()

from openfisca_france.reforms.mensualisation import mensualisation_ir_8 as mensualisation_ir

TaxBenefitSystem = reforms.make_reform(
    key = 'openfisca_france_data',
    name = u"OpenFisca for survey data",
    #reference = openfisca_france_tax_benefit_system,
    reference=mensualisation_ir.build_reform(openfisca_france_tax_benefit_system)
    )

# Export reform classes to register variables in reform column_by_name dict.
DatedVariable = TaxBenefitSystem.DatedVariable
EntityToPersonColumn = TaxBenefitSystem.EntityToPersonColumn
PersonToEntityColumn = TaxBenefitSystem.PersonToEntityColumn
Variable = TaxBenefitSystem.Variable
