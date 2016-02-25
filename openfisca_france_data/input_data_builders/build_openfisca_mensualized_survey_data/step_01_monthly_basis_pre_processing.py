#! /usr/bin/env python
# -*- coding: utf-8 -*-


#Filter vars places (if you want to add a new variable you need to include it in all those steps...
# Step 6 : l671


import gc
import numpy
import logging


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_data.temporary import temporary_store_decorator
from openfisca_france_data.input_data_builders.build_openfisca_survey_data.utils import assert_dtype
from openfisca_france_data.input_data_builders.build_openfisca_mensualized_survey_data.base import year_specific_by_generic_data_frame_name

from openfisca_survey_manager.survey_collections import SurveyCollection



log = logging.getLogger(__name__)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = "erfs_mensualized")
def create_indivim_menagem(temporary_store = None, year = None):
    """
    Création des tables ménages et individus concaténée (merged)
    """
    # Prepare the some useful merged tables

    assert temporary_store is not None
    assert year is not None
    # load data
    erfs_survey_collection = SurveyCollection.load(
        collection = 'erfs', config_files_directory = config_files_directory)

    year_specific_by_generic = year_specific_by_generic_data_frame_name(year)
    survey = erfs_survey_collection.get_survey('erfs_{}'.format(year))
    erfmen = survey.get_values(table = year_specific_by_generic["erf_menage"])
    eecmen = survey.get_values(table = year_specific_by_generic["eec_menage"])
    erfind = survey.get_values(table = year_specific_by_generic["erf_indivi"])
    eecind = survey.get_values(table = year_specific_by_generic["eec_indivi"])

    eec_1 = survey.get_values(table = year_specific_by_generic["eec_cmp1"])
    eec_2 = survey.get_values(table = year_specific_by_generic["eec_cmp2"])
    eec_3 = survey.get_values(table = year_specific_by_generic["eec_cmp3"])

    assert (eec_1.shape < eec_2.shape) &  (eec_2.shape < eec_3.shape)  &  (eec_3.shape < eecind.shape) # due to the survey  eec_1.shape is 3/6 of eecind.shape ; eec_2 is 4/6 ; and eec_3 is 5/6.
    



    # travail sur la cohérence entre les bases
    noappar_m = eecmen[~(eecmen.ident.isin(erfmen.ident.values))].copy()

    noappar_i = eecmen[~(eecind.ident.isin(erfind.ident.values))].copy()
    noappar_i = noappar_i.drop_duplicates(subset = 'ident', take_last = True)
    # TODO: vérifier qu'il n'y a théoriquement pas de doublon



    # Vérifie les individus de l'eec qui ne sont pas appareillé, nomalement on doit se retrouver qu'avec la moitié du sample.

    (eec_1.ident.isin(eec_2.ident.values) & eec_1.ident.isin(eec_3.ident.values)).value_counts()  #TODO: confirm that it is due to attrition 3369/47312, explain attrition (death, MDS ? )

    log.info("There are {} over {} obs that are in eec_1 but not in eec_2 and eec_3 ".format(3369, 47312 )) #TODO : automatize




    #remove attrition
    attrition_ident = eec_1[(~(eec_1.ident.isin(eec_2.ident.values) & eec_1.ident.isin(eec_3.ident.values)))].ident
    #attrition_ident_set = set(attrition.ident)
    #print len(attrition_ident_set)  #1326

    #assert numpy.all(attrition == attrition &  eec_1.ident.isin(eecind.ident.values))
    print eec_1.shape
    eec_1 = eec_1[~eec_1.ident.isin(attrition_ident.values)].copy()
    print eec_1.shape
    #attrition = set(attrition.ident)
    print eec_2.shape
    eec_2 = eec_2[~eec_2.ident.isin(attrition_ident.values)].copy()
    print eec_2.shape
    print eec_3.shape
    eec_3 = eec_3[~eec_3.ident.isin(attrition_ident.values)].copy()
    print eec_3.shape #TODO : bien comprendre et expliquer correctement les shapes



    #explication : les attritions des gens qui sont dans eec_1 mais pas dans 2 ou 3





    #remove obs in eec_2 and/or eec_3 but not in eec_1

    print (eec_2.ident.isin(eec_1.ident.values) & eec_3.ident.isin(eec_1.ident.values)).value_counts()
    eec_3 = eec_3[eec_3.ident.isin(eec_1.ident.values)].copy()
    eec_2 = eec_2[eec_2.ident.isin(eec_1.ident.values)].copy()
    print (eec_2.ident.isin(eec_1.ident.values) & eec_3.ident.isin(eec_1.ident.values)).value_counts()

    # On a dans eec_1 38% d'eecind, pourquoi ? (censé avoir 50% ?)




