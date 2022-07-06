VOC_CARBON_DICT = {'ethane': 2, 'ethene': 2,
                   'propane': 3, 'propene': 3, '1_3-butadiene': 4, 'i-butane': 4,
                   'n-butane': 4, 'acetylene': 2, 'i-pentane': 5, 'n-pentane': 5,
                   'n-hexane': 6, 'isoprene': 5, 'benzene': 6, 'n-heptane': 7,
                   'n-octane': 8, 'toluene': 7, 'ethyl-benzene': 8,
                   'm&p-xylene': 8, 'o-xylene': 8, 'cyclopentane': 5, 'acetone': 3, 'acetaldehyde': 2}

LAT_LON_DICT = {"BNP": '39.981 -105.006', "BLV": '39.979 -105.043', "BSE": '39.984 -105.037', "LMA": '40.160 -105.159',
                "LLG": ['none'], "LUR": '40.176 -105.048',
                "BRZ": '40.070 -105.220', "CCF": ['39.812770', '-104.948218'], "ECC": ['none'], }

NAME_DICT = {'co2': 'Carbon Dioxide', 'co2_ppm': 'Carbon Dioxide', 'co': 'Carbon Monoxide', 'ch4': 'Methane',
             'h2s': 'Hydrogen Sulfide', 'pm10': 'PM 10', 'pm2_5': 'PM 2.5',
             'o3': 'Ozone', 'no': 'Nitric Oxide', 'nox': 'Nitrogen Oxides', 'ethane': 'Ethane', 'ethene': 'Ethene',
             'propane': 'Propane', 'propene': 'Propene', '1_3-butadiene': '1, 3-Butadiene', 'i-butane': 'i-Butane',
             'n-butane': 'n-Butane', 'acetylene': 'Acetylene', 'i-pentane': 'i-Pentane', 'n-pentane': 'n-Pentane',
             'cyclopentane': 'Cyclopentane', 'acetone': 'Acetone', 'acetaldehyde': 'Acetaldehyde',
             'n-hexane': 'n-Hexane', 'isoprene': 'Isoprene', 'n-heptane': 'n-Heptane', 'benzene': 'Benzene',
             'n-octane': 'n-Octane', 'toluene': 'Toluene', 'toulene': 'Toluene', 'ethyl-benzene': 'Ethylbenzene',
             'm&p-xylene': 'm&p-Xylene', 'o-xylene': 'o-Xylene', 'solr': 'Solar Radiation', 'temp_f': 'Temperature',
             'temp_c': 'Temperature', 'relh': 'Relative Humidity', 'wsp_avg_ms': 'Wind Speed', 'wsp': 'Wind Speed',
             'wdr_avg': 'Wind Direction', 'wdr': 'Wind Direction'}

UNIT_DICT = {'co2': '(ppm)', 'co2_ppm': '(ppm)', 'co': '(ppb)', 'ch4': '(ppb)', 'h2s': '(ppb)', 'pm10': '(μg/m³)',
             'pm2_5': '(μg/m³)', 'o3': '(ppb)', 'no': '(ppb)', 'nox': '(ppb)', 'ethane': '(ppb)', 'ethene': '(ppb)',
             'propane': '(ppb)', 'propene': '(ppb)', '1_3-butadiene': '(ppb)', 'i-butane': '(ppb)',
             'n-butane': '(ppb)', 'acetylene': '(ppb)', 'i-pentane': '(ppb)', 'n-pentane': '(ppb)',
             'cyclopentane': '(ppb)',
             'n-hexane': '(ppb)', 'isoprene': '(ppb)', 'n-heptane': '(ppb)', 'benzene': '(ppb)',
             'n-octane': '(ppb)', 'toluene': '(ppb)', 'toulene': '(ppb)', 'ethyl-benzene': '(ppb)', 'acetone': '(ppb)',
             'acetaldehyde': '(ppb)',
             'm&p-xylene': '(ppb)', 'o-xylene': '(ppb)', 'solr': '(W/m²)', 'temp_f': '(°F)', 'temp_c': '(°C)',
             'relh': '(%RH)', 'wsp_avg_ms': '(m/s)', 'wsp': '(m/s)', 'wdr_avg': '(Degrees)',
             'wdr': '(Degrees)'}

COLOR_DICT = {"BNP": '#70a597', "BLV": '#70a597', "BSE": '#0CF215', "LMA": '#E84B10', "LLG": '#E84B10',
              "LUR": '#B10CF2',
              "BRZ": '#008BE8', "CCF": '#283593', "CCM": '#2e5575', "ECC": '#ffc107'}

VOC_DICT = {'ethane': 'voc', 'ethene': 'voc',
            'propane': 'voc', 'propene': 'voc', '1_3-butadiene': 'voc', 'i-butane': 'voc',
            'n-butane': 'voc', 'acetylene': 'voc', 'i-pentane': 'voc', 'n-pentane': 'voc',
            'n-hexane': 'voc', 'isoprene': 'voc', 'benzene': 'voc', 'n-heptane': 'voc', 'acetone': 'voc',
            'acetaldehyde': 'voc',
            'n-octane': 'voc', 'toluene': 'voc', 'cyclopentane': 'voc', 'toulene': 'voc', 'ethyl-benzene': 'voc',
            'm&p-xylene': 'voc', 'o-xylene': 'voc', 'solr': 'voc', 'temp_f': 'voc'}

QUARTERLY_MONTHS_DICT = {'q1': ['01-01', '04-01'], 'q2': ['04-01', '07-01'], 'q3': ['07-01', '10-01'],
                         'q4': ['10-01', '12-01']}

VOC_LIST = ['ethane', 'ethene', 'propane', 'propene', '1_3-butadiene', 'i-butane', 'n-butane', 'acetylene', 'i-pentane',
            'n-pentane', 'n-hexane', 'isoprene', 'benzene', 'n-heptane', 'acetone', 'acetaldehyde', 'n-octane',
            'toluene', 'cyclopentane', 'ethyl-benzene', 'm&p-xylene', 'o-xylene']

MET_LIST = ['solr', 'temp_f', 'relh', 'wsp_avg_ms', 'wdr_avg', 'ptemp_f', 'tempinstr_f', 'wsp', 'wdr']
