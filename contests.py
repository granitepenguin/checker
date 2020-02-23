#!/usr/local/bin/python3
#
# contests.py
#
# module for calculating contest results

# Things to add
# TODO : divine State from ARRL section
# TODO : handle missing MODE exception (W3SW example)

import re
import sys

# Enumerations
categories = {
    5: 'QRP 5 watts',
    25: 'Low Power 25 watts',
    50: 'Medium Power 50 watts',
    100: 'High Power 100 watts',
}

dxcc_entities = {
    '0': {"name": "None (the contacted station is known to not be within a DXCC entity)", "deleted": False},
    '1': {"name": "CANADA", "deleted": False},
    '2': {"name": "ABU AIL IS.", "deleted": True},
    '3': {"name": "AFGHANISTAN", "deleted": False},
    '4': {"name": "AGALEGA & ST. BRANDON IS.", "deleted": False},
    '5': {"name": "ALAND IS.", "deleted": False},
    '6': {"name": "ALASKA", "deleted": False},
    '7': {"name": "ALBANIA", "deleted": False},
    '8': {"name": "ALDABRA", "deleted": True},
    '9': {"name": "AMERICAN SAMOA", "deleted": False},
    '10': {"name": "AMSTERDAM & ST. PAUL IS.", "deleted": False},
    '11': {"name": "ANDAMAN & NICOBAR IS.", "deleted": False},
    '12': {"name": "ANGUILLA", "deleted": False},
    '13': {"name": "ANTARCTICA", "deleted": False},
    '14': {"name": "ARMENIA", "deleted": False},
    '15': {"name": "ASIATIC RUSSIA", "deleted": False},
    '16': {"name": "NEW ZEALAND SUBANTARCTIC ISLANDS", "deleted": False},
    '17': {"name": "AVES I.", "deleted": False},
    '18': {"name": "AZERBAIJAN", "deleted": False},
    '19': {"name": "BAJO NUEVO", "deleted": True},
    '20': {"name": "BAKER & HOWLAND IS.", "deleted": False},
    '21': {"name": "BALEARIC IS.", "deleted": False},
    '22': {"name": "PALAU", "deleted": False},
    '23': {"name": "BLENHEIM REEF", "deleted": True},
    '24': {"name": "BOUVET", "deleted": False},
    '25': {"name": "BRITISH NORTH BORNEO", "deleted": True},
    '26': {"name": "BRITISH SOMALILAND", "deleted": True},
    '27': {"name": "BELARUS", "deleted": False},
    '28': {"name": "CANAL ZONE", "deleted": True},
    '29': {"name": "CANARY IS.", "deleted": False},
    '30': {"name": "CELEBE & MOLUCCA IS.", "deleted": True},
    '31': {"name": "C. KIRIBATI (BRITISH PHOENIX IS.)", "deleted": False},
    '32': {"name": "CEUTA & MELILLA", "deleted": False},
    '33': {"name": "CHAGOS IS.", "deleted": False},
    '34': {"name": "CHATHAM IS.", "deleted": False},
    '35': {"name": "CHRISTMAS I.", "deleted": False},
    '36': {"name": "CLIPPERTON I.", "deleted": False},
    '37': {"name": "COCOS I.", "deleted": False},
    '38': {"name": "COCOS (KEELING) IS.", "deleted": False},
    '39': {"name": "COMOROS", "deleted": True},
    '40': {"name": "CRETE", "deleted": False},
    '41': {"name": "CROZET I.", "deleted": False},
    '42': {"name": "DAMAO, DIU", "deleted": True},
    '43': {"name": "DESECHEO I.", "deleted": False},
    '44': {"name": "DESROCHES", "deleted": True},
    '45': {"name": "DODECANESE", "deleted": False},
    '46': {"name": "EAST MALAYSIA", "deleted": False},
    '47': {"name": "EASTER I.", "deleted": False},
    '48': {"name": "E. KIRIBATI (LINE IS.)", "deleted": False},
    '49': {"name": "EQUATORIAL GUINEA", "deleted": False},
    '50': {"name": "MEXICO", "deleted": False},
    '51': {"name": "ERITREA", "deleted": False},
    '52': {"name": "ESTONIA", "deleted": False},
    '53': {"name": "ETHIOPIA", "deleted": False},
    '54': {"name": "EUROPEAN RUSSIA", "deleted": False},
    '55': {"name": "FARQUHAR", "deleted": True},
    '56': {"name": "FERNANDO DE NORONHA", "deleted": False},
    '57': {"name": "FRENCH EQUATORIAL AFRICA", "deleted": True},
    '58': {"name": "FRENCH INDO-CHINA", "deleted": True},
    '59': {"name": "FRENCH WEST AFRICA", "deleted": True},
    '60': {"name": "BAHAMAS", "deleted": False},
    '61': {"name": "FRANZ JOSEF LAND", "deleted": False},
    '62': {"name": "BARBADOS", "deleted": False},
    '63': {"name": "FRENCH GUIANA", "deleted": False},
    '64': {"name": "BERMUDA", "deleted": False},
    '65': {"name": "BRITISH VIRGIN IS.", "deleted": False},
    '66': {"name": "BELIZE", "deleted": False},
    '67': {"name": "FRENCH INDIA", "deleted": True},
    '68': {"name": "KUWAIT/SAUDI ARABIA NEUTRAL ZONE", "deleted": True},
    '69': {"name": "CAYMAN IS.", "deleted": False},
    '70': {"name": "CUBA", "deleted": False},
    '71': {"name": "GALAPAGOS IS.", "deleted": False},
    '72': {"name": "DOMINICAN REPUBLIC", "deleted": False},
    '74': {"name": "EL SALVADOR", "deleted": False},
    '75': {"name": "GEORGIA", "deleted": False},
    '76': {"name": "GUATEMALA", "deleted": False},
    '77': {"name": "GRENADA", "deleted": False},
    '78': {"name": "HAITI", "deleted": False},
    '79': {"name": "GUADELOUPE", "deleted": False},
    '80': {"name": "HONDURAS", "deleted": False},
    '81': {"name": "GERMANY", "deleted": True},
    '82': {"name": "JAMAICA", "deleted": False},
    '84': {"name": "MARTINIQUE", "deleted": False},
    '85': {"name": "BONAIRE, CURACAO", "deleted": True},
    '86': {"name": "NICARAGUA", "deleted": False},
    '88': {"name": "PANAMA", "deleted": False},
    '89': {"name": "TURKS & CAICOS IS.", "deleted": False},
    '90': {"name": "TRINIDAD & TOBAGO", "deleted": False},
    '91': {"name": "ARUBA", "deleted": False},
    '93': {"name": "GEYSER REEF", "deleted": True},
    '94': {"name": "ANTIGUA & BARBUDA", "deleted": False},
    '95': {"name": "DOMINICA", "deleted": False},
    '96': {"name": "MONTSERRAT", "deleted": False},
    '97': {"name": "ST. LUCIA", "deleted": False},
    '98': {"name": "ST. VINCENT", "deleted": False},
    '99': {"name": "GLORIOSO IS.", "deleted": False},
    '100': {"name": "ARGENTINA", "deleted": False},
    '101': {"name": "GOA", "deleted": True},
    '102': {"name": "GOLD COAST, TOGOLAND", "deleted": True},
    '103': {"name": "GUAM", "deleted": False},
    '104': {"name": "BOLIVIA", "deleted": False},
    '105': {"name": "GUANTANAMO BAY", "deleted": False},
    '106': {"name": "GUERNSEY", "deleted": False},
    '107': {"name": "GUINEA", "deleted": False},
    '108': {"name": "BRAZIL", "deleted": False},
    '109': {"name": "GUINEA-BISSAU", "deleted": False},
    '110': {"name": "HAWAII", "deleted": False},
    '111': {"name": "HEARD I.", "deleted": False},
    '112': {"name": "CHILE", "deleted": False},
    '113': {"name": "IFNI", "deleted": True},
    '114': {"name": "ISLE OF MAN", "deleted": False},
    '115': {"name": "ITALIAN SOMALILAND", "deleted": True},
    '116': {"name": "COLOMBIA", "deleted": False},
    '117': {"name": "ITU HQ", "deleted": False},
    '118': {"name": "JAN MAYEN", "deleted": False},
    '119': {"name": "JAVA", "deleted": True},
    '120': {"name": "ECUADOR", "deleted": False},
    '122': {"name": "JERSEY", "deleted": False},
    '123': {"name": "JOHNSTON I.", "deleted": False},
    '124': {"name": "JUAN DE NOVA, EUROPA", "deleted": False},
    '125': {"name": "JUAN FERNANDEZ IS.", "deleted": False},
    '126': {"name": "KALININGRAD", "deleted": False},
    '127': {"name": "KAMARAN IS.", "deleted": True},
    '128': {"name": "KARELO-FINNISH REPUBLIC", "deleted": True},
    '129': {"name": "GUYANA", "deleted": False},
    '130': {"name": "KAZAKHSTAN", "deleted": False},
    '131': {"name": "KERGUELEN IS.", "deleted": False},
    '132': {"name": "PARAGUAY", "deleted": False},
    '133': {"name": "KERMADEC IS.", "deleted": False},
    '134': {"name": "KINGMAN REEF", "deleted": True},
    '135': {"name": "KYRGYZSTAN", "deleted": False},
    '136': {"name": "PERU", "deleted": False},
    '137': {"name": "REPUBLIC OF KOREA", "deleted": False},
    '138': {"name": "KURE I.", "deleted": False},
    '139': {"name": "KURIA MURIA I.", "deleted": True},
    '140': {"name": "SURINAME", "deleted": False},
    '141': {"name": "FALKLAND IS.", "deleted": False},
    '142': {"name": "LAKSHADWEEP IS.", "deleted": False},
    '143': {"name": "LAOS", "deleted": False},
    '144': {"name": "URUGUAY", "deleted": False},
    '145': {"name": "LATVIA", "deleted": False},
    '146': {"name": "LITHUANIA", "deleted": False},
    '147': {"name": "LORD HOWE I.", "deleted": False},
    '148': {"name": "VENEZUELA", "deleted": False},
    '149': {"name": "AZORES", "deleted": False},
    '150': {"name": "AUSTRALIA", "deleted": False},
    '151': {"name": "MALYJ VYSOTSKIJ I.", "deleted": True},
    '152': {"name": "MACAO", "deleted": False},
    '153': {"name": "MACQUARIE I.", "deleted": False},
    '154': {"name": "YEMEN ARAB REPUBLIC", "deleted": True},
    '155': {"name": "MALAYA", "deleted": True},
    '157': {"name": "NAURU", "deleted": False},
    '158': {"name": "VANUATU", "deleted": False},
    '159': {"name": "MALDIVES", "deleted": False},
    '160': {"name": "TONGA", "deleted": False},
    '161': {"name": "MALPELO I.", "deleted": False},
    '162': {"name": "NEW CALEDONIA", "deleted": False},
    '163': {"name": "PAPUA NEW GUINEA", "deleted": False},
    '164': {"name": "MANCHURIA", "deleted": True},
    '165': {"name": "MAURITIUS", "deleted": False},
    '166': {"name": "MARIANA IS.", "deleted": False},
    '167': {"name": "MARKET REEF", "deleted": False},
    '168': {"name": "MARSHALL IS.", "deleted": False},
    '169': {"name": "MAYOTTE", "deleted": False},
    '170': {"name": "NEW ZEALAND", "deleted": False},
    '171': {"name": "MELLISH REEF", "deleted": False},
    '172': {"name": "PITCAIRN I.", "deleted": False},
    '173': {"name": "MICRONESIA", "deleted": False},
    '174': {"name": "MIDWAY I.", "deleted": False},
    '175': {"name": "FRENCH POLYNESIA", "deleted": False},
    '176': {"name": "FIJI", "deleted": False},
    '177': {"name": "MINAMI TORISHIMA", "deleted": False},
    '178': {"name": "MINERVA REEF", "deleted": True},
    '179': {"name": "MOLDOVA", "deleted": False},
    '180': {"name": "MOUNT ATHOS", "deleted": False},
    '181': {"name": "MOZAMBIQUE", "deleted": False},
    '182': {"name": "NAVASSA I.", "deleted": False},
    '183': {"name": "NETHERLANDS BORNEO", "deleted": True},
    '184': {"name": "NETHERLANDS NEW GUINEA", "deleted": True},
    '185': {"name": "SOLOMON IS.", "deleted": False},
    '186': {"name": "NEWFOUNDLAND, LABRADOR", "deleted": True},
    '187': {"name": "NIGER", "deleted": False},
    '188': {"name": "NIUE", "deleted": False},
    '189': {"name": "NORFOLK I.", "deleted": False},
    '190': {"name": "SAMOA", "deleted": False},
    '191': {"name": "NORTH COOK IS.", "deleted": False},
    '192': {"name": "OGASAWARA", "deleted": False},
    '193': {"name": "OKINAWA (RYUKYU IS.)", "deleted": True},
    '194': {"name": "OKINO TORI-SHIMA", "deleted": True},
    '195': {"name": "ANNOBON I.", "deleted": False},
    '196': {"name": "PALESTINE", "deleted": True},
    '197': {"name": "PALMYRA & JARVIS IS.", "deleted": False},
    '198': {"name": "PAPUA TERRITORY", "deleted": True},
    '199': {"name": "PETER 1 I.", "deleted": False},
    '200': {"name": "PORTUGUESE TIMOR", "deleted": True},
    '201': {"name": "PRINCE EDWARD & MARION IS.", "deleted": False},
    '202': {"name": "PUERTO RICO", "deleted": False},
    '203': {"name": "ANDORRA", "deleted": False},
    '204': {"name": "REVILLAGIGEDO", "deleted": False},
    '205': {"name": "ASCENSION I.", "deleted": False},
    '206': {"name": "AUSTRIA", "deleted": False},
    '207': {"name": "RODRIGUEZ I.", "deleted": False},
    '208': {"name": "RUANDA-URUNDI", "deleted": True},
    '209': {"name": "BELGIUM", "deleted": False},
    '210': {"name": "SAAR", "deleted": True},
    '211': {"name": "SABLE I.", "deleted": False},
    '212': {"name": "BULGARIA", "deleted": False},
    '213': {"name": "SAINT MARTIN", "deleted": False},
    '214': {"name": "CORSICA", "deleted": False},
    '215': {"name": "CYPRUS", "deleted": False},
    '216': {"name": "SAN ANDRES & PROVIDENCIA", "deleted": False},
    '217': {"name": "SAN FELIX & SAN AMBROSIO", "deleted": False},
    '218': {"name": "CZECHOSLOVAKIA", "deleted": True},
    '219': {"name": "SAO TOME & PRINCIPE", "deleted": False},
    '220': {"name": "SARAWAK", "deleted": True},
    '221': {"name": "DENMARK", "deleted": False},
    '222': {"name": "FAROE IS.", "deleted": False},
    '223': {"name": "ENGLAND", "deleted": False},
    '224': {"name": "FINLAND", "deleted": False},
    '225': {"name": "SARDINIA", "deleted": False},
    '226': {"name": "SAUDI ARABIA/IRAQ NEUTRAL ZONE", "deleted": True},
    '227': {"name": "FRANCE", "deleted": False},
    '228': {"name": "SERRANA BANK & RONCADOR CAY", "deleted": True},
    '229': {"name": "GERMAN DEMOCRATIC REPUBLIC", "deleted": True},
    '230': {"name": "FEDERAL REPUBLIC OF GERMANY", "deleted": False},
    '231': {"name": "SIKKIM", "deleted": True},
    '232': {"name": "SOMALIA", "deleted": False},
    '233': {"name": "GIBRALTAR", "deleted": False},
    '234': {"name": "SOUTH COOK IS.", "deleted": False},
    '235': {"name": "SOUTH GEORGIA I.", "deleted": False},
    '236': {"name": "GREECE", "deleted": False},
    '237': {"name": "GREENLAND", "deleted": False},
    '238': {"name": "SOUTH ORKNEY IS.", "deleted": False},
    '239': {"name": "HUNGARY", "deleted": False},
    '240': {"name": "SOUTH SANDWICH IS.", "deleted": False},
    '241': {"name": "SOUTH SHETLAND IS.", "deleted": False},
    '242': {"name": "ICELAND", "deleted": False},
    '243': {"name": "PEOPLE'S DEMOCRATIC REP. OF YEMEN", "deleted": True},
    '244': {"name": "SOUTHERN SUDAN", "deleted": True},
    '245': {"name": "IRELAND", "deleted": False},
    '246': {"name": "SOVEREIGN MILITARY ORDER OF MALTA", "deleted": False},
    '247': {"name": "SPRATLY IS.", "deleted": False},
    '248': {"name": "ITALY", "deleted": False},
    '249': {"name": "ST. KITTS & NEVIS", "deleted": False},
    '250': {"name": "ST. HELENA", "deleted": False},
    '251': {"name": "LIECHTENSTEIN", "deleted": False},
    '252': {"name": "ST. PAUL I.", "deleted": False},
    '253': {"name": "ST. PETER & ST. PAUL ROCKS", "deleted": False},
    '254': {"name": "LUXEMBOURG", "deleted": False},
    '255': {"name": "ST. MAARTEN, SABA, ST. EUSTATIUS", "deleted": True},
    '256': {"name": "MADEIRA IS.", "deleted": False},
    '257': {"name": "MALTA", "deleted": False},
    '258': {"name": "SUMATRA", "deleted": True},
    '259': {"name": "SVALBARD", "deleted": False},
    '260': {"name": "MONACO", "deleted": False},
    '261': {"name": "SWAN IS.", "deleted": True},
    '262': {"name": "TAJIKISTAN", "deleted": False},
    '263': {"name": "NETHERLANDS", "deleted": False},
    '264': {"name": "TANGIER", "deleted": True},
    '265': {"name": "NORTHERN IRELAND", "deleted": False},
    '266': {"name": "NORWAY", "deleted": False},
    '267': {"name": "TERRITORY OF NEW GUINEA", "deleted": True},
    '268': {"name": "TIBET", "deleted": True},
    '269': {"name": "POLAND", "deleted": False},
    '270': {"name": "TOKELAU IS.", "deleted": False},
    '271': {"name": "TRIESTE", "deleted": True},
    '272': {"name": "PORTUGAL", "deleted": False},
    '273': {"name": "TRINDADE & MARTIM VAZ IS.", "deleted": False},
    '274': {"name": "TRISTAN DA CUNHA & GOUGH I.", "deleted": False},
    '275': {"name": "ROMANIA", "deleted": False},
    '276': {"name": "TROMELIN I.", "deleted": False},
    '277': {"name": "ST. PIERRE & MIQUELON", "deleted": False},
    '278': {"name": "SAN MARINO", "deleted": False},
    '279': {"name": "SCOTLAND", "deleted": False},
    '280': {"name": "TURKMENISTAN", "deleted": False},
    '281': {"name": "SPAIN", "deleted": False},
    '282': {"name": "TUVALU", "deleted": False},
    '283': {"name": "UK SOVEREIGN BASE AREAS ON CYPRUS", "deleted": False},
    '284': {"name": "SWEDEN", "deleted": False},
    '285': {"name": "VIRGIN IS.", "deleted": False},
    '286': {"name": "UGANDA", "deleted": False},
    '287': {"name": "SWITZERLAND", "deleted": False},
    '288': {"name": "UKRAINE", "deleted": False},
    '289': {"name": "UNITED NATIONS HQ", "deleted": False},
    '291': {"name": "UNITED STATES OF AMERICA", "deleted": False},
    '292': {"name": "UZBEKISTAN", "deleted": False},
    '293': {"name": "VIET NAM", "deleted": False},
    '294': {"name": "WALES", "deleted": False},
    '295': {"name": "VATICAN", "deleted": False},
    '296': {"name": "SERBIA", "deleted": False},
    '297': {"name": "WAKE I.", "deleted": False},
    '298': {"name": "WALLIS & FUTUNA IS.", "deleted": False},
    '299': {"name": "WEST MALAYSIA", "deleted": False},
    '301': {"name": "W. KIRIBATI (GILBERT IS. )", "deleted": False},
    '302': {"name": "WESTERN SAHARA", "deleted": False},
    '303': {"name": "WILLIS I.", "deleted": False},
    '304': {"name": "BAHRAIN", "deleted": False},
    '305': {"name": "BANGLADESH", "deleted": False},
    '306': {"name": "BHUTAN", "deleted": False},
    '307': {"name": "ZANZIBAR", "deleted": True},
    '308': {"name": "COSTA RICA", "deleted": False},
    '309': {"name": "MYANMAR", "deleted": False},
    '312': {"name": "CAMBODIA", "deleted": False},
    '315': {"name": "SRI LANKA", "deleted": False},
    '318': {"name": "CHINA", "deleted": False},
    '321': {"name": "HONG KONG", "deleted": False},
    '324': {"name": "INDIA", "deleted": False},
    '327': {"name": "INDONESIA", "deleted": False},
    '330': {"name": "IRAN", "deleted": False},
    '333': {"name": "IRAQ", "deleted": False},
    '336': {"name": "ISRAEL", "deleted": False},
    '339': {"name": "JAPAN", "deleted": False},
    '342': {"name": "JORDAN", "deleted": False},
    '344': {"name": "DEMOCRATIC PEOPLE'S REP. OF KOREA", "deleted": False},
    '345': {"name": "BRUNEI DARUSSALAM", "deleted": False},
    '348': {"name": "KUWAIT", "deleted": False},
    '354': {"name": "LEBANON", "deleted": False},
    '363': {"name": "MONGOLIA", "deleted": False},
    '369': {"name": "NEPAL", "deleted": False},
    '370': {"name": "OMAN", "deleted": False},
    '372': {"name": "PAKISTAN", "deleted": False},
    '375': {"name": "PHILIPPINES", "deleted": False},
    '376': {"name": "QATAR", "deleted": False},
    '378': {"name": "SAUDI ARABIA", "deleted": False},
    '379': {"name": "SEYCHELLES", "deleted": False},
    '381': {"name": "SINGAPORE", "deleted": False},
    '382': {"name": "DJIBOUTI", "deleted": False},
    '384': {"name": "SYRIA", "deleted": False},
    '386': {"name": "TAIWAN", "deleted": False},
    '387': {"name": "THAILAND", "deleted": False},
    '390': {"name": "TURKEY", "deleted": False},
    '391': {"name": "UNITED ARAB EMIRATES", "deleted": False},
    '400': {"name": "ALGERIA", "deleted": False},
    '401': {"name": "ANGOLA", "deleted": False},
    '402': {"name": "BOTSWANA", "deleted": False},
    '404': {"name": "BURUNDI", "deleted": False},
    '406': {"name": "CAMEROON", "deleted": False},
    '408': {"name": "CENTRAL AFRICA", "deleted": False},
    '409': {"name": "CAPE VERDE", "deleted": False},
    '410': {"name": "CHAD", "deleted": False},
    '411': {"name": "COMOROS", "deleted": False},
    '412': {"name": "REPUBLIC OF THE CONGO", "deleted": False},
    '414': {"name": "DEMOCRATIC REPUBLIC OF THE CONGO", "deleted": False},
    '416': {"name": "BENIN", "deleted": False},
    '420': {"name": "GABON", "deleted": False},
    '422': {"name": "THE GAMBIA", "deleted": False},
    '424': {"name": "GHANA", "deleted": False},
    '428': {"name": "COTE D'IVOIRE", "deleted": False},
    '430': {"name": "KENYA", "deleted": False},
    '432': {"name": "LESOTHO", "deleted": False},
    '434': {"name": "LIBERIA", "deleted": False},
    '436': {"name": "LIBYA", "deleted": False},
    '438': {"name": "MADAGASCAR", "deleted": False},
    '440': {"name": "MALAWI", "deleted": False},
    '442': {"name": "MALI", "deleted": False},
    '444': {"name": "MAURITANIA", "deleted": False},
    '446': {"name": "MOROCCO", "deleted": False},
    '450': {"name": "NIGERIA", "deleted": False},
    '452': {"name": "ZIMBABWE", "deleted": False},
    '453': {"name": "REUNION I.", "deleted": False},
    '454': {"name": "RWANDA", "deleted": False},
    '456': {"name": "SENEGAL", "deleted": False},
    '458': {"name": "SIERRA LEONE", "deleted": False},
    '460': {"name": "ROTUMA I.", "deleted": False},
    '462': {"name": "SOUTH AFRICA", "deleted": False},
    '464': {"name": "NAMIBIA", "deleted": False},
    '466': {"name": "SUDAN", "deleted": False},
    '468': {"name": "SWAZILAND", "deleted": False},
    '470': {"name": "TANZANIA", "deleted": False},
    '474': {"name": "TUNISIA", "deleted": False},
    '478': {"name": "EGYPT", "deleted": False},
    '480': {"name": "BURKINA FASO", "deleted": False},
    '482': {"name": "ZAMBIA", "deleted": False},
    '483': {"name": "TOGO", "deleted": False},
    '488': {"name": "WALVIS BAY", "deleted": True},
    '489': {"name": "CONWAY REEF", "deleted": False},
    '490': {"name": "BANABA I. (OCEAN I.)", "deleted": False},
    '492': {"name": "YEMEN", "deleted": False},
    '493': {"name": "PENGUIN IS.", "deleted": True},
    '497': {"name": "CROATIA", "deleted": False},
    '499': {"name": "SLOVENIA", "deleted": False},
    '501': {"name": "BOSNIA-HERZEGOVINA", "deleted": False},
    '502': {"name": "MACEDONIA", "deleted": False},
    '503': {"name": "CZECH REPUBLIC", "deleted": False},
    '504': {"name": "SLOVAK REPUBLIC", "deleted": False},
    '505': {"name": "PRATAS I.", "deleted": False},
    '506': {"name": "SCARBOROUGH REEF", "deleted": False},
    '507': {"name": "TEMOTU PROVINCE", "deleted": False},
    '508': {"name": "AUSTRAL I.", "deleted": False},
    '509': {"name": "MARQUESAS IS.", "deleted": False},
    '510': {"name": "PALESTINE", "deleted": False},
    '511': {"name": "TIMOR-LESTE", "deleted": False},
    '512': {"name": "CHESTERFIELD IS.", "deleted": False},
    '513': {"name": "DUCIE I.", "deleted": False},
    '514': {"name": "MONTENEGRO", "deleted": False},
    '515': {"name": "SWAINS I.", "deleted": False},
    '516': {"name": "SAINT BARTHELEMY", "deleted": False},
    '517': {"name": "CURACAO", "deleted": False},
    '518': {"name": "ST MAARTEN", "deleted": False},
    '519': {"name": "SABA & ST. EUSTATIUS", "deleted": False},
    '520': {"name": "BONAIRE", "deleted": False},
    '521': {"name": "SOUTH SUDAN (REPUBLIC OF)", "deleted": False},
    '522': {"name": "REPUBLIC OF KOSOVO", "deleted": False},
}