### On identifie quel eec appartien a quel eec avant le merge
    ## Pour l'instant ça ne sert à rien car on a trim qui identifie ces bases pour une seule année, mais si plusieurs
    ## années ça peut être utile
    eec_1['queleec'] = 1
    eec_2['queleec'] = 2
    eec_3['queleec'] = 3
    eecind['queleec'] = 4




    # for year in range(2009,2010): #qu'une seule année pour l'instant
    #     for rga in range(1,5):
    #         for sp in range(0,3):
    #             situation_mois = (rga*3)-3 + sp -2
    #             final.loc[final.RGA == rga,'situation_mois{}'.format(situation_mois) ] = final["sp{}".format(str(2 - sp).zfill(2))]
    #             #print (result.TRIM == trim).value_counts()
    #
    #             print situation_mois, str(2 - sp).zfill(2),rga


    for table in [eec_1, eec_2, eec_3, eecind]: #attention on décale de deux mois situation_mois1 correspond novembre de l'année précédente !!!
        for trim in range(1,5):
            for sp in range(0,3):
                situation_mois = (trim*3 + sp -2)
                table.loc[table.trim == trim,'situation_mois{}'.format(situation_mois) ] = table["sp{}".format(str(2 - sp).zfill(2))]
                print situation_mois, str(2 - sp).zfill(2), trim






    #pour comprendre
        # for trim in range(1,5):
        #     for sp in range(0,3):
        #         situation_mois = (trim*3 + sp -2)
        #         print situation_mois, str(2 - sp).zfill(2), trim






#### puis colapse


    #trouver identifiant individuel personne, le mettre en index, faire les combine first.

    eecind.set_index('noindiv', inplace = True, drop = False)
    eec_1.set_index('noindiv', inplace = True, drop = False)
    eec_2.set_index('noindiv', inplace = True, drop = False)
    eec_3.set_index('noindiv', inplace = True, drop = False)

    eecind_mensualized = eecind.combine_first(eec_1)
    eecind_mensualized = eecind_mensualized.combine_first(eec_2)
    eecind_mensualized = eecind_mensualized.combine_first(eec_3)





    eecind.reset_index(drop = True)
    eec_1.reset_index(drop = True)
    eec_2.reset_index(drop = True)
    eec_3.reset_index(drop = True)












    difference = set(noappar_i.ident).symmetric_difference(noappar_m.ident)
    intersection = set(noappar_i.ident) & set(noappar_m.ident)
    log.info("There are {} differences and {} intersections".format(len(difference), len(intersection)))
    del noappar_i, noappar_m, difference, intersection
    gc.collect()




    # fusion enquete emploi et source fiscale
    menagem = erfmen.merge(eecmen)

    indivim = eecind_mensualized.merge(erfind, on = ['noindiv', 'ident', 'noi'], how = "inner")


    # optimisation des types? Controle de l'existence en passant
    # TODO: minimal dtype
    # TODO: this should be done somewhere else
    var_list = ([
        'acteu',
        'agepr',
        'cohab',
        'contra',
        'encadr',
        'forter',
        'lien',
        'mrec',
        'naia',
        'noicon',
        'noimer',
        'noiper',
        'prosa',
        'retrai',
        'rstg',
        'statut',
        'stc',
        'titc',
        'txtppb',
        ])

    ###### Rajouté à l'arache, voir en amont pourquoi le dtype d'acteu est changé par le set_index
    ##### TODO: CRADE !

    for var in var_list:
         indivim[var] = indivim[var].astype('int')

    ####
    for var in var_list:
        assert numpy.issubdtype(indivim[var].dtype , numpy.integer), "Variable {} dtype is {} and should be an integer".format(
            var, indivim[var].dtype)

    ########################
    # création de variables#
    ########################

# codage SP


# 1 Occupe un emploi (salarié, à votre compte, y compris aide d'une personne dans son travail, un apprentissage sous contrat ou un stage rémunéré)
# 2 Etudes (élèves, étudiants) ou stage non rémunéré
# 3 Chômage (inscrit ou non à Pôle emploi (ex ANPE))
# 4 Retraite ou préretraite (ancien salarié ou ancien indépendant)
# 5 Femme ou Homme au foyer
# 6 Autre inactif
#
# recode = sp
# 8 = 6
# 8 = 5
# 1 ou 2 ou 3 = 1 (cdi, cdd, a son compte)
# 5 = 2 (etudiant)
# 7 = 4
# 0 = Nan