dxcc_1_states = {
    'AB': {'name': 'Alberta', 'cqzones': ['04'], 'ituzones': ['02']},
    'BC': {'name': 'British Columbia', 'cqzones': ['03'], 'ituzones': ['02']},
    'MB': {'name': 'Manitoba', 'cqzones': ['04'], 'ituzones': ['03', '04']},
    'NB': {'name': 'New Brunswick', 'cqzones': ['05'], 'ituzones': ['09']},
    'NL': {'name': 'Newfoundland and Labrador', 'cqzones': ['02', '05'], 'ituzones': ['09']},
    'NS': {'name': 'Nova Scotia', 'cqzones': ['05'], 'ituzones': ['09']},
    'NT': {'name': 'Northwest Territories', 'cqzones': ['01', '02', '04'], 'ituzones': ['03', '04', '75']},
    'NU': {'name': 'Nunavut', 'cqzones': ['02'], 'ituzones': ['04', '09']},
    'ON': {'name': 'Ontario', 'cqzones': ['04'], 'ituzones': ['03', '04']},
    'PE': {'name': 'Prince Edward Island', 'cqzones': ['05'], 'ituzones': ['09']},
    'QC': {'name': 'Québec', 'cqzones': ['02', '05'], 'ituzones': ['04', '09']},
    'SK': {'name': 'Saskatchewan', 'cqzones': ['04'], 'ituzones': ['03']},
    'YT': {'name': 'Yukon', 'cqzones': ['01'], 'ituzones': ['02']},
}

dxcc_291_states = {
    'AL': {'name': 'Alabama', 'cqzones': ['04'], 'ituzones': ['08']},
    'AR': {'name': 'Arkansas', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'AZ': {'name': 'Arizona', 'cqzones': ['03'], 'ituzones': ['06', '07']},
    'CA': {'name': 'California', 'cqzones': ['03'], 'ituzones': ['06']},
    'CO': {'name': 'Colorado', 'cqzones': ['04'], 'ituzones': ['07']},
    'CT': {'name': 'Connecticut', 'cqzones': ['05'], 'ituzones': ['08']},
    'DC': {'name': 'District of Columbia', 'cqzones': ['05'], 'ituzones': ['08']},
    'DE': {'name': 'Delaware', 'cqzones': ['05'], 'ituzones': ['08']},
    'FL': {'name': 'Florida', 'cqzones': ['05'], 'ituzones': ['08']},
    'GA': {'name': 'Georgia', 'cqzones': ['05'], 'ituzones': ['08']},
    'IA': {'name': 'Iowa', 'cqzones': ['04'], 'ituzones': ['07']},
    'ID': {'name': 'Idaho', 'cqzones': ['03'], 'ituzones': ['06']},
    'IL': {'name': 'Illinois', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'IN': {'name': 'Indiana', 'cqzones': ['04'], 'ituzones': ['08']},
    'KS': {'name': 'Kansas', 'cqzones': ['04'], 'ituzones': ['07']},
    'KY': {'name': 'Kentucky', 'cqzones': ['04'], 'ituzones': ['08']},
    'LA': {'name': 'Louisiana', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'MA': {'name': 'Massachusetts', 'cqzones': ['05'], 'ituzones': ['08']},
    'MD': {'name': 'Maryland', 'cqzones': ['05'], 'ituzones': ['08']},
    'ME': {'name': 'Maine', 'cqzones': ['05'], 'ituzones': ['08']},
    'MI': {'name': 'Michigan', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'MN': {'name': 'Minnesota', 'cqzones': ['04'], 'ituzones': ['07']},
    'MO': {'name': 'Missouri', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'MS': {'name': 'Mississippi', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'MT': {'name': 'Montana', 'cqzones': ['04'], 'ituzones': ['06', '07']},
    'NC': {'name': 'North Carolina', 'cqzones': ['04'], 'ituzones': ['08']},
    'ND': {'name': 'North Dakota', 'cqzones': ['04'], 'ituzones': ['07']},
    'NE': {'name': 'Nebraska', 'cqzones': ['04'], 'ituzones': ['07']},
    'NH': {'name': 'New Hampshire', 'cqzones': ['05'], 'ituzones': ['08']},
    'NJ': {'name': 'New Jersey', 'cqzones': ['05'], 'ituzones': ['08']},
    'NM': {'name': 'New Mexico', 'cqzones': ['04'], 'ituzones': ['07']},
    'NV': {'name': 'Nevada', 'cqzones': ['03'], 'ituzones': ['06']},
    'NY': {'name': 'New York', 'cqzones': ['05'], 'ituzones': ['08']},
    'OH': {'name': 'Ohio', 'cqzones': ['04'], 'ituzones': ['08']},
    'OK': {'name': 'Oklahoma', 'cqzones': ['04'], 'ituzones': ['07']},
    'OR': {'name': 'Oregon', 'cqzones': ['03'], 'ituzones': ['06']},
    'PA': {'name': 'Pennsylvania', 'cqzones': ['05'], 'ituzones': ['08']},
    'RI': {'name': 'Rhode Island', 'cqzones': ['05'], 'ituzones': ['08']},
    'SC': {'name': 'South Carolina', 'cqzones': ['05'], 'ituzones': ['08']},
    'SD': {'name': 'South Dakota', 'cqzones': ['04'], 'ituzones': ['07']},
    'TN': {'name': 'Tennessee', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'TX': {'name': 'Texas', 'cqzones': ['04'], 'ituzones': ['07']},
    'UT': {'name': 'Utah', 'cqzones': ['03'], 'ituzones': ['06', '07']},
    'VA': {'name': 'Virginia', 'cqzones': ['05'], 'ituzones': ['08']},
    'VT': {'name': 'Vermont', 'cqzones': ['05'], 'ituzones': ['08']},
    'WA': {'name': 'Washington', 'cqzones': ['03'], 'ituzones': ['06']},
    'WI': {'name': 'Wisconsin', 'cqzones': ['04'], 'ituzones': ['07', '08']},
    'WV': {'name': 'West Virginia', 'cqzones': ['05'], 'ituzones': ['08']},
    'WY': {'name': 'Wyoming', 'cqzones': ['04'], 'ituzones': ['07']},
}


# ARRL sections
# arrl_section_to_state = {
#  'AL': { 'name': 'Alabama',	291
#  'AK': { 'name': 'Alaska',	6
#  'AB': { 'name': 'Alberta',	1
#  'AR': { 'name': 'Arkansas',	291
#  'AZ': { 'name': 'Arizona',	291
#  'BC': { 'name': 'British Columbia',	1
#  'CO': { 'name': 'Colorado',	291
#  'CT': { 'name': 'Connecticut',	291
#  'DE': { 'name': 'Delaware',	291
#  'EB': { 'name': 'East Bay',	291
#  'EMA': { 'name': 'Eastern Massachusetts',	291
#  'ENY': { 'name': 'Eastern New York',	291
#  'EPA': { 'name': 'Eastern Pennsylvania',	291
#  'EWA': { 'name': 'Eastern Washington',	291
#  'GA': { 'name': 'Georgia',	291
#  'GTA': { 'name': 'Greater Toronto Area',	1	2012/09/01
#  'ID': { 'name': 'Idaho',	291
#  'IL': { 'name': 'Illinois',	291
#  'IN': { 'name': 'Indiana',	291
#  'IA': { 'name': 'Iowa',	291
#  'KS': { 'name': 'Kansas',	291
#  'KY': { 'name': 'Kentucky',	291
#  'LAX': { 'name': 'Los Angeles',	291
#  'LA': { 'name': 'Louisiana',	291
#  'ME': { 'name': 'Maine',	1
#  'MB': { 'name': 'Manitoba',	1
#  'MAR': { 'name': 'Maritime',	1
#  'MDC': { 'name': 'Maryland-DC',	291
#  'MI': { 'name': 'Michigan',	291
#  'MN': { 'name': 'Minnesota',	291
#  'MS': { 'name': 'Mississippi',	291
#  'MO': { 'name': 'Missouri',	291
#  'MT': { 'name': 'Montana',	291
#  'NE': { 'name': 'Nebraska',	291
#  'NV': { 'name': 'Nevada',	291
#  'NH': { 'name': 'New Hampshire',	291
#  'NM': { 'name': 'New Mexico',	291
#  'NLI': { 'name': 'New York City-Long Island',	291
#  'NL': { 'name': 'Newfoundland/Labrador',	1
#  'NC': { 'name': 'North Carolina',	291
#  'ND': { 'name': 'North Dakota',	291
#  'NTX': { 'name': 'North Texas',	291
#  'NFL': { 'name': 'Northern Florida',	291
#  'NNJ': { 'name': 'Northern New Jersey',	291
#  'NNY': { 'name': 'Northern New York',	291
#  'NT': { 'name': 'Northwest Territories/Yukon/Nunavut',	1	2003/11/01
#  'NWT': { 'name': 'Northwest Territories/Yukon/Nunavut (replaced by NT)',	1	 	2003/11/01
#  'OH': { 'name': 'Ohio',	291
#  'OK': { 'name': 'Oklahoma',	291
#  'ON': { 'name': 'Ontario(replaced by GTA, ONE, ONN, and ONS)',	1	 	2012/09/01
#  'ONE': { 'name': 'Ontario East',	1	2012/09/01
#  'ONN': { 'name': 'Ontario North',	1	2012/09/01
#  'ONS': { 'name': 'Ontario South',	1	2012/09/01
#  'ORG': { 'name': 'Orange',	291
#  'OR': { 'name': 'Oregon',	291
#  'PAC': { 'name': 'Pacific',	9, 20, 103, 110, 123, 134, 138, 166, 174, 197, 297, 515
#  'PR': { 'name': 'Puerto Rico',	43, 202
#  'QC': { 'name': 'Quebec',	1
#  'RI': { 'name': 'Rhode Island',	291
#  'SV': { 'name': 'Sacramento Valley',	291
#  'SDG': { 'name': 'San Diego',	291
#  'SF': { 'name': 'San Francisco',	291
#  'SJV': { 'name': 'San Joaquin Valley',	291
#  'SB': { 'name': 'Santa Barbara',	291
#  'SCV': { 'name': 'Santa Clara Valley',	291
#  'SK': { 'name': 'Saskatchewan',	1
#  'SC': { 'name': 'South Carolina',	291
#  'SD': { 'name': 'South Dakota',	291
#  'STX': { 'name': 'South Texas',	291
#  'SFL': { 'name': 'Southern Florida',	291
#  'SNJ': { 'name': 'Southern New Jersey',	291
#  'TN': { 'name': 'Tennessee',	291
#  'VI': { 'name': 'US Virgin Islands',	105, 182, 285
#  'UT': { 'name': 'Utah',	291
#  'VT': { 'name': 'Vermont',	291
#  'VA': { 'name': 'Virginia',	291
#  'WCF': { 'name': 'West Central Florida',	291
#  'WTX': { 'name': 'West Texas',	291
#  'WV': { 'name': 'West Virginia',	291
#  'WMA': { 'name': 'Western Massachusetts',	291
#  'WNY': { 'name': 'Western New York',	291
#  'WPA': { 'name': 'Western Pennsylvania',	291
#  'WWA': { 'name': 'Western Washington',	291
#  'WI': { 'name': 'Wisconsin',	291
#  'WY': { 'name': 'Wyoming',	291

# }

# End of enumerations

def triple_play_2019(adif, summary):
    results = {}  # going to stuff scorer results for all the entries here
    valid_modes = ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31']
    valid_dates = [20191109, 20191110, 20191111]
    conditions = {valid_dates, valid_modes}
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif:
        valid_entries, invalid_entries = test_record(entry, valid_dates, summary)
        print(entry, len(adif[entry]))
        print(summary[entry])


def doubleheader_2019(adif, summary):
    results = {}  # going to stuff scorer results for all the entries here
    valid_modes = ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31']
    valid_dates = [20191214, 20191215, 20191216]
    conditions = {valid_dates, valid_modes}
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif:
        if test_record(entry, valid_dates, summary):
            pass
        print(entry, len(adif[entry]))
        print(summary[entry])


def pskfest_2019(adif_files, summary):
    conditions = {'valid_dates': [20190105],
                  'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31'],
                  'valid_bands': ['10m', '15m', '20m', '40m', '80m'],
                  }
    valid_records = []
    invalid_records = []
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif_files:
        for record in adif_files[entry]:
            status, errors = test_record(record, conditions, summary, valid_records)
            if errors:
                invalid_records.append({'data': record, 'errors': errors})
            else:
                valid_records.append(record)
    scores = calc_scores(valid_records)
    return valid_records, invalid_records, scores


def pskfest_2020(adif_files, summary):
    conditions = {'valid_dates': [20200104],
                  'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31'],
                  'valid_bands': ['10m', '15m', '20m', '40m', '80m'],
                  }
    valid_records = []
    invalid_records = []
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif_files:
        for record in adif_files[entry]:
            s_record = synthesize_fields(record)
            status, errors = test_record(s_record, conditions, summary, valid_records)
            if errors:
                invalid_records.append({'data': s_record, 'errors': errors})
            else:
                valid_records.append(s_record)
    scores = calc_scores(valid_records)
    return valid_records, invalid_records, scores


def vdsprint_2019(adif_files, summary):
    return None


def vdsprint_2020(adif_files, summary):
    conditions = {'valid_dates': [20200214],
                  'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31'],
                  'valid_bands': ['40m', '80m', '160m'],
                  }
    valid_records = []
    invalid_records = []
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif_files:
        for record in adif_files[entry]:
            s_record = synthesize_fields(record)
            status, errors = test_record(s_record, conditions, summary, valid_records)
            if errors:
                invalid_records.append({'data': s_record, 'errors': errors})
            else:
                valid_records.append(s_record)
    scores = calc_scores(valid_records)
    return valid_records, invalid_records, scores


def synthesize_fields(record):
    """Method to build synthetic fields for the values we care about if they are
        empty or broken or something else (e.g., build band from freq)"""
    s_record = record

    if 'band' not in record:
        if 'freq' in record:
            s_record['band'] = get_band_from_freq(float(record['freq']['data']))
        else:
            s_record['band'] = {'length': 2, 'data': '??'}
    if 'qso_date' not in record:
        if 'qso_date_off' in record:
            s_record['qso_date'] = record['qso_date_off']
        else:
            s_record['qso_date'] = {'length': 2, 'data': '??'}
    if 'time_on' not in record:
        if 'time_off' in record:
            s_record['time_on'] = record['time_off']
        else:
            s_record['time_on'] = {'length': 2, 'data': '??'}
    if 'state' not in record:
        state = get_state(record)
        if state:
            s_record['state'] = state
    if 'dxcc' not in record:
        dxcc = get_dxcc(record)
        if dxcc:
            s_record['dxcc'] = dxcc
    return s_record


def get_om_yl(record):
    """ look for OM or YL in various places for the Valentine's Sprint"""

    if 'app_n1mm_misctext' in record:
        n1mm_data = re.split('[\W\s]{1}', record['app_n1mm_misctext']['data'])
        for element in n1mm_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'srx_string' in record:
        srx_data = re.split('[\W\s]{1}', record['srx_string']['data'])
        for element in srx_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'srx' in record:
        srx_data = re.split('[\W\s]{1}', record['srx']['data'])
        for element in srx_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'comment' in record:
        comment_data = re.split('[\W\s]{1}', record['comment']['data'])
        for element in comment_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'notes' in record:
        notes_data = re.split('[\W\s]{1}', record['notes']['data'])
        for element in notes_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'name' in record:
        name_data = re.split('[\W\s]{1}', record['name']['data'])
        for element in name_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'other' in record:
        other_data = re.split('[\W\s]{1}', record['other']['data'])
        for element in other_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    if 'award' in record:
        award_data = re.split('[\W\s]{1}', record['award']['data'])
        for element in award_data:
            if element.upper() in ['OM', 'YL']:
                return {'length': len(element), 'data': element.upper()}
    return None


def get_state(record):
    """ Walk a list of increasingly poor options to try and find a value for State"""

    if 've_prov' in record:
        return record['ve_prov']
    if 'app_n1mm_exchange1' in record:
        return record['app_n1mm_exchange1']
    if 'srx_string' in record:
        srx_data = re.split('[\W\s]{1}', record['srx_string']['data'])
        for element in srx_data:
            if element.upper() in dxcc_291_states.keys():
                return {'length': len(element), 'data': element.upper()}
            if element.upper() in dxcc_1_states.keys():
                return {'length': len(element), 'data': element.upper()}
    if 'rst_rcvd' in record:
        rst_data = re.split('[\W\s]{1}', record['rst_rcvd']['data'])
        for element in rst_data:
            if element.upper() in dxcc_291_states.keys():
                return {'length': len(element), 'data': element.upper()}
            if element.upper() in dxcc_1_states.keys():
                return {'length': len(element), 'data': element.upper()}
    if 'srx' in record:
        srx_data = re.split('[\W\s]{1}', record['srx']['data'])
        for element in srx_data:
            if element.upper() in dxcc_291_states.keys():
                return {'length': len(element), 'data': element.upper()}
            if element.upper() in dxcc_1_states.keys():
                return {'length': len(element), 'data': element.upper()}
    if 'qth' in record:
        qth_data = record['qth']['data'].upper()
        if len(qth_data) == 2:
            if qth_data in dxcc_291_states.keys():
                return {'length': len(qth_data), 'data': qth_data}
            if qth_data in dxcc_1_states.keys():
                return {'length': len(qth_data), 'data': qth_data}
        elif len(qth_data) > 2:
            elements = re.split('[,\s]{1}', qth_data)
            for element in elements:
                if element in dxcc_291_states.keys():
                    return {'length': len(element), 'data': element}
                if element in dxcc_1_states.keys():
                    return {'length': len(element), 'data': element}
    if 'section' in record:  # Scraping the bottom of the barrel (section is not the same as State)
        return record['section']
    return None


def get_dxcc(record):
    if 've_prov' in record:
        return {'length': 1, 'data': '1'}
    if 'state' in record:
        if record['state']['data'].upper() in dxcc_1_states.keys():
            return {'length': 1, 'data': '1'}
        elif record['state']['data'].upper() in dxcc_291_states.keys():
            return {'length': 3, 'data': '291'}
    if 'app_n1mm_exchange1' in record:
        if record['app_n1mm_exchange1']['data'].upper() in dxcc_1_states.keys():
            return {'length': 1, 'data': '1'}
        elif record['app_n1mm_exchange1']['data'].upper() in dxcc_291_states.keys():
            return {'length': 3, 'data': '291'}
    if 'srx_string' in record:
        srx_data = re.split('[\W\s]{1}', record['srx_string']['data'])
        for element in srx_data:
            for entity in dxcc_entities:
                if element.upper() == dxcc_entities[entity]['name']:
                    return {'length': len(entity), 'data': entity.upper()}
    if 'country' in record:
        if record['country']['data'].upper() in ['US', 'USA', 'UNITED STATES']:
            return {'length': 3, 'data': '291'}
        for entity in dxcc_entities:
            if record['country']['data'].upper() == dxcc_entities[entity]['name']:
                return {'length': len(entity), 'data': entity.upper()}
    return None


def get_band_from_freq(freq):
    if 1.8 <= freq <= 2.0:
        band = {'length': 4, 'data': '160m'}
    elif 3.5 <= freq <= 4.0:
        band = {'length': 3, 'data': '80m'}
    elif 5.06 <= freq <= 5.45:
        band = {'length': 3, 'data': '60m'}
    elif 7.0 <= freq <= 7.3:
        band = {'length': 3, 'data': '40m'}
    elif 10.1 <= freq <= 10.15:
        band = {'length': 3, 'data': '30m'}
    elif 14.0 <= freq <= 14.35:
        band = {'length': 3, 'data': '20m'}
    elif 18.068 <= freq <= 18.168:
        band = {'length': 3, 'data': '17m'}
    elif 21.0 <= freq <= 21.45:
        band = {'length': 3, 'data': '15m'}
    elif 24.890 <= freq <= 24.99:
        band = {'length': 3, 'data': '12m'}
    elif 28.0 <= freq <= 29.7:
        band = {'length': 3, 'data': '10m'}
    else:
        band = {'length': 2, 'data': '??'}
    return band


def calc_scores(valid_records):
    scores = {}
    scores['q-points'] = len(valid_records)
    scores['mults'] = {}
    scores['mults']['yl'] = 0
    scores['mults']['dxcc'] = {}
    scores['mults']['dxcc']['data'] = []
    scores['mults']['dxcc']['errors'] = []
    scores['mults']['state'] = []
    for rec in valid_records:
        om_yl = get_om_yl(rec)
        try:
            if om_yl['data'] == 'YL':  # VD Sprint Mult
                scores['mults']['yl'] += 1
        except TypeError:
            pass
        except KeyError:
            pass
        try:
            if rec['dxcc']['data'] not in scores['mults']['dxcc']['data']:
                scores['mults']['dxcc']['data'].append(rec['dxcc']['data'])
        except:
            scores['mults']['dxcc']['errors'].append(rec)
        try:
            # For now, assuming only US and Canada for states
            if rec['state']['data'].upper() not in scores['mults']['state'] and \
                    int(rec['dxcc']['data']) in [1, 6, 110, 291]:
                scores['mults']['state'].append(rec['state']['data'].upper())
        except:
            pass
    scores['total'] = (len(scores['mults']['dxcc']['data']) + len(scores['mults']['state'])) * (
                scores['q-points'] + scores['mults']['yl'])
    return scores


def summary_parser(inputfile, delim):
    import csv
    summary = {}
    with open(inputfile, newline='', encoding='utf-16') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delim)
        for row in reader:
            summary[row['callsign']] = row
    return summary


def test_record(entry, conditions, summary, valid_records):
    # Walk through each adif entry and validate against a bunch of stuff

    errors = ['not_valid_band', 'not_in_window', 'is_not_psk', 'is_dupe']

    if rec_in_bands(entry, conditions['valid_bands'], summary):
        errors.remove('not_valid_band')

    if rec_in_window(entry, conditions['valid_dates'], summary):
        errors.remove('not_in_window')

    if rec_is_psk(entry, conditions['valid_modes'], summary):
        errors.remove('is_not_psk')

    if rec_is_not_dupe(entry, valid_records):
        errors.remove('is_dupe')

    if len(errors) == 0:
        return True, None
    else:
        return False, errors


def rec_is_not_dupe(entry, valid_entries):
    # check to see if the same combo already exists in valid_entries
    if len(valid_entries) != 0:
        try:
            check_value = entry['qso_date']['data'] + entry['call']['data'] + entry['band']['data']
        except:
            return False
        for record in valid_entries:
            dupe_check = record['qso_date']['data'] + record['call']['data'] + record['band']['data']
            if check_value.lower() == dupe_check.lower():
                return False
        return True
    else:
        return True


def rec_in_bands(entry, valid_bands, summary):
    # take the adif record and compare against valid
    # dates and times

    try:
        if entry['band']['data'].lower() in valid_bands:
            return True
        else:
            return False
    except:
        return False


def rec_in_window(entry, valid_dates, summary):
    # take the adif record and compare against valid
    # dates and times
    # TODO Need to generalize for multi-windows (eg, TDW)
    # TODO Need to standardize on form field names

    block_start = int(summary['Block start time'])
    block_end = block_start + 600
    if block_end > 2359:
        block_end = 2359
    if entry['time_on']['length'] == 6:
        block_start *= 100
        block_end *= 100

    # print("qso_date: {} valid_dates: {}".format(entry['qso_date']['data'],valid_dates))
    if int(entry['qso_date']['data']) in valid_dates:
        if block_start <= int(entry['time_on']['data']) <= block_end:
            return True
        else:
            return False
    else:
        return False


def rec_is_psk(entry, valid_modes, summary):
    # take the adif record and compare against valid
    # operating modes (ie, PSK)

    if entry['mode']['data'].lower() in valid_modes:
        return True
    else:
        return False


def print_entries(entries, valid=True):
    if valid:
        print('\nValid QSOs')
        print_header(valid=True)
        for rec in entries:
            try:
                call = rec['call']['data'].upper()
            except:
                call = ''
            try:
                qso_date = rec['qso_date']['data']
            except:
                qso_date = ''
            try:
                time_on = rec['time_on']['data']
            except:
                time_on = ''
            try:
                band = rec['band']['data']
            except:
                band = ''
            try:
                srx_string = rec['srx_string']['data']
            except:
                try:
                    srx_string = rec['srx']['data']
                except:
                    try:
                        srx_string = rec['comment']['data']
                    except:
                        try:
                            srx_string = rec['notes']['data']
                        except:
                            try:
                                srx_string = rec['app_n1mm_misctext']['data']
                            except:
                                try:
                                    srx_string = rec['name']['data']
                                except:
                                    try:
                                        srx_string = rec['other']['data']
                                    except:
                                        try:
                                            srx_string = rec['award']['data']
                                        except:
                                            srx_string = ''
            try:
                dxcc = rec['dxcc']['data']
            except:
                dxcc = ''
            try:
                state = rec['state']['data'].upper()
            except:
                state = ''
            try:
                print("{},{},{},{},{},{},{}".format(
                    call,
                    qso_date,
                    time_on,
                    band,
                    srx_string,
                    dxcc,
                    state,
                )
                )
            except KeyError:
                print("KeyError for record", file=sys.stderr)
    else:
        print('\nBroken QSOs (check listed errors)')
        print_header(valid=False)
        for rec in entries:
            try:
                call = rec['data']['call']['data']
            except:
                call = ''
            try:
                qso_date = rec['data']['qso_date']['data']
            except:
                qso_date = ''
            try:
                time_on = rec['data']['time_on']['data']
            except:
                time_on = ''
            try:
                band = rec['data']['band']['data']
            except:
                band = ''
            try:
                srx_string = rec['data']['srx_string']['data']
            except:
                srx_string = ''
            try:
                dxcc = rec['data']['dxcc']['data']
            except:
                dxcc = ''
            try:
                state = rec['data']['state']['data']
            except:
                state = ''

            try:
                print("{},{},{},{},{},{},{},{}".format(
                    call,
                    qso_date,
                    time_on,
                    band,
                    srx_string,
                    dxcc,
                    state,
                    '|'.join(rec['errors']),
                )
                )
            except KeyError:
                print("KeyError for record", file=sys.stderr)


def print_score(scores, summary):
    if summary:  # Report only, spit out CSV of call+score
        callsign = summary['callsign']
        try:
            category = categories[int(summary['category'])]
        except:
            category = 'unknown'
        try:
            podxs_number = summary['070-number']
        except:
            podxs_number = 'unknown'
        try:
            om_yl = summary['Old Man / Young Lady'].upper()
        except:
            om_yl = None
        email = summary['email']
        q_points = scores['q-points']
        dxcc = len(scores['mults']['dxcc']['data'])
        state = len(scores['mults']['state'])
        total = scores['total']

        if om_yl != None:
            yl_count = scores['mults']['yl']
            print('callsign,category,OM/YL,070-number,email,q-points,yl-count,dxcc-mult,state-mult,total')
            print('{},{},{},{},{},{},{},{},{},{}'.format(
                callsign,
                category,
                om_yl,
                podxs_number,
                email,
                q_points,
                yl_count,
                dxcc,
                state,
                total,
            )
            )
        else:
            print('callsign,category,070-number,email,q-points,dxcc-mult,state-mult,total')
            print('{},{},{},{},{},{},{},{}'.format(
                callsign,
                category,
                podxs_number,
                email,
                q_points,
                dxcc,
                state,
                total,
            )
            )
    else:
        if scores['mults']['yl']:
            print('\nQs:{} YL:{} DXCC:{} STATE:{} Total:{}'.format(
                scores['q-points'],
                scores['mults']['yl'],
                len(scores['mults']['dxcc']['data']),
                len(scores['mults']['state']),
                scores['total']
            )
            )
        else:
            print('\nQs:{} DXCC:{} STATE:{} Total:{}'.format(
                scores['q-points'],
                len(scores['mults']['dxcc']['data']),
                len(scores['mults']['state']),
                scores['total']
            )
            )
        if scores['mults']['dxcc']['errors']:
            for error in scores['mults']['dxcc']['errors']:
                print('DXCC ERRORS: {},{},{}'.format(
                    error['call']['data'],
                    error['qso_date']['data'],
                    error['time_on']['data'],
                )
                )


def print_header(valid=True):
    if valid:
        print("\ncall,qso_date,time_on,band,srx_string,dxcc,state")
    else:
        print("\ncall,qso_date,time_on,band,srx_string,dxcc,state,errors")


def print_title_block(summary):
    try:
        category = categories[int(summary['category'])]
    except:
        category = 'unknown'
    try:
        podxs_number = summary['070-number']
    except:
        podxs_number = 'unknown'
    try:
        om_yl = summary['Old Man / Young Lady'].upper()
    except:
        om_yl = None

    if om_yl is None:
        print('\nCALL:{}\nPOWER:{}\nEMAIL:{}\n'.format(
            summary['callsign'],
            category,
            summary['email'],
        )
        )
    else:
        print('\nCALL:{}\nPOWER:{}\nCATEGORY:{}\nSTART TIME:{}\nEMAIL:{}\n'.format(
            summary['callsign'],
            category,
            om_yl,
            summary['Block start time'],
            summary['email'],
        )
        )


if __name__ == '__main__':
    import adifparser
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description='Contests Checker')
    parser.add_argument('--contest', metavar='CONTEST')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    args = parser.parse_args()

    summary = summary_parser(args.summary)
    adif_records = {}
    for adif in args.adif:
        name, ext = adif.split('.')
        adif_records[name] = adifparser.parse(adif)
    pprint.pprint(adif_records)
    # pprint.pprint(summary)
    if args.contest == 'tp2019':
        triple_play_2019(adif_records, summary)
    if args.contest == 'dh2019':
        doubleheader_2019(adif_records, summary)