#TODO : faire jolie boucle


    for month in range(1,13):
        sitmoi = "situation_mois{}".format(month)
        actrec = "actrec_mois{}".format(month)


    #   actrec : activité recodée comme preconisé par l'INSEE p84 du guide utilisateur
        indivim["actrec_mois{}".format(month)] = numpy.nan
        # 3: contrat a durée déterminée
        indivim[actrec].loc[indivim[sitmoi] == 1] = 3     #TODO : voir si dans les réinterrogations on peut distinguer les cdd, mis en occupe emploi
        # 8 : femme (homme) au foyer, autre inactif
        indivim[actrec].loc[indivim[sitmoi] == 6] = 8
        # 1 : actif occupé non salarié
        #filter1 = (indivim.acteu == 1) & (indivim.stc.isin([1, 3]))  # actifs occupés non salariés à son compte ou pour un #TODO: IDEM
        indivim[actrec].loc[indivim[sitmoi] == 1] = 1                              # membre de sa famille
        # 2 : salarié pour une durée non limitée
        #filter2 = (indivim.acteu == 1) & (((indivim.stc == 2) & (indivim.contra == 1)) | (indivim.titc == 2))
        indivim[actrec].loc[indivim[sitmoi] == 1] = 2 #TODO: IDEM
        # 4 : au chomage
        filter4 = (indivim.acteu == 2) | ((indivim.acteu == 3) & (indivim.mrec == 1))
        indivim[actrec].loc[indivim[sitmoi] == 3] = 4
        # 5 : élève étudiant , stagiaire non rémunéré
        filter5 = (indivim.acteu == 3) & ((indivim.forter == 2) | (indivim.rstg == 1))
        indivim[actrec].loc[indivim[sitmoi] == 2] = 5
        # 7 : retraité, préretraité, retiré des affaires unchecked
        filter7 = (indivim.acteu == 3) & ((indivim.retrai == 1) | (indivim.retrai == 2))
        indivim[actrec].loc[indivim[sitmoi] == 4] = 7
        # 9 : probablement enfants de - de 16 ans
        indivim[actrec].loc[indivim[sitmoi] == 0] = 9  #TODO: distinguer les retraités des enfants de moins de 16 ans
        indivim[actrec].loc[indivim[actrec].isnull()] = 99 # TODO : corriger

        #assert indivim[actrec].isnull().value_counts() == indivim[sitmoi].isnull().value_counts() # TODO : plus de sitmois null que d'actrec, pourquoi, pas normal ?!

        indivim[actrec].fillna(value = 0, inplace = True)
        indivim[actrec] = indivim[actrec].astype("int8")

        #assert indivim[actrec].isnull().value_counts() == indivim[sitmoi].isnull().value_counts()
        # TODO : mensualiser NBTEMP pour prendre en compte ceux qui ont plusieurs emplois, HHX le nombre d'heure moyenne par semaine (faire la variation)

    for month in range(1,13):
        assert_dtype(indivim[actrec], "int8")
        #assert indivim[actrec].isin(range(0, 10)).all(), 'actrec values are outside the interval [1, 9]' #mis 0 pour les NaN # TODO : se débrouiller pour mieux gérer le truc avec la valeur 99



  #  print indivim
#   actrec : activité recodée comme preconisé par l'INSEE p84 du guide utilisateur
    indivim["actrec"] = numpy.nan
    # Attention : Q: pas de 6 ?!! A : Non pas de 6, la variable recodée de l'INSEE (voit p84 du guide methodo), ici \
    # la même nomenclature à été adopée
    # 3: contrat a durée déterminée
    indivim.actrec.loc[indivim.acteu == 1] = 3
    # 8 : femme (homme) au foyer, autre inactif
    indivim.actrec.loc[indivim.acteu == 3] = 8
    # 1 : actif occupé non salarié
    filter1 = (indivim.acteu == 1) & (indivim.stc.isin([1, 3]))  # actifs occupés non salariés à son compte ou pour un
    indivim.actrec.loc[filter1] = 1                              # membre de sa famille
    # 2 : salarié pour une durée non limitée
    filter2 = (indivim.acteu == 1) & (((indivim.stc == 2) & (indivim.contra == 1)) | (indivim.titc == 2))
    indivim.actrec.loc[filter2] = 2
    # 4 : au chomage
    filter4 = (indivim.acteu == 2) | ((indivim.acteu == 3) & (indivim.mrec == 1))
    indivim.actrec.loc[filter4] = 4
    # 5 : élève étudiant , stagiaire non rémunéré
    filter5 = (indivim.acteu == 3) & ((indivim.forter == 2) | (indivim.rstg == 1))
    indivim.actrec.loc[filter5] = 5
    # 7 : retraité, préretraité, retiré des affaires unchecked
    filter7 = (indivim.acteu == 3) & ((indivim.retrai == 1) | (indivim.retrai == 2))
    indivim.actrec.loc[filter7] = 7
    # 9 : probablement enfants de - de 16 ans TODO: check that fact in database and questionnaire
    indivim.actrec.loc[indivim.acteu == 0] = 9

    indivim.actrec = indivim.actrec.astype("int8")
    assert_dtype(indivim.actrec, "int8")
    assert indivim.actrec.isin(range(1, 10)).all(), 'actrec values are outside the interval [1, 9]'

#   TODO : compare the result with results provided by Insee
#   tu99
    if year == 2009:
        erfind['tu99'] = None  # TODO: why ?


    # Locataire
    menagem["locataire"] = menagem.so.isin([3, 4, 5])
    assert_dtype(menagem.locataire, "bool")


    transfert = indivim.loc[indivim.lpr == 1, ['ident', 'ddipl']].copy()
    menagem = menagem.merge(transfert)


    # Correction
    def _manually_remove_errors():
        '''
        This method is here because some oddities can make it through the controls throughout the procedure
        It is here to remove all these individual errors that compromise the process.
        '''
        if year == 2006:
            indivim.lien[indivim.noindiv == 603018905] = 2
            indivim.noimer[indivim.noindiv == 603018905] = 1
            log.info("{}".format(indivim[indivim.noindiv == 603018905].to_string()))

    _manually_remove_errors()

    temporary_store['menagem_{}'.format(year)] = menagem
    del eecmen, erfmen, menagem, transfert
    gc.collect()
    temporary_store['indivim_{}'.format(year)] = indivim
    del erfind, eecind


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = "erfs_mensualized")  #TODO : find how to catch a child birth during the year
def create_enfants_a_naitre(temporary_store = None, year = None):
    '''
    '''
    assert temporary_store is not None
    assert year is not None
    erfs_survey_collection = SurveyCollection.load(
        collection = 'erfs', config_files_directory = config_files_directory)
    survey = erfs_survey_collection.get_survey('erfs_{}'.format(year))
    # Enfant à naître (NN pour nouveaux nés)
    individual_vars = [
        'acteu',
        'agepr',
        'cohab',
        'contra',
        'forter',
        'ident',
        'lien',
        'lpr',
        'mrec',
        'naia',
        'naim',
        'noi',
        'noicon',
        'noimer',
        'noindiv',
        'noiper',
        'retrai',
        'rga',
        'rstg',
        'sexe',
        'stc',
        'titc',
        ]
    year_specific_by_generic = year_specific_by_generic_data_frame_name(year)
    eeccmp1 = survey.get_values(table = year_specific_by_generic["eec_cmp5"], variables = individual_vars) # TODO : check ça prend les enfants de l'année après pas d'avant...
    eeccmp2 = survey.get_values(table = year_specific_by_generic["eec_cmp6"], variables = individual_vars)
    eeccmp3 = survey.get_values(table = year_specific_by_generic["eec_cmp7"], variables = individual_vars)
    tmp = eeccmp1.merge(eeccmp2, how = "outer")
    enfants_a_naitre = tmp.merge(eeccmp3, how = "outer")

    # optimisation des types? Controle de l'existence en passant
    # pourquoi pas des int quand c'est possible
    # TODO: minimal dtype TODO: shoudln't be here
    for var in individual_vars:
        assert_dtype(enfants_a_naitre[var], 'float')
    del eeccmp1, eeccmp2, eeccmp3, individual_vars, tmp
    gc.collect()

    # création de variables
    enfants_a_naitre['declar1'] = ''
    enfants_a_naitre['noidec'] = 0
    enfants_a_naitre['ztsai'] = 0
    enfants_a_naitre['year'] = year
    enfants_a_naitre.year = enfants_a_naitre.year.astype("float32")  # TODO: should be an integer but NaN are present
    enfants_a_naitre['agepf'] = enfants_a_naitre.year - enfants_a_naitre.naia
    enfants_a_naitre.loc[enfants_a_naitre.naim >= 7,'agepf'] -= 1
    enfants_a_naitre['actrec'] = 9
    enfants_a_naitre['quelfic'] = 'ENF_NN'
    enfants_a_naitre['persfip'] = ""

    # TODO: deal with agepf
    for series_name in ['actrec', 'noidec', 'ztsai']:
        assert_dtype(enfants_a_naitre[series_name], "int")

    # selection
    enfants_a_naitre = enfants_a_naitre[
        (
            (enfants_a_naitre.naia == enfants_a_naitre.year) & (enfants_a_naitre.naim >= 10)
            ) | (
                (enfants_a_naitre.naia == enfants_a_naitre.year + 1) & (enfants_a_naitre.naim <= 5)
                )
        ].copy()

    temporary_store["enfants_a_naitre_{}".format(year)] = enfants_a_naitre

if __name__ == '__main__':
    log.info('Entering 01_pre_proc')
    import sys
    import time
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    deb = time.clock()
    year = 2009
    create_indivim_menagem(year = year)
    create_enfants_a_naitre(year = year)
    log.info("etape 01 pre-processing terminee en {}".format(time.clock() - deb))
