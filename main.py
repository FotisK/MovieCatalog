"""
needs:

pip3 & python3
also: 
beautifulsoup4     4.7.1   


pip3 install parse-torrent-name #(PTN)
pip3 install Jinja2 
pip3 install imdbpy
pip3 install google #(googlesearch)
pip3 install Pillow

not to forget that python is buggy without setting locale:
nano ~/.bash_profile (new file) add:
	export LANG=en_US.UTF-8
	export LC_ALL=en_US.UTF-8
save!

pip3 install requests
pipenv install parse-torrent-name --pre --skip-lock
pipenv install requests --pre --skip-lock
pipenv install jinja2 --pre --skip-lock
pipenv install google --pre --skip-lock
pipenv install imdbpy --pre --skip-lock
pipenv install Pillow --pre --skip-lock


updating imdbpy:
pipenv run pip3 install git+https://github.com/alberanid/imdbpy
"""

import io
import pickle
from random import *
import sys
import getopt
import pprint
import os
import string
import PTN
import re
import requests
import bs4
import json
from jinja2 import Environment, FileSystemLoader
import shutil
import datetime
import time
from urllib.parse import urlparse, parse_qs, unquote, quote_plus
import urllib.error
import googlesearch
from imdb import IMDb
from imdb.Person import Person
import imdb
import imdb.utils
import copy
import base64
import collections
from PIL import Image


def CountryNameByCode(name):
    # countries list from stackoverflow: https://stackoverflow.com/questions/16253060/how-to-convert-country-names-to-iso-3166-1-alpha-2-values-using-python
    countries = {
        "AF": "Afghanistan",
        "AL": "Albania",
        "DZ": "Algeria",
        "AS": "American Samoa",
        "AD": "Andorra",
        "AO": "Angola",
        "AI": "Anguilla",
        "AQ": "Antarctica",
        "AG": "Antigua and Barbuda",
        "AR": "Argentina",
        "AM": "Armenia",
        "AW": "Aruba",
        "AU": "Australia",
        "AT": "Austria",
        "AZ": "Azerbaijan",
        "BS": "Bahamas",
        "BH": "Bahrain",
        "BD": "Bangladesh",
        "BB": "Barbados",
        "BY": "Belarus",
        "BE": "Belgium",
        "BZ": "Belize",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BT": "Bhutan",
        "BO": "Bolivia, Plurinational State of",
        "BQ": "Bonaire, Sint Eustatius and Saba",
        "BA": "Bosnia and Herzegovina",
        "BW": "Botswana",
        "BV": "Bouvet Island",
        "BR": "Brazil",
        "IO": "British Indian Ocean Territory",
        "BN": "Brunei Darussalam",
        "BG": "Bulgaria",
        "BF": "Burkina Faso",
        "BI": "Burundi",
        "KH": "Cambodia",
        "CM": "Cameroon",
        "CA": "Canada",
        "CV": "Cape Verde",
        "KY": "Cayman Islands",
        "CF": "Central African Republic",
        "TD": "Chad",
        "CL": "Chile",
        "CN": "China",
        "CX": "Christmas Island",
        "CC": "Cocos (Keeling) Islands",
        "CO": "Colombia",
        "KM": "Comoros",
        "CG": "Congo",
        "CD": "Congo, the Democratic Republic of the",
        "CK": "Cook Islands",
        "CR": "Costa Rica",
        "Code": "Country name",
        "HR": "Croatia",
        "CU": "Cuba",
        "CW": "Curaçao",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "Côte d'Ivoire": "CI",
        "DK": "Denmark",
        "DJ": "Djibouti",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EN": "England",
        "EL": "Greece",
        "EG": "Egypt",
        "SV": "El Salvador",
        "GQ": "Equatorial Guinea",
        "ER": "Eritrea",
        "EE": "Estonia",
        "ET": "Ethiopia",
        "FK": "Falkland Islands (Malvinas)",
        "FO": "Faroe Islands",
        "FJ": "Fiji",
        "FI": "Finland",
        "FR": "France",
        "GF": "French Guiana",
        "PF": "French Polynesia",
        "TF": "French Southern Territories",
        "GA": "Gabon",
        "GM": "Gambia",
        "GE": "Georgia",
        "DE": "Germany",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GR": "Greece",
        "GL": "Greenland",
        "GD": "Grenada",
        "GP": "Guadeloupe",
        "GU": "Guam",
        "GT": "Guatemala",
        "GG": "Guernsey",
        "GN": "Guinea",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HT": "Haiti",
        "HM": "Heard Island and McDonald Islands",
        "VA": "Holy See (Vatican City State)",
        "HN": "Honduras",
        "HK": "Hong Kong",
        "HU": "Hungary",
        "uk": "United Kingdom",
        "IS": "Iceland",
        "IN": "India",
        "ID": "Indonesia",
        "IR": "Iran, Islamic Republic of",
        "IQ": "Iraq",
        "IE": "Ireland",
        "IM": "Isle of Man",
        "IL": "Israel",
        "IT": "Italy",
        "JM": "Jamaica",
        "JP": "Japan",
        "JE": "Jersey",
        "JO": "Jordan",
        "KZ": "Kazakhstan",
        "KE": "Kenya",
        "KI": "Kiribati",
        "Korea, Democratic People's Republic of": "KP",
        "KR": "Korea, Republic of",
        "KW": "Kuwait",
        "KG": "Kyrgyzstan",
        "Lao People's Democratic Republic": "LA",
        "LV": "Latvia",
        "LB": "Lebanon",
        "LS": "Lesotho",
        "LR": "Liberia",
        "LY": "Libya",
        "LI": "Liechtenstein",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "MO": "Macao",
        "MK": "Macedonia, the former Yugoslav Republic of",
        "MG": "Madagascar",
        "MW": "Malawi",
        "MY": "Malaysia",
        "MV": "Maldives",
        "ML": "Mali",
        "MT": "Malta",
        "MH": "Marshall Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MU": "Mauritius",
        "YT": "Mayotte",
        "MX": "Mexico",
        "FM": "Micronesia, Federated States of",
        "MD": "Moldova, Republic of",
        "MC": "Monaco",
        "MN": "Mongolia",
        "ME": "Montenegro",
        "MS": "Montserrat",
        "MA": "Morocco",
        "MZ": "Mozambique",
        "MM": "Myanmar",
        "NA": "Namibia",
        "NR": "Nauru",
        "NP": "Nepal",
        "NL": "Netherlands",
        "NC": "New Caledonia",
        "NZ": "New Zealand",
        "NI": "Nicaragua",
        "NE": "Niger",
        "NG": "Nigeria",
        "NU": "Niue",
        "NF": "Norfolk Island",
        "MP": "Northern Mariana Islands",
        "NO": "Norway",
        "OM": "Oman",
        "PK": "Pakistan",
        "PW": "Palau",
        "PS": "Palestine, State of",
        "PA": "Panama",
        "PG": "Papua New Guinea",
        "PY": "Paraguay",
        "PE": "Peru",
        "PH": "Philippines",
        "PN": "Pitcairn",
        "PL": "Poland",
        "PT": "Portugal",
        "PR": "Puerto Rico",
        "QA": "Qatar",
        "RO": "Romania",
        "RU": "Russian Federation",
        "RW": "Rwanda",
        "RE": "Réunion",
        "BL": "Saint Barthélemy",
        "SH": "Saint Helena, Ascension and Tristan da Cunha",
        "KN": "Saint Kitts and Nevis",
        "LC": "Saint Lucia",
        "MF": "Saint Martin (French part)",
        "PM": "Saint Pierre and Miquelon",
        "VC": "Saint Vincent and the Grenadines",
        "WS": "Samoa",
        "SM": "San Marino",
        "ST": "Sao Tome and Principe",
        "SA": "Saudi Arabia",
        "SN": "Senegal",
        "RS": "Serbia",
        "SC": "Seychelles",
        "SL": "Sierra Leone",
        "SG": "Singapore",
        "SX": "Sint Maarten (Dutch part)",
        "SK": "Slovakia",
        "SI": "Slovenia",
        "SB": "Solomon Islands",
        "SO": "Somalia",
        "ZA": "South Africa",
        "GS": "South Georgia and the South Sandwich Islands",
        "SS": "South Sudan",
        "ES": "Spain",
        "LK": "Sri Lanka",
        "SD": "Sudan",
        "SR": "Suriname",
        "SJ": "Svalbard and Jan Mayen",
        "SZ": "Swaziland",
        "SE": "Sweden",
        "CH": "Switzerland",
        "SY": "Syrian Arab Republic",
        "TW": "Taiwan, Province of China",
        "TJ": "Tajikistan",
        "TZ": "Tanzania, United Republic of",
        "TH": "Thailand",
        "TL": "Timor-Leste",
        "TG": "Togo",
        "TK": "Tokelau",
        "TO": "Tonga",
        "TT": "Trinidad and Tobago",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TM": "Turkmenistan",
        "TC": "Turks and Caicos Islands",
        "TV": "Tuvalu",
        "UG": "Uganda",
        "UA": "Ukraine",
        "AE": "United Arab Emirates",
        "GB": "Great Britain",
        "US": "United States",
        "UM": "United States Minor Outlying Islands",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VU": "Vanuatu",
        "VE": "Venezuela, Bolivarian Republic of",
        "VN": "Viet Nam",
        "VG": "Virgin Islands, British",
        "VI": "Virgin Islands, U.S.",
        "WF": "Wallis and Futuna",
        "EH": "Western Sahara",
        "YE": "Yemen",
        "ZM": "Zambia",
        "ZW": "Zimbabwe",
        "Åland Islands": "AX",
    }
    if name.upper() in countries:
        return countries[name.upper()]
    else:
        return name


def LanguageNameByCode(name):
    # languages list from stackoverflow: https://gist.github.com/alexanderjulo/4073388
    languages = {
        "aa": "Afar",
        "ab": "Abkhazian",
        "af": "Afrikaans",
        "ak": "Akan",
        "sq": "Albanian",
        "am": "Amharic",
        "ar": "Arabic",
        "an": "Aragonese",
        "hy": "Armenian",
        "as": "Assamese",
        "av": "Avaric",
        "ae": "Avestan",
        "ay": "Aymara",
        "az": "Azerbaijani",
        "ba": "Bashkir",
        "bm": "Bambara",
        "eu": "Basque",
        "be": "Belarusian",
        "bn": "Bengali",
        "bh": "Bihari languages",
        "bi": "Bislama",
        "bo": "Tibetan",
        "bs": "Bosnian",
        "br": "Breton",
        "bg": "Bulgarian",
        "my": "Burmese",
        "ca": "Catalan; Valencian",
        "cs": "Czech",
        "ch": "Chamorro",
        "ce": "Chechen",
        "zh": "Chinese",
        "cu": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic",
        "cv": "Chuvash",
        "kw": "Cornish",
        "co": "Corsican",
        "cr": "Cree",
        "cy": "Welsh",
        "cs": "Czech",
        "da": "Danish",
        "de": "German",
        "dv": "Divehi; Dhivehi; Maldivian",
        "nl": "Dutch; Flemish",
        "dz": "Dzongkha",
        "el": "Greek, Modern (1453-)",
        "en": "English",
        "eo": "Esperanto",
        "et": "Estonian",
        "eu": "Basque",
        "ee": "Ewe",
        "fo": "Faroese",
        "fa": "Persian",
        "fj": "Fijian",
        "fi": "Finnish",
        "fr": "French",
        "fr": "French",
        "fy": "Western Frisian",
        "ff": "Fulah",
        "Ga": "Georgian",
        "de": "German",
        "gd": "Gaelic; Scottish Gaelic",
        "ga": "Irish",
        "gl": "Galician",
        "gv": "Manx",
        "el": "Greek, Modern (1453-)",
        "gn": "Guarani",
        "gu": "Gujarati",
        "ht": "Haitian; Haitian Creole",
        "ha": "Hausa",
        "he": "Hebrew",
        "hz": "Herero",
        "hi": "Hindi",
        "ho": "Hiri Motu",
        "hr": "Croatian",
        "hu": "Hungarian",
        "hy": "Armenian",
        "ig": "Igbo",
        "is": "Icelandic",
        "io": "Ido",
        "ii": "Sichuan Yi; Nuosu",
        "iu": "Inuktitut",
        "ie": "Interlingue; Occidental",
        "ia": "Interlingua (International Auxiliary Language Association)",
        "id": "Indonesian",
        "ik": "Inupiaq",
        "is": "Icelandic",
        "it": "Italian",
        "jv": "Javanese",
        "ja": "Japanese",
        "kl": "Kalaallisut; Greenlandic",
        "kn": "Kannada",
        "ks": "Kashmiri",
        "ka": "Georgian",
        "kr": "Kanuri",
        "kk": "Kazakh",
        "km": "Central Khmer",
        "ki": "Kikuyu; Gikuyu",
        "rw": "Kinyarwanda",
        "ky": "Kirghiz; Kyrgyz",
        "kv": "Komi",
        "kg": "Kongo",
        "ko": "Korean",
        "kj": "Kuanyama; Kwanyama",
        "ku": "Kurdish",
        "lo": "Lao",
        "la": "Latin",
        "lv": "Latvian",
        "li": "Limburgan; Limburger; Limburgish",
        "ln": "Lingala",
        "lt": "Lithuanian",
        "lb": "Luxembourgish; Letzeburgesch",
        "lu": "Luba-Katanga",
        "lg": "Ganda",
        "mk": "Macedonian",
        "mh": "Marshallese",
        "ml": "Malayalam",
        "mi": "Maori",
        "mr": "Marathi",
        "ms": "Malay",
        "Mi": "Micmac",
        "mk": "Macedonian",
        "mg": "Malagasy",
        "mt": "Maltese",
        "mn": "Mongolian",
        "mi": "Maori",
        "ms": "Malay",
        "my": "Burmese",
        "na": "Nauru",
        "nv": "Navajo; Navaho",
        "nr": "Ndebele, South; South Ndebele",
        "nd": "Ndebele, North; North Ndebele",
        "ng": "Ndonga",
        "ne": "Nepali",
        "nl": "Dutch; Flemish",
        "nn": "Norwegian Nynorsk; Nynorsk, Norwegian",
        "nb": "Bokmål, Norwegian; Norwegian Bokmål",
        "no": "Norwegian",
        "oc": "Occitan (post 1500)",
        "oj": "Ojibwa",
        "or": "Oriya",
        "om": "Oromo",
        "os": "Ossetian; Ossetic",
        "pa": "Panjabi; Punjabi",
        "fa": "Persian",
        "pi": "Pali",
        "pl": "Polish",
        "pt": "Portuguese",
        "ps": "Pushto; Pashto",
        "qu": "Quechua",
        "rm": "Romansh",
        "ro": "Romanian; Moldavian; Moldovan",
        "ro": "Romanian; Moldavian; Moldovan",
        "rn": "Rundi",
        "ru": "Russian",
        "sg": "Sango",
        "sa": "Sanskrit",
        "si": "Sinhala; Sinhalese",
        "sk": "Slovak",
        "sk": "Slovak",
        "sl": "Slovenian",
        "se": "Northern Sami",
        "sm": "Samoan",
        "sn": "Shona",
        "sd": "Sindhi",
        "so": "Somali",
        "st": "Sotho, Southern",
        "es": "Spanish; Castilian",
        "sq": "Albanian",
        "sc": "Sardinian",
        "sr": "Serbian",
        "ss": "Swati",
        "su": "Sundanese",
        "sw": "Swahili",
        "sv": "Swedish",
        "ty": "Tahitian",
        "ta": "Tamil",
        "tt": "Tatar",
        "te": "Telugu",
        "tg": "Tajik",
        "tl": "Tagalog",
        "th": "Thai",
        "bo": "Tibetan",
        "ti": "Tigrinya",
        "to": "Tonga (Tonga Islands)",
        "tn": "Tswana",
        "ts": "Tsonga",
        "tk": "Turkmen",
        "tr": "Turkish",
        "tw": "Twi",
        "ug": "Uighur; Uyghur",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "uz": "Uzbek",
        "ve": "Venda",
        "vi": "Vietnamese",
        "vo": "Volapük",
        "cy": "Welsh",
        "wa": "Walloon",
        "wo": "Wolof",
        "xh": "Xhosa",
        "yi": "Yiddish",
        "yo": "Yoruba",
        "za": "Zhuang; Chuang",
        "zh": "Chinese",
        "zu": "Zulu",
    }
    if name.lower() in languages:
        return languages[name.lower()]
    else:
        return name


def selectiveMerge(a, b):
    # Intelligently merge TMDB(a) and IMDB data(b):
    # assumptions: IMDB data is more compete, and accurate. However some information can be found only on TMDB - eg. adult
    # take unique infor from TMDB
    # also for People in particular (directors etc), merge data:
    # if a person category is found only in TMDB (eg. show creators, art directors) then take the category as is
    # if it exists on both or only IMDB, take IMDB data and selectively for the people that exist on both sites (with identical name)
    # import missing info from TMDB (eg. portrait, character name, billing order etc)

    # - Top level items:
    c = {}
    for ak, av in a.items():
        if ak in b:
            # +if a.has_non_empty_item and b.has_non_empty_item, prefer +b & children
            if b.get(ak):
                c[ak] = b[ak]
            else:
                c[ak] = av
            if type(av) is list:
                # +if is person(director,writer etc)
                if ak in [
                    "CreatedBy",
                    "Directors",
                    "Writers",
                    "Producers",
                    "Cinematographers",
                    "ArtDirectors",
                    "Cast",
                ]:
                    # if a.child.name == b.child.name == non_empty then
                    for a_index, person in enumerate(av):
                        b_index = find(b[ak], "Name", person["Name"])
                        if b_index >= 0:  # found inside b!
                            # so there is something matching: get all elements from matchin b element, unless ones unique to a
                            tmpItem = b[ak][b_index]
                            # + take exta fields from a (TMDBID,PortraitURL,Order,Character)
                            if av[a_index].get("TMDBID"):
                                tmpItem["TMDBID"] = av[a_index].get("TMDBID")
                            if av[a_index].get("PortraitURL"):
                                if av[a_index]["PortraitURL"] is not None:
                                    tmpItem["PortraitURL"] = av[a_index].get(
                                        "PortraitURL"
                                    )
                                else:
                                    print(
                                        "Bug, Shouldn't be none, should had already been filtered out"
                                    )
                            if "Order" in av[a_index]:
                                tmpItem["Order"] = av[a_index].get("Order")
                            if av[a_index].get("Character"):
                                tmpItem["Character"] = av[a_index].get("Character")
                            c_index = find(c[ak], "Name", person["Name"])
                            c[ak][c_index] = tmpItem
                        else:  # not found inside b, unique in a - in that case, ignore completely, a (TMDB) is not the accurate one!
                            #
                            #   !!!!!!!!!!!! this will have to change if at some point I get rid of IMDB.
                            #
                            pass
                else:
                    # +if is language: do nothing (retain b)
                    # +if is countries: do nothing (retain b)
                    # +if is language: do nothing (retain b)
                    # +if is keywords: do nothing (retain b)
                    # + same for taglines - what else have i forgotten? hmm...
                    pass
        else:
            # +unique, non-empty items from a, should be copied +a?
            c[ak] = av
    for bk, bv in b.items():
        # +unique, non-empty items from b, should be copied +b?
        if not bk in a:
            # 3. items unique to b? copy them to a!
            c[bk] = bv
    return c


def update(d, u):
    #
    # By Alex Martelli
    # https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    # (some people say there is some bug in it)
    #
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def find(lst, key, value):
    # find index within list of dictionaries, by searching for a specific key's value
    # https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def PreCleanUpFileName(Filename):
    tmpRegex = re.compile(r"\+")
    Result = tmpRegex.sub(r" ", Filename)
    return Result


def PostCleanUpFileName(Filename):
    tmpRegex = re.compile(r"([sS]\d+)|(\.)|(\[.*\])")
    Result = tmpRegex.sub(r" ", Filename)
    return Result


def StripExtension(Filename):
    if includeFoldersInValidFileTypes and Filename.endswith(os.sep):
        Filename = os.path.normpath(Filename)
        if not Filename.endswith(".ffiles"):
            return Filename
    # else it's either .ffile directory or real file with (assumed) extension
    Result = os.path.splitext(Filename)[0]
    return Result


def ExtractExtension(Filename):
    # BUGGY 197239012
    Result = os.path.splitext(Filename)[1]
    return Result


def GetMovieDirectory(BaseDir, MovieName):
    if MovieName != "":
        NewDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        if os.path.exists(NewDirectory):
            return NewDirectory
    return None


def doesFileExist(BaseDir, MovieName, FileName):
    if MovieName != "" and BaseDir != "" and FileName != "":
        Directory = os.path.join(BaseDir, MovieName + ".ffiles")
        File = os.path.join(Directory, FileName)
        if os.path.exists(File):
            return True
        else:
            return False
    else:
        print(
            "Bug, testing for existence of file, without setting file, folder or moviename - why?"
        )
        return False


def isValidMovieFile(BaseDir, MovieNameWithExtension):
    FileURI = os.path.join(os.getcwd(), BaseDir, MovieNameWithExtension)
    if os.path.isdir(FileURI):
        if includeFoldersInValidFileTypes and not MovieNameWithExtension.endswith(
            ".ffiles"
        ):
            return True  # is folder, and not a cache folder. Assume it's a movie!
        else:
            return (
                False
            )  # is cache folder or we don't care about folders (in case where you have same cache and source folders)
    else:
        # StrippedMovieName = StripExtension(MovieNameWithExtension)
        StrippedExtension = ExtractExtension(MovieNameWithExtension)
        if StrippedExtension.lower() in ValidFileTypes:
            return True
        else:
            return False


def MakeDirectory(BaseDir, MovieName, dotExtension=".ffiles"):
    if BaseDir != "":
        NewDirectory = os.path.join(BaseDir, MovieName + dotExtension)
        if not os.path.exists(NewDirectory):
            os.makedirs(NewDirectory)
    return None


def ReplaceWSwithPlus(StringToReplace):
    # replace whitespace( ) with plus(+)
    tmpRegex = re.compile(r"\s")
    Result = tmpRegex.sub(r"\+", StringToReplace)
    return Result


def RemoveAuthorFromPlot(StringToReplace):
    # replace whitespace( ) with plus(+)
    Result = ""
    if StringToReplace:
        tmpRegex = re.compile(r"(.*)::.*$")
        Result = tmpRegex.sub(r"\1", StringToReplace)
    return Result


def ConvertCountryCodeToName(Countries):
    if Countries:
        for index in range(len(Countries)):
            Country = Countries[index]
            if len(Country) == 2:
                Countries[index] = CountryNameByCode(Country)
        return Countries


def ConvertLanguageCodeToName(Languages):
    if Languages:
        for index in range(len(Languages)):
            Lang = Languages[index]
            if len(Lang) == 2:
                Languages[index] = LanguageNameByCode(Lang)
        return Languages


def isIMDBURL(URLString):
    # if this String an IMDB movie url?
    extractedID = ExtractIDfromIMDBURL(URLString)
    if extractedID > 0:
        return True
    else:
        return False


def ExtractIDfromIMDBURL(IMDBurl):
    # extract the numbered movie ID from the imdb url
    # https://www.imdb.com/title/tt6628102/
    tmpRegex = re.compile(r"imdb\.com.*\/tt([0-9]*).*$")
    extractedID = tmpRegex.search(IMDBurl)
    # print("url_raw:" + str(IMDBurl))
    # print("movieID_raw:" + str(extractedID))
    if extractedID == None:
        return -1
    else:
        # print("movieID:" + str(extractedID.group(1)) )
        return int(extractedID.group(1))


def ParseDuckDuckGoSearchResults(PageText):
    # pprint.pprint("PAGE --------------------:\n" + PageText)
    tmpSoup = bs4.BeautifulSoup(PageText, features="html.parser")
    tmpResults = tmpSoup.select("#links > div.result .result__a")
    try:
        tmpFirstResult = tmpResults[0]
    except:
        print(
            "bug, DuckDuckGo did not return results for query,"
            "page's HTML probably has changed, need to adjust"
        )
        return "Error"  # error
    link = tmpFirstResult.get("href")
    print(link)
    url_obj = urlparse(link)
    parsed_url = parse_qs(url_obj.query).get("uddg", "")
    if parsed_url:
        movieID = ExtractIDfromIMDBURL(unquote(parsed_url[0]))
        # print(unquote(parsed_url[0]))
        # pprint.pprint(link)
        return movieID
    else:
        return -1


def FetchGoogleSearchResults(MovieSearchString):
    MovieID = None
    try:
        for GGLurl in googlesearch.search(MovieSearchString, stop=20):
            if isIMDBURL(GGLurl):
                MovieID = ExtractIDfromIMDBURL(GGLurl)
                # print("ID is "+str(MovieID)+" ("+GGLurl+")")
                return MovieID
    except urllib.error.URLError:
        print("Could not connect to Google - Perhaps you are offline?")
    return -1  # -1: no ID found, perhaps not a movie?


def FetchDuckDuckGoSearchResults(MovieSearchString):
    ConvertedMovieName = ReplaceWSwithPlus(MovieSearchString)
    # print("encoded name:"+quote_plus(MovieSearchString))
    DDGurl = (
        "https://duckduckgo.com/html/?q=imdb+"
        + quote_plus(MovieSearchString)
        + "&sites=www.imdb.com"
        + "&kp=-2&norw=1"
    )
    print("requesting url:" + DDGurl)
    tmpreqresp = requests.get(DDGurl)
    # tmpreqresp.raise_for_status()
    if tmpreqresp.status_code != requests.codes.ok:
        print("duckduckgo did not return correctly")
        MovieID = -1
    else:
        MovieID = ParseDuckDuckGoSearchResults(tmpreqresp.text)
    if MovieID > 0:
        # print("found")
        return MovieID
    else:
        # print("Not found")
        return -1


def GetMovieIDfromWeb(MovieName, Year="", AdditionalInfo="", Provider="google"):
    # https://duckduckgo.com/?q=imdb+QUERY&kp=-2
    # kp=-2 safesearching OFF
    # provider service "google" or "duckduckgo"
    SearchQuery = MovieName + " " + str(Year) + " " + AdditionalInfo
    if Provider == "google":
        MovieID = FetchGoogleSearchResults(SearchQuery)
        # pprint.pprint(tmpreqresp)
    elif Provider == "duckduckgo":
        MovieID = FetchDuckDuckGoSearchResults(SearchQuery)
    if MovieID > 0:
        # print("found")
        return MovieID
    else:
        # print("Not found")
        return -1


def isMissingDataFile(BaseDir, MovieName):
    # if is a new Movie File or moviedata is missing, return True (for refetch etc)
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MovieDataFile = os.path.join(MovieDirectory, "moviedata.json")
        if not os.path.exists(MovieDirectory):
            return True  # new movie data is missing!
        elif os.path.exists(MovieDataFile):
            return False  # Datafile exists
        else:
            return True  # missing datafile but folder exists! possibly corrupt
    return None


def isMissingFolder(BaseDir, MovieName):
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        if not os.path.exists(MovieDirectory):
            return True  # yes, it's missing the poster file!
        else:
            return False  # no, the file exists


def isMissingPosterFile(BaseDir, MovieName):
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MoviePosterFile = os.path.join(MovieDirectory, "poster.jpg")
        if not os.path.exists(MoviePosterFile):
            return True  # yes, it's missing the poster file!
        else:
            return False  # no, the file exists


def isMissingBackdropFile(BaseDir, MovieName):
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MovieBackdropFile = os.path.join(MovieDirectory, "backdrop.jpg")
        if not os.path.exists(MovieBackdropFile):
            return True  # yes, it's missing the backdrop file!
        else:
            return False  # no, the file exists


def isFolderOrphan(SourceFilesList, CacheDir, StrippedMovieName):
    if StrippedMovieName != "" and len(SourceFilesList) > 0:
        # StrippedMovieName = StripExtension(MovieNameWithExtension)
        # MovieDirectory = os.path.join(CacheDir,StrippedMovieName+".ffiles")
        # MovieFile = os.path.join(SourceDir,StrippedMovieName)
        # MovieDataFile = os.path.join(MovieDirectory,"moviedata.json")
        GeneratedNameVariants = {StrippedMovieName + fn for fn in ValidFileTypes}
        if includeFoldersInValidFileTypes:
            GeneratedNameVariants.add(
                StrippedMovieName + os.sep
            )  # FUTURE192938: for folder testing, also create a variant with trailing /
            # assumes that if the file ends in / or \ depending on the OS, it was a directory.
            # reason? because I embedded "/" at the end of folders so that I can tell them apart.
        Common = GeneratedNameVariants.intersection(SourceFilesList)
        if len(Common) == 0:
            return True  # yes, it's an orphan!
        else:
            return False  # no, folder has paired Movie file - no orphan here


def DeleteFolder(BaseDir, MovieName):
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        if os.path.exists(MovieDirectory):
            shutil.rmtree(MovieDirectory)
            # print("mock del: [" + MovieDirectory+"]")
            return None
        else:
            print("Bug! Deleting non-existent folder. Why?")
            return None


def BuildGenresList(MoviesCatalog):
    tmpGenresList = []
    for Movie in MoviesCatalog:
        # print(Movie['DateAdded'])
        if "Genres" in Movie:
            tmpGenresList += Movie["Genres"]
    tmpGenresList = list(set(tmpGenresList))
    tmpGenresList.sort()
    return tmpGenresList


def BuildIndex(MoviesCatalog):
    file_loader = FileSystemLoader(TemplatesRelativePath)
    env = Environment(loader=file_loader)
    GenresList = BuildGenresList(MoviesCatalog)
    template = env.get_template("index.htmltemplate")
    output = template.render(
        genres=GenresList,
        foundmovies=True,
        movies=MoviesCatalog,
        CachePath=CacheRelativePath,
        HowManyActorsShouldDisplay=constHowManyActorsShouldDisplay,
    )
    indexfile = open("index.html", "w")
    indexfile.write(output)
    indexfile.close
    return None


def CreateMovieDataFile(BaseDir, MovieName, MovieData, ForceRebuild=False):
    # create data file for movie
    # print(MovieName)
    # print(len(MovieData))
    # print(BaseDir)
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MovieDataFile = os.path.join(MovieDirectory, "moviedata.json")
        if not os.path.exists(MovieDirectory):
            MakeDirectory(BaseDir, MovieName)
        if os.path.exists(MovieDataFile):
            if ForceRebuild == False:
                # complain, why does overwritting happen?
                print("bug: overwritting movie data, why?")
            os.remove(MovieDataFile)
        # with open(MovieDataFile, 'w') as JSONFile:
        # 	json.dump(MovieData, JSONFile)
        with io.open(MovieDataFile, "w", encoding="utf8") as json_file:
            json.dump(MovieData, json_file, ensure_ascii=False)
        return True
    return False


def GenerateGalleryThumbnail(
    BaseDir,
    MovieName,
    input_file="poster.jpg",
    output_file="poster_thumbnail.jpg",
    basewidth=256,
):
    return GenerateResizedImage(BaseDir, MovieName, input_file, output_file, basewidth)


def GenerateResizedImage(BaseDir, MovieName, input_file, output_file, basewidth):
    if input_file == None or output_file == None or basewidth < 1:
        print("Bug, forgot to set filenames, and basewidth")
        return -1
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        ImageInputFile = os.path.join(MovieDirectory, input_file)
        if os.path.exists(ImageInputFile):
            ImageOutputFile = os.path.join(MovieDirectory, output_file)
            img = Image.open(ImageInputFile)
            wpercent = basewidth / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(ImageOutputFile)
            return 1
        else:
            print("Bug, Generating Thumbnail for non-existent file?")
            return -1


def UpdateMovieDataFile(BaseDir, MovieName, MovieData):
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MovieDataFile = os.path.join(MovieDirectory, "moviedata.json")

        if os.path.exists(MovieDataFile):
            os.rename(MovieDataFile, MovieDataFile + ".bak")
            with io.open(MovieDataFile, "w", encoding="utf8") as json_file:
                json.dump(MovieData, json_file, ensure_ascii=False)
        else:
            print("bug: reading non-existent file, yet you asked for update! why?")
            return None
    return None


def RestoreMovieDataFile(BaseDir, MovieName, ignore_not_found=False):
    # returns movie data object as read by the file
    if MovieName != "":
        MovieDirectory = os.path.join(BaseDir, MovieName + ".ffiles")
        MovieDataFile = os.path.join(MovieDirectory, "moviedata.json")
        if os.path.exists(MovieDataFile):
            # with open(MovieDataFile) as JSONFile:
            # 	MovieData = json.load(JSONFile)#.decode('unicode-escape')
            with io.open(MovieDataFile, "r", encoding="utf8") as json_file:
                MovieData = json.load(json_file)
                return MovieData
        else:
            if not ignore_not_found:
                print("bug: reading non-existent file and wasn't suppressed, why?")
            return None
    return None


def GetHeadshotURL(personID, Condition=True, Provider="tmdb"):
    if (
        Condition == False
    ):  # should I fetch data? condition eg. if counter < 7, do! else --> stop fetching
        # print("reached condition - not displaying person "+ personID)
        return None
    if Provider == "imdb":
        tmpPerson = ia.get_person(personID)
    elif Provider == "tmdb":
        # print("mock fetch")
        # print(type(personID))
        tmpResults = getTMDBDetailsfromIMDBID(personID, "person")
        # print("+")
        if tmpResults:

            tmpPerson = {
                "full-size headshot": tmpResults["profile_path"],
                "name": tmpResults["name"],
                "id": personID,
            }
        else:
            tmpPerson = {}
            # print("no-results! for person "+personID)
    # print("/")
    # print(Person.default_info)
    # print(ia.get_person_infoset())
    # print(tmpPerson.current_info)
    # pprint.pprint(tmpPerson)
    # print(type(tmpPerson))
    # for key in tmpPerson.keys():
    # 	print("key is ["+key+"]")
    # print("-")
    if "full-size headshot" in tmpPerson.keys():
        tmpImageURL = ConstructTMDBImageURL(tmpPerson["full-size headshot"], "original")
        if tmpImageURL:
            if re.match(r"^https?://.*\.jpg$", tmpImageURL):
                # print(tmpPerson['name'])
                # print(tmpPerson['full-size headshot'])
                return tmpImageURL
            else:
                print(
                    "Error - found headshot for "
                    + tmpPerson["name"]
                    + " but format is not URL but ["
                    + tmpPerson["full-size headshot"]
                    + "]"
                )
    return None
    # tmpPerson['ImdbID'] = tmpDirector['personid']


def WrapTMDBDataInIMDB(IMDBMovieID):
    if IMDBMovieID == None:
        print("Bug, why try fetching TMDBData if movie wasn't found?")
        return
    MovieInformation = {}
    tmpData = getTMDBIDfromIMDBID(IMDBMovieID, "movie")
    movieID = None
    kind = None
    # HANDLE NO DATA BUG 91239
    if tmpData and "id" in tmpData:
        movieID = tmpData.get("id")
    if tmpData and "kind" in tmpData:
        kind = tmpData.get("kind")
    if not (kind == "movie" or kind == "tv"):
        print("Bug, getTMDBIDfromIMDBID returned wrong kind of data, perhaps no movie?")
        # HANDLE NO DATA BUG 91239
        return
    # https://api.themoviedb.org/3/movie/109443?api_key=096187be7a5391bfa9843173e059137d
    # &language=en-US&append_to_response
    # =external_ids,keywords,credits,videos,images&include_image_language=null,en,fr,jp,cn,de,es,it
    # print("Fetching TMDB Data for "+ str(IMDBMovieID))

    requestURL = (
        "https://api.themoviedb.org/3/"
        + kind
        + "/"
        + str(movieID)
        + "?api_key="
        + myTMDB_APIkey
        + "&language=en-US&append_to_response"
        + "=external_ids,alternative_titles,keywords,credits,videos,images&include_image_language=null,en,fr,jp,cn,de,es,it"
    )
    response = requests.get(requestURL)
    # for tmpkey in response.headers.keys():
    # 	print(tmpkey+":["+response.headers[tmpkey]+"]")

    # 	print(response.headers['X-RateLimit-Limit'])
    response.raise_for_status()

    if response.status_code == requests.codes.ok:
        current_time = time.time()
        if "X-RateLimit-Remaining" in response.headers and int(response.headers["X-RateLimit-Remaining"]) <= 1:
            while int(response.headers["X-RateLimit-Reset"]) + 1 > time.time():
                print("TMDB:Reached rate-limit. Waiting...")
                time.sleep(1)
        tmpJSON = json.loads(response.text)
    # for key in tmpJSON.keys():
    # 	print("- "+ key)
    # 	print(tmpJSON.get(key))
    MovieInformation["ImdbID"] = IMDBMovieID
    MovieInformation["TMDBID"] = movieID
    if "title" in tmpJSON:
        MovieInformation["Title"] = tmpJSON.get("title")
    MovieInformation["OtherTitles"] = []
    if "original_title" in tmpJSON:
        MovieInformation["OriginalTitle"] = tmpJSON.get("original_title")
        MovieInformation["OtherTitles"].append(
            tmpJSON.get("original_title") + " (original)"
        )
    if "original_name" in tmpJSON:
        MovieInformation["OriginalTitle"] = tmpJSON.get("original_name")
        MovieInformation["OtherTitles"].append(
            tmpJSON.get("original_name") + " (original)"
        )
    if "alternative_titles" in tmpJSON:
        if "alternative_titles" in tmpJSON:
            tmpTag = None
            if "titles" in tmpJSON["alternative_titles"]:
                tmpTag = "titles"
            if "results" in tmpJSON["alternative_titles"]:
                tmpTag = "results"
            # pprint.pprint(tmpJSON.get('alternative_titles'))
            for tmpD in tmpJSON["alternative_titles"][tmpTag]:
                title_type = tmpD.get("type")
                title_iso = tmpD.get("iso_3166_1")
                title_par = ""
                if title_type or title_iso:
                    title_par = " ("
                    if title_type:
                        title_par += title_type
                    if title_iso:
                        title_par += " " + title_iso
                    title_par += ")"

                MovieInformation["OtherTitles"].append(tmpD.get("title") + title_par)

    if "tagline" in tmpJSON:
        MovieInformation["Taglines"] = []
        MovieInformation["Taglines"].append(tmpJSON.get("tagline"))

    # Kind: movie or tv? needs to be extracted earlier in the process

    if "release_date" in tmpJSON:
        MovieInformation["ReleaseYear"] = tmpJSON.get("release_date")[:4]
    MovieInformation["Languages"] = []
    if "spoken_languages" in tmpJSON:
        for tmpD in tmpJSON.get("spoken_languages"):
            MovieInformation["Languages"].append(tmpD["iso_639_1"])
    if "original_language" in tmpJSON:
        MovieInformation["Languages"].append(tmpJSON["original_language"])
    MovieInformation["Countries"] = []
    if "production_countries" in tmpJSON:
        for tmpD in tmpJSON.get("production_countries"):
            MovieInformation["Countries"].append(tmpD["iso_3166_1"])
    if "original_country" in tmpJSON:
        MovieInformation["Countries"].append(tmpJSON["original_country"])
    # Metascore: not available for TMDB
    # MetacriticURL: not available for TMDB

    if "runtime" in tmpJSON:
        MovieInformation["Duration"] = tmpJSON.get("runtime")
    if "genres" in tmpJSON:
        MovieInformation["Genres"] = []
        for tmpD in tmpJSON.get("genres"):
            MovieInformation["Genres"].append(tmpD["name"].lower())
    if "overview" in tmpJSON:
        MovieInformation["Synopsis"] = tmpJSON.get("overview")

    # Plot: TMDB has only overview - no "plot outline", nor user "plot"s
    if "created_by" in tmpJSON:
        MovieInformation["CreatedBy"] = []
        for tmpD in tmpJSON.get("created_by"):
            tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
            if tmpD.get("profile_path") is not None:
                tmp["PortraitURL"] = tmpD.get("profile_path")
            MovieInformation["CreatedBy"].append(tmp)
    if "credits" in tmpJSON:
        if "crew" in tmpJSON["credits"]:
            MovieInformation["Directors"] = []
            MovieInformation["Writers"] = []
            MovieInformation["Producers"] = []
            MovieInformation["Cinematographers"] = []
            MovieInformation["ArtDirectors"] = []
            for tmpD in tmpJSON["credits"].get("crew"):
                if tmpD.get("job") == "Director":
                    tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                    if tmpD.get("profile_path") is not None:
                        tmp["PortraitURL"] = tmpD.get("profile_path")
                    MovieInformation["Directors"].append(tmp)
                if (
                    tmpD.get("job") == "Screenplay"
                    or tmpD.get("job") == "Writer"
                    or tmpD.get("job") == "Author"
                ):
                    tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                    if tmpD.get("profile_path") is not None:
                        tmp["PortraitURL"] = tmpD.get("profile_path")
                    MovieInformation["Writers"].append(tmp)
                if tmpD.get("job") == "Producer":
                    tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                    if tmpD.get("profile_path") is not None:
                        tmp["PortraitURL"] = tmpD.get("profile_path")
                    MovieInformation["Producers"].append(tmp)
                if tmpD.get("job") == "Art Direction":
                    tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                    if tmpD.get("profile_path") is not None:
                        tmp["PortraitURL"] = tmpD.get("profile_path")
                    MovieInformation["ArtDirectors"].append(tmp)
                if (
                    tmpD.get("job") == "Cinematography"
                    or tmpD.get("job") == "Director of Photography"
                ):
                    tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                    if tmpD.get("profile_path") is not None:
                        tmp["PortraitURL"] = tmpD.get("profile_path")
                    MovieInformation["Cinematographers"].append(tmp)
        if "cast" in tmpJSON["credits"]:
            MovieInformation["Cast"] = []
            for tmpD in tmpJSON["credits"].get("cast"):
                tmp = {"Name": tmpD.get("name"), "TMDBID": tmpD.get("id")}
                if tmpD.get("profile_path") is not None:
                    tmp["PortraitURL"] = tmpD.get("profile_path")
                if "order" in tmpD:
                    tmp["Order"] = tmpD.get("order")
                if tmpD.get("character") is not None:
                    tmp["Character"] = tmpD.get("character")
                MovieInformation["Cast"].append(tmp)
    if "keywords" in tmpJSON and "keywords" in tmpJSON["keywords"]:
        MovieInformation["Keywords"] = []
        for tmpD in tmpJSON["keywords"].get("keywords"):
            tmpStr = tmpD["name"].strip().replace(" ", "-")
            MovieInformation["Keywords"].append(tmpStr)
    if "videos" in tmpJSON and "results" in tmpJSON["videos"]:
        for tmpD in tmpJSON["videos"].get("results"):
            if tmpD["iso_639_1"] == "en" or not MovieInformation["TrailerID"]:
                if (
                    tmpD["site"] == "YouTube"
                    and tmpD["type"] == "Trailer"
                    and len(tmpD["key"]) > 8
                ):  # should be 11, but arbirarily I asked 8 minimun :-p
                    MovieInformation["TrailerID"] = tmpD["key"]
    if "backdrop_path" in tmpJSON:
        MovieInformation["TMDBBackdrop"] = tmpJSON.get("backdrop_path")
    if "poster_path" in tmpJSON:
        MovieInformation["TMDBPoster"] = tmpJSON.get("poster_path")
    if "budget" in tmpJSON:
        MovieInformation["TMDBBudget"] = tmpJSON.get("budget")
    MovieInformation["Images"] = []
    if "images" in tmpJSON and "backdrops" in tmpJSON["images"]:
        for tmpD in tmpJSON["images"]["backdrops"]:
            MovieInformation["Images"].append(tmpD.get("file_path"))
    if "images" in tmpJSON and "posters" in tmpJSON["images"]:
        for tmpD in tmpJSON["images"]["posters"]:
            MovieInformation["Images"].append(tmpD.get("file_path"))

    # tmpMovieDictionary['Poster'] obsolete - I wasn't using this particular one anyways (I'd take the one from TMDB)
    # tmpMovieDictionary['ImdbRating'] - IMDB specific
    # tmpMovieDictionary['ImdbVotes'] - IMDB specific
    # tmpMovieDictionary['ImdbVoteDistribution'] - IMDB specific
    # tmpMovieDictionary['ImdbVoteDemographics'] - IMDB specific
    # 'RottenTomatoesRating'
    # 'RottenTomatoesVotes'

    if "popularity" in tmpJSON:
        MovieInformation["TMDBPopularity"] = tmpJSON.get("popularity")
    if "adult" in tmpJSON:
        MovieInformation["Adult"] = tmpJSON.get("adult")
    if "vote_count" in tmpJSON:
        MovieInformation["TMDBVotes"] = tmpJSON.get("vote_count")
    if "vote_average" in tmpJSON:
        MovieInformation["TMDBRating"] = tmpJSON.get("vote_average")

    # pprint.pprint(MovieInformation)
    return MovieInformation


def FetchMovieDataIMDBLite(MovieID, getPeople=False):
    #
    # 	fetch only basic movie data, so that you can complement the
    # 	data from TMDB - FetchMovieData does thes oposite: fetches most
    # 	data from IMDB and only minimal from TMDB. In case you want to fetch
    # 	people data (directors, actors etc) choose this option - this is for
    # 	movies that couldn't be found in TMDB so you can not get the ORDERED
    # 	cast list from there.
    #
    try:
        movieData = ia.get_movie(str(MovieID))  # interstellar 0816692
        ia.update(
            movieData, info=["keywords", "vote details", "taglines", "critic reviews"]
        )
    except IMDbError as e:
        print(e)
    tmpMovieDictionary = {}
    tmpMovieDictionary.clear()
    # for key in movieData.keys():
    # 	print("---------"+key+"-----------")
    # 	pprint.pprint(movieData[key])

    # from movie 'main' information_set
    tmpMovieDictionary["Title"] = movieData.get("title")
    tmpMovieDictionary["OtherTitles"] = []
    if "akas" in movieData:
        tmpMovieDictionary["OtherTitles"] = copy.copy(movieData.get("akas"))
    if "taglines" in movieData:
        tmpMovieDictionary["Taglines"] = copy.copy(movieData.get("taglines"))
    tmpMovieDictionary["Kind"] = movieData.get("kind")
    tmpMovieDictionary["ReleaseYear"] = movieData.get("year")
    tmpMovieDictionary["Languages"] = movieData.get("languages")
    tmpMovieDictionary["Countries"] = movieData.get("countries")
    if "metascore" in movieData:
        tmpMovieDictionary["Metascore"] = copy.copy(movieData.get("metascore"))
    if "metacritic url" in movieData:
        tmpMovieDictionary["MetacriticUrl"] = copy.copy(movieData.get("metacritic url"))
    if "runtimes" in movieData:
        tmpMovieDictionary["Duration"] = int(
            movieData.get("runtimes")[0]
        )  # is it list?
    tmpMovieDictionary["Genres"] = movieData.get("genres").copy()
    if "plot outline" in movieData:
        tmpMovieDictionary["Synopsis"] = movieData.get("plot outline")
    if movieData.get("plot")[0]:
        tmpMovieDictionary["Plot"] = movieData.get("plot")[0]
    if "keywords" in movieData:
        tmpMovieDictionary["Keywords"] = copy.copy(movieData.get("keywords"))
    tmpMovieDictionary["ImdbID"] = MovieID
    if "rating" in movieData:
        tmpMovieDictionary["ImdbRating"] = movieData.get("rating")
    if "votes" in movieData:
        tmpMovieDictionary["ImdbVotes"] = movieData.get("votes")
    if "number of votes" in movieData:
        tmpMovieDictionary["ImdbVoteDistribution"] = copy.copy(
            movieData.get("number of votes")
        )
    if "demographics" in movieData:
        tmpMovieDictionary["ImdbVoteDemographics"] = copy.deepcopy(
            movieData.get("demographics")
        )

    tmpMovieDictionary["Directors"] = []
    if "directors" in movieData:
        for tmpDirector in movieData.get("directors"):
            if tmpDirector:
                tmpPerson = {
                    "Name": tmpDirector["name"],
                    "ImdbID": tmpDirector.personID,
                }
            tmpMovieDictionary["Directors"].append(tmpPerson)
    tmpMovieDictionary["Producers"] = []
    if "producers" in movieData:
        for tmpProducer in movieData.get("producers"):
            if tmpProducer:
                tmpPerson = {
                    "Name": tmpProducer["name"],
                    "ImdbID": tmpProducer.personID,
                }
                tmpMovieDictionary["Producers"].append(tmpPerson)
    tmpMovieDictionary["Writers"] = []
    if "writers" in movieData:
        for tmpWriter in movieData.get("writers"):
            if tmpWriter:
                tmpPerson = {"Name": tmpWriter["name"], "ImdbID": tmpWriter.personID}
                tmpMovieDictionary["Writers"].append(tmpPerson)
    tmpMovieDictionary["Cinematographers"] = []
    if "cinematographers" in movieData:
        for tmpCinematographer in movieData.get("cinematographers"):
            if tmpCinematographer:
                tmpPerson = {
                    "Name": tmpCinematographer["name"],
                    "ImdbID": tmpCinematographer.personID,
                }
                tmpMovieDictionary["Cinematographers"].append(tmpPerson)
    if getPeople == True:
        tmpMovieDictionary["Cast"] = []
        if "cast" in movieData:
            for tmpCast in movieData.get("cast"):
                if tmpCast:
                    tmpPerson = {"Name": tmpCast["name"], "ImdbID": tmpCast.personID}
                    tmpMovieDictionary["Cast"].append(tmpPerson)
    return tmpMovieDictionary


def ConstructIMDBIDfromNumber(movieID, idtype="movie"):
    # takes 190590 and returns IMDB format of: tt0190590
    if type(movieID) == int:
        if idtype == "movie":
            # print("mp!")
            return "tt{:07d}".format(movieID)
        elif idtype == "person":
            # print("ip!")
            return "nm{:10d}".format(movieID)
    elif type(movieID) == str:
        if idtype == "movie":
            # print("ms!")
            return "tt" + movieID
        elif idtype == "person":
            # print("is!")
            return "nm" + movieID
    print(
        "Bug - ConstructIMDBIDfromNumber shouldn't ever reach here. Movie/Person ID is:"
    )
    print(movieID)
    print(type(movieID))
    return None


def ConstructTMDBImageURL(ImageName, ImageWidth="w780"):
    # https://image.tmdb.org/t/p/w780/xu9zaAevzQ5nnrsXN6JcahLnG4i.jpg
    # 780/1280/original
    if ImageName and ImageWidth:
        tmpURL = "https://image.tmdb.org/t/p/" + ImageWidth + ImageName
        return tmpURL
    return None


def getTMDBTrailerLink(TMDBmovieID, Kind="movie"):
    # https://api.themoviedb.org/3/find/tt0816692?api_key=096187be7a5391bfa9843173e059137d&language=en-US&external_source=imdb_id
    FoundTrailer = None
    if Kind != "tv":
        Kind = "movie"
    requestURL = (
        "https://api.themoviedb.org/3/"
        + Kind
        + "/"
        + str(TMDBmovieID)
        + "/videos?api_key="
        + myTMDB_APIkey
        + "&language=en-US"
    )
    response = requests.get(requestURL)
    # response.raise_for_status()
    # print("1")
    if response.status_code == requests.codes.ok:
        tmpJSON = json.loads(response.text)
        # print("2")
        # pprint.pprint(tmpJSON)
        if tmpJSON["results"]:
            # print("3")
            # pprint.pprint(tmpJSON['results'])
            # TrailerIndex = next((index for (index, d) in enumerate(lst) if d["type"].lower() == "trailer"), None)
            # TrailerIndex = find(tmpJSON['results'],"type","Trailer")
            # print(TrailerIndex)
            # FoundTrailer = tmpJSON['results'][TrailerIndex]
            for tmpVideoFileResult in tmpJSON["results"]:
                # print("4")
                # pprint.pprint(tmpVideoFileResult)
                if (
                    tmpVideoFileResult["site"] == "YouTube"
                    and tmpVideoFileResult["type"] == "Trailer"
                    and len(tmpVideoFileResult["key"]) == 11
                ):
                    # print("5")
                    FoundTrailer = tmpVideoFileResult["key"]
                    # print("found: " +FoundTrailer )
                    return FoundTrailer
                else:
                    return None
    return FoundTrailer


def getTMDBDetailsfromIMDBID(movieID, idtype="movie"):
    # https://api.themoviedb.org/3/find/tt0816692?api_key=096187be7a5391bfa9843173e059137d&language=en-US&external_source=imdb_id
    requestURL = (
        "https://api.themoviedb.org/3/find/"
        + ConstructIMDBIDfromNumber(movieID, idtype)
        + "?api_key="
        + myTMDB_APIkey
        + "&language=en-US&external_source=imdb_id"
    )
    response = requests.get(requestURL)
    response.raise_for_status()
    if response.status_code == requests.codes.ok:
        tmpJSON = json.loads(response.text)

    if idtype == "movie" or idtype == "tv":
        if tmpJSON[idtype + "_results"]:
            # print(idtype + '_results')
            # if tmpJSON[0][idtype + '_results']['vote_average']:
            tmpJSON[idtype + "_results"][0]["TMDBRating"] = tmpJSON[
                idtype + "_results"
            ][0]["vote_average"]
            # if tmpJSON[0][idtype + '_results']['vote_count']:
            tmpJSON[idtype + "_results"][0]["TMDBVotes"] = tmpJSON[idtype + "_results"][
                0
            ]["vote_count"]
            # if tmpJSON[0][idtype + '_results']['vote_average']:
            tmpJSON[idtype + "_results"][0]["TMDBAdult"] = tmpJSON[idtype + "_results"][
                0
            ]["adult"]
            tmpJSON[idtype + "_results"][0]["TMDBPopularity"] = tmpJSON[
                idtype + "_results"
            ][0]["popularity"]
            tmpJSON[idtype + "_results"][0]["Kind"] = idtype
            # pprint.pprint(tmpJSON['movie_results'][0])
            return tmpJSON[idtype + "_results"][0]
    if idtype == "person":
        if tmpJSON["person_results"]:
            tmpJSON["person_results"][0]["Kind"] = "person"
            return tmpJSON["person_results"][0]


def getTMDBIDfromIMDBID(movieID, idtype="movie"):
    # https://api.themoviedb.org/3/find/tt0816692?api_key=096187be7a5391bfa9843173e059137d&language=en-US&external_source=imdb_id
    requestURL = (
        "https://api.themoviedb.org/3/find/"
        + ConstructIMDBIDfromNumber(movieID, idtype)
        + "?api_key="
        + myTMDB_APIkey
        + "&language=en-US&external_source=imdb_id"
    )
    response = requests.get(requestURL)
    response.raise_for_status()
    if response.status_code == requests.codes.ok:
        tmpJSON = json.loads(response.text)
    if idtype == "person":
        if tmpJSON["movie_results"]:  # and len(tmpJSON['movie_results'])>0:
            return {"id": tmpJSON["person_results"][0]["id"], "kind": "person"}
    if idtype == "movie":
        if tmpJSON["movie_results"]:  # and len(tmpJSON['movie_results'])>0:
            return {"id": tmpJSON["movie_results"][0]["id"], "kind": "movie"}
        if tmpJSON["tv_results"]:  # and len(tmpJSON['tv_results'])>0:
            return {"id": tmpJSON["tv_results"][0]["id"], "kind": "tv"}
    return None


def is_downloadable(url):
    """
    Does the url contain a downloadable resource?
    by https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get("content-type")
    if "text" in content_type.lower():
        return False
    if "html" in content_type.lower():
        return False
    return True


def getImageDataFromURL(url):
    r = requests.get(url, allow_redirects=True)
    return r.content


def WriteDataToFile(Data, FileURI, Overwrite=False):
    if FileURI:
        if os.path.exists(FileURI) and Overwrite == False:
            raise FileExistsError(
                "Bug, file writen to already exists and overwrite is set to False"
            )
        tmpFile = open(FileURI, "wb")
        tmpFile.write(Data)
        tmpFile.close()
    else:
        raise ValueError("Bug, attempting to write file without filename set properly")


def test_movie_keywords_should_be_a_list_of_keywords(ia):
    movie = ia.get_movie("0133093", info=["keywords"])  # Matrix
    keywords = movie.get("keywords", [])
    print("here!")
    print(keywords)
    assert 250 <= len(keywords) <= 400
    assert {"computer-hacker", "messiah", "artificial-reality"}.issubset(set(keywords))


def BuildLaunchOptions(argv):
    LaunchOptions = {
        "ListItems": False,
        "DisplayedItemsStatus": [
            "Ambiguous",
            "Verified",
            "Unverified",
            "Unimported",
            "Incomplete",
        ],
        "Filename": None,
        "ImdbID": None,
        "UpdateFile": False,
        "UpdateFileWithID": False,
        "UpdateFileWithStatus": False,
        "NewStatus": None,
        "ScanFolder": False,
    }
    try:
        opts, args = getopt.getopt(
            argv,
            "?hl:sd:f:i:ct:",
            [
                "help",
                "list=",
                "set",
                "display=",
                "file=",
                "imdb=",
                "--change",
                "--status=",
            ],
        )
    except getopt.GetoptError:
        print("Invalid syntax use -?, -h, --help: for help")
        sys.exit(2)
    for opt, arg in opts:
        if opt.lower() in ("-h", "-?", "--help"):
            print("-h, --help: displays this help")
            print(
                "-l [all,ambiguous,unimported,verified,incomplete], --list [all,ambiguous,unimported,verified,incomplete]: list all,ambiguous or unimported movies with their IMDB ID"
            )
            print(
                "-c -f <filename> -i <new imdbID> -t [Unimported/Unverified/Verified/Ambiguous/Incomplete], --change --file <filename> --imdb <new imdbID> --status [Unimported/Unverified/Verified/Ambiguous/Incomplete]: match imdbID and/or manually set status for movie with given filename"
            )
            # print('-u -f <filename> -t [Unimported/Unverified/Verified/Ambiguous/Incomplete], --update --file <filename> --status [Unimported/Unverified/Verified/Ambiguous/Incomplete]: manually set the status for the file')
            print(
                "-i <imdbID>, --imdb <imdbID>: displays details for movie with imdb ID"
            )
            print("-s, --scan: scan and update new movies and cleanup orphans")
            # print '-i <filename>, --details <imdbID>: display details for movie with imdb ID'
            # print '-i <movie name>, --import <movie name>: '
            # print '-u <imdbID>, --update <imdbID>:'
            sys.exit()
        elif opt.lower() in ("-l", "--list"):
            if arg.lower() in ("", "all"):
                LaunchOptions["ListItems"] = True
            elif arg.lower() in ("ambiguous"):
                LaunchOptions["ListItems"] = True
                LaunchOptions["DisplayedItemsStatus"] = ["Ambiguous"]
            elif arg.lower() in ("unimported"):
                LaunchOptions["ListItems"] = True
                LaunchOptions["DisplayedItemsStatus"] = ["Unimported"]
            elif arg.lower() in ("verified"):
                LaunchOptions["ListItems"] = True
                LaunchOptions["DisplayedItemsStatus"] = ["Verified"]
            elif arg.lower() in ("incomplete"):
                LaunchOptions["ListItems"] = True
                LaunchOptions["DisplayedItemsStatus"] = ["Incomplete"]
            else:
                print(
                    "invalid list argument --list should be all/ambiguous/unimported/verified/incomplete"
                )
                sys.exit()
        elif opt.lower() in ("-c", "--change"):
            LaunchOptions["UpdateFile"] = True
        elif opt.lower() in ("-f", "--file"):
            if arg:
                LaunchOptions["Filename"] = arg
            else:
                print("Invalid Syntax: missing filename")
                sys.exit()
        elif opt.lower() in ("-i", "--imdb"):
            if re.match(r"^[0-9]{7}$", arg):
                LaunchOptions["ImdbID"] = int(arg)
            else:
                print("Invalid Imdb ID: should be a 7 digit number")
                sys.exit()
        elif opt.lower() in ("-t", "--status"):
            if arg.lower() in (
                "ambiguous",
                "unimported",
                "unverified",
                "verified",
                "incomplete",
            ):
                LaunchOptions["NewStatus"] = arg.lower().capitalize()
            else:
                print(
                    "Invalid Status: should be Unimported, Unverified, Verified, Ambiguous or Incomplete"
                )
                sys.exit()
        elif opt.lower() in ("-s", "--scan"):
            LaunchOptions["ScanFolder"] = True

    # 2nd pass: for combined args eg. -c, needs -f and -i
    if LaunchOptions["UpdateFile"]:
        if not LaunchOptions["Filename"]:
            print("invalid syntax for -c,--change: Missing filename")
            print("correct syntax: -c -f filename.ext -i 1234567")
            sys.exit()
        elif not (LaunchOptions["ImdbID"] or LaunchOptions["NewStatus"]):
            print(
                "invalid syntax for -c,--change: Missing new imdbid or/and new Status "
            )
            print("correct syntax: -c -f filename.ext -i 1234567 -t Ambiguous")
            sys.exit()
        else:
            if not os.path.isabs(LaunchOptions["Filename"]):
                tmpFileName = os.path.join(SourcePath, LaunchOptions["Filename"])
                LaunchOptions["Filename"] = os.path.basename(LaunchOptions["Filename"])
            if not os.path.exists(tmpFileName):
                print("File Not Found")
                sys.exit()
    return LaunchOptions


SourceRelativePath = None
SourcePath = None
CacheRelativePath = "cache"
CachePath = os.path.join(os.getcwd(), CacheRelativePath)
TemplatesRelativePath = "templates"
MyMoviesCatalog = []  # list of Imported Movies
SleepInMS = 2000  # 2sec interval between calls to google (to prevent detection of bot)
constHowManyPortraitsShouldFetch = 6  # fetch six portraits -
constHowManyActorsShouldDisplay = (
    6
)  # pass this const/var to javascript - how many actors should I display for each movie?
shouldCrossReferenceOnDuckDuckGo = (
    False
)  # was working fine set to True, until duckduckgo stopped working on my computer! Perhaps I was throttles, perhaps it's country-wide issue.
CurrentMovieDataFileVersion = (
    19032501
)  # format: YY+MM+DD+INC:0,1,2.. changing this, causes the moviedata files to be modified/touched/updated
DefaultThumbnailWidth = 256  # 256px
# ValidFileTypes = [".mkv",".avi",".mp4",".mov",".mpeg",".txt",".torrent"] #list of valid filetypes to treat as movie names and fetch their data
# includeFoldersInValidFileTypes = True #additionally allow folders to be treated as movie names and fetch their data
from DefaultSettings import *

try:
    from UserSettings import *  # if UserSettings.py exists, it overwrites Defaults settings
except ImportError:
    pass
if SourceRelativePath and not SourcePath:
    SourcePath = os.path.join(os.getcwd(), SourceRelativePath)
if not myTMDB_APIkey:
    print(
        "Error: You haven't set an TMDB_APIkey. You need to create an account on TMDB, request an API key and set the generated key into the DefaultSettings.py - sample value: myTMDB_APIkey='036119ba3e5391bfb9941113a089417e'"
    )
    exit()
if not SourcePath and not SourceRelativePath:
    print(
        "Error: You haven't set a folder where the movies are. Open DefaultSettings.py and set SourcePath (absolute) or SourceRelativePath (relative) into the desired one"
    )
    exit()

ia = imdb.IMDb()  # imdb object


def main(argv):
    # TestRun()

    LaunchOptions = BuildLaunchOptions(argv)
    MakeDirectory(CachePath, "", "")
    if os.path.isdir(SourcePath) and os.path.isdir(CachePath):
        if LaunchOptions["ListItems"]:
            print("\n")
            print(
                "   \t{:^30.30}\t{:<4.4}\t{:<7.7}\t{:<13.13}\t{:<60.60}".format(
                    "Movie Name", "Year", "IMDB ID", "Import Status", "Filename"
                )
            )
            print("{:_<132}".format(""))
        myreps = 0
        # SourceFilesList=set(os.listdir(SourcePath))
        SourceFilesList = {}
        CacheFilesList = {}
        if includeFoldersInValidFileTypes:
            SourceFilesList = {
                f + os.sep
                for f in os.listdir(SourcePath)
                if os.path.isdir(os.path.join(SourcePath, f))
            }
        SourceFilesList = SourceFilesList.union(
            {
                f
                for f in os.listdir(SourcePath)
                if os.path.isfile(os.path.join(SourcePath, f))
            }
        )
        # CacheFilesList=os.listdir(CachePath)
        if includeFoldersInValidFileTypes:
            CacheFilesList = {
                f + os.sep
                for f in os.listdir(CachePath)
                if os.path.isdir(os.path.join(CachePath, f, os.sep))
            }
        CacheFilesList = CacheFilesList.union(
            {
                f
                for f in os.listdir(CachePath)
                if os.path.isfile(os.path.join(CachePath, f))
            }
        )
        for File in CacheFilesList:
            FileURI = os.path.join(CachePath, File)
            if File.endswith(".ffiles/"):
                StrippedMovieName = StripExtension(File)
                if LaunchOptions["ScanFolder"] and isFolderOrphan(
                    SourceFilesList, CachePath, StrippedMovieName
                ):
                    print("deleting: " + File)
                    DeleteFolder(CachePath, StrippedMovieName)
        for File in SourceFilesList:
            FileURI = os.path.join(SourcePath, File)
            # 13/4/19: HERE!!!!
            if isValidMovieFile(SourcePath, File):
                StrippedMovieName = StripExtension(File)
                # print(".", end ="")
                ShouldUpdateFile = False
                # print(str(LaunchOptions["UpdateFile"]) + "\t"+ LaunchOptions["Filename"] +"\t" + File)
                if (
                    LaunchOptions["UpdateFile"]
                    and LaunchOptions["Filename"] == File
                    and LaunchOptions["Filename"]
                ):
                    ShouldUpdateFile = (
                        True
                    )  # apparently, this is one file that needs updating! Bypassing main loop
                    print(".")
                if (ShouldUpdateFile and LaunchOptions["ImdbID"]) or (
                    LaunchOptions["ScanFolder"]
                    and isMissingDataFile(CachePath, StrippedMovieName)
                ):
                    myreps += 1
                    if myreps % 25 == 0:
                        print("sleeping:")
                        time.sleep(randint(10, 100))
                        print("woken.")
                    # perform prefetching loop for new movies
                    FileClean = PreCleanUpFileName(File)
                    info = PTN.parse(FileClean)
                    MovieName = PostCleanUpFileName(info["title"])
                    MakeDirectory(CachePath, StrippedMovieName)
                    if "year" not in info:
                        info["year"] = ""
                    # print("Searching for " + MovieName +":" )
                    old_time = int(round(time.time() * 1000))
                    MovieID1 = None
                    MovieID2 = None
                    MovieID = None
                    if (
                        LaunchOptions["UpdateFile"]
                        and LaunchOptions["ImdbID"]
                        and ShouldUpdateFile
                    ):
                        MovieID1 = LaunchOptions["ImdbID"]
                        print("fetching data for movie with ID " + str(MovieID1))
                        MovieID2 = MovieID1
                        MovieName = "New"
                    else:
                        MovieID1 = GetMovieIDfromWeb(
                            MovieName, info["year"], Provider="google"
                        )
                        if shouldCrossReferenceOnDuckDuckGo:
                            # check on duckduckgo too!
                            MovieID2 = GetMovieIDfromWeb(
                                MovieName, info["year"], Provider="duckduckgo"
                            )
                        else:
                            MovieID2 = MovieID1  # bypass duckduckgo
                        MovieID = None
                    tmpMovieData = {}
                    # print("Check: %s is %d on google and %d on tmdb" %(MovieName,MovieID1,MovieID2))
                    if MovieID1 == MovieID2 and MovieID1 == -1:
                        print(MovieName + " not found")
                        tmpMovieData["Status"] = "Unimported"
                        tmpMovieData["Kind"] = "Unknown"
                    else:
                        if MovieID1 == -1:
                            MovieID = (
                                MovieID2
                            )  # if duckduckgo had an answer and google didn't, pick duckduckgo (though it's 99% wrong)
                        else:
                            MovieID = (
                                MovieID1
                            )  # google does better, anyways, so pick google.
                        if MovieID1 != MovieID2:
                            print(
                                "Ambiguity: %s is %d on google and %d on duckduckgo"
                                % (MovieName, MovieID1, MovieID2)
                            )
                            tmpMovieData["Status"] = "Ambiguous"
                        else:
                            print("%s ID is %d" % (MovieName, MovieID))
                            if LaunchOptions["UpdateFile"] and ShouldUpdateFile:
                                tmpMovieData[
                                    "Status"
                                ] = "Verified"  # hey, it's set by the user!
                            else:
                                tmpMovieData[
                                    "Status"
                                ] = "Unverified"  # automatic match, might be wrong
                        if MovieID > 0:
                            # for x in range(40):
                            # 	WrapTMDBDataInIMDB(MovieID)
                            tmpData = WrapTMDBDataInIMDB(MovieID)
                            if tmpData:
                                tmpMovieData.update(tmpData)
                            else:
                                print(
                                    "Error, couldn't find movie with ImdbID %d on TMDB"
                                    % (MovieID)
                                )
                                tmpMovieData[
                                    "Status"
                                ] = (
                                    "Incomplete"
                                )  # assumed TMDB found nothing, deem data incomplete
                        else:
                            print(
                                "Bug, couldn't find movie because I chose movieID %d whereas it should never reach here"
                                % (MovieID)
                            )
                        print(".", end="", flush=True)
                        # pprint.pprint(tmpMovieData)
                        if "TMDBID" in tmpMovieData:
                            tmp = FetchMovieDataIMDBLite(MovieID, True)
                            tmpMovieData = selectiveMerge(tmpMovieData, tmp)
                            print(".", end="", flush=True)
                            # pprint.pprint(tmp)
                        else:
                            tmp = FetchMovieDataIMDBLite(MovieID, True)
                            tmpMovieData = update(tmpMovieData, tmp)
                            print(".", end="", flush=True)
                            # pprint.pprint(tmp)
                        print(".", end="", flush=True)
                        if "TMDBPoster" in tmpMovieData:
                            PosterURL = ConstructTMDBImageURL(
                                tmpMovieData["TMDBPoster"], ImageWidth="original"
                            )
                            if PosterURL:
                                if (
                                    isMissingPosterFile(CachePath, StrippedMovieName)
                                    or ShouldUpdateFile
                                ):
                                    PosterData = getImageDataFromURL(PosterURL)
                                    PosterFileName = os.path.join(
                                        CachePath,
                                        StrippedMovieName + ".ffiles",
                                        "poster.jpg",
                                    )
                                    WriteDataToFile(
                                        PosterData, PosterFileName, ShouldUpdateFile
                                    )
                                else:
                                    print(
                                        "Bug, poster file already exists in folder - why? should had already purged"
                                    )
                        if "TMDBBackdrop" in tmpMovieData:
                            BackdropURL = ConstructTMDBImageURL(
                                tmpMovieData["TMDBBackdrop"], ImageWidth="original"
                            )
                            if BackdropURL:
                                if (
                                    isMissingBackdropFile(CachePath, StrippedMovieName)
                                    or ShouldUpdateFile
                                ):
                                    BackdropData = getImageDataFromURL(BackdropURL)
                                    BackdropFileName = os.path.join(
                                        CachePath,
                                        StrippedMovieName + ".ffiles",
                                        "backdrop.jpg",
                                    )
                                    WriteDataToFile(
                                        BackdropData, BackdropFileName, ShouldUpdateFile
                                    )
                                else:
                                    print(
                                        "Bug, backdrop file already exists in folder - why? should had already purged"
                                    )

                        # DATA POST FIXES -- for everytime you import something:
                        # 1. remove authorname from plot
                        tmpMovieData["Plot"] = RemoveAuthorFromPlot(
                            tmpMovieData["Plot"]
                        )
                        tmpMovieData["Languages"] = ConvertLanguageCodeToName(
                            tmpMovieData["Languages"]
                        )
                        tmpMovieData["Countries"] = ConvertCountryCodeToName(
                            tmpMovieData["Countries"]
                        )
                    tmpMovieData["DateAdded"] = time.strftime(
                        "%Y-%m-%d", time.gmtime(os.path.getmtime(FileURI))
                    )
                    # ^--- date that the movie file was added
                    tmpMovieData["DateImported"] = datetime.date.today().strftime(
                        "%Y-%m-%d"
                    )
                    # ^--- date tha the file was imported into the database (ie today)
                    tmpMovieData["Filename"] = StrippedMovieName
                    tmpMovieData["DataInternalVersion"] = CurrentMovieDataFileVersion
                    CreateMovieDataFile(
                        CachePath, StrippedMovieName, tmpMovieData, ShouldUpdateFile
                    )
                    if doesFileExist(
                        CachePath, tmpMovieData["Filename"], "poster.jpg"
                    ) and (
                        ShouldUpdateFile
                        or not doesFileExist(
                            CachePath, tmpMovieData["Filename"], "poster_thumbnail.jpg"
                        )
                    ):
                        GenerateGalleryThumbnail(
                            CachePath,
                            tmpMovieData["Filename"],
                            "poster.jpg",
                            "poster_thumbnail.jpg",
                            DefaultThumbnailWidth,
                        )
                    new_time = int(round(time.time() * 1000))
                    diff_time = new_time - old_time
                    remaining_sleep = SleepInMS - diff_time
                    # print('old:%d new:%d, diff:%d' % (old_time, new_time, remaining_sleep))
                    if remaining_sleep > 0:
                        time.sleep(remaining_sleep / 1000.0)
                ignore_not_found = not LaunchOptions[
                    "ScanFolder"
                ]  # ignore not found files and suppress warnings, if you were not asked to scan (and update files)

                MovieData2 = RestoreMovieDataFile(
                    CachePath, StrippedMovieName, ignore_not_found
                )

                # print("LO")
                # pprint.pprint(LaunchOptions)
                # print(StrippedMovieName)
                # print("MD2")
                # pprint.pprint(MovieData2)
                if MovieData2:
                    if (
                        LaunchOptions["ListItems"]
                        and MovieData2["Status"]
                        in LaunchOptions["DisplayedItemsStatus"]
                    ):
                        if MovieData2["Status"] == "Verified":
                            print(
                                "[+]\t{:<30.30}\t{:4d}\t{:7d}\t{:>13.13}\t{:<10.60}".format(
                                    MovieData2.get("Title"),
                                    MovieData2.get("ReleaseYear"),
                                    MovieData2.get("ImdbID"),
                                    MovieData2.get("Status"),
                                    MovieData2.get("Filename"),
                                )
                            )
                        if MovieData2["Status"] == "Unimported":
                            print(
                                "[-]\t{:^30.30}\t{:^4.4}\t{:^7.4}\t{:>13.13}\t{:<10.60}".format(
                                    "-",
                                    "-",
                                    "-",
                                    MovieData2.get("Status"),
                                    MovieData2.get("Filename"),
                                )
                            )
                        if MovieData2["Status"] == "Unverified":
                            print(
                                "   \t{:<30.30}\t{:4d}\t{:7d}\t{:>13.13}\t{:<10.60}".format(
                                    MovieData2.get("Title"),
                                    MovieData2.get("ReleaseYear"),
                                    MovieData2.get("ImdbID"),
                                    MovieData2.get("Status"),
                                    MovieData2.get("Filename"),
                                )
                            )
                        if MovieData2["Status"] == "Ambiguous":
                            print(
                                "(?)\t{:<30.30}\t{:4d}\t{:7d}\t{:>13.13}\t{:<10.60}".format(
                                    MovieData2.get("Title"),
                                    MovieData2.get("ReleaseYear"),
                                    MovieData2.get("ImdbID"),
                                    MovieData2.get("Status"),
                                    MovieData2.get("Filename"),
                                )
                            )
                        if MovieData2["Status"] == "Incomplete":
                            print(
                                "[?]\t{:<30.30}\t{:4d}\t{:7d}\t{:>13.13}\t{:<10.60}".format(
                                    MovieData2.get("Title"),
                                    MovieData2.get("ReleaseYear"),
                                    MovieData2.get("ImdbID"),
                                    MovieData2.get("Status"),
                                    MovieData2.get("Filename"),
                                )
                            )
                # else:
                # (do not display pending files)
                # 		print("***\t{:^30.30}\t{:^4.4}\t{:^7.4}\t{:>13.13}\t{:<10.60}".format("-","-","-","Pending",StrippedMovieName))
                if ShouldUpdateFile and MovieData2:
                    if (
                        LaunchOptions["UpdateFile"]
                        and LaunchOptions["NewStatus"]
                        and ShouldUpdateFile
                    ):
                        MovieData2["Status"] = LaunchOptions["NewStatus"]
                        UpdateMovieDataFile(
                            CachePath, MovieData2["Filename"], MovieData2
                        )
                        print("updating...")
                elif ShouldUpdateFile:
                    print(
                        "File not imported yet, please import first (with -s,--scan option)"
                    )
                    # F12BUGGGGGGG

                if MovieData2:
                    MyMoviesCatalog.append(copy.deepcopy(MovieData2))
                # pprint.pprint(MyMoviesCatalog[-1])
        print("\n============ Building index ===========")
        for Movie in MyMoviesCatalog:
            # FIX1: for early imported json data, where the file with the full extension was saved, convert them in-memory

            FileIsDirty = False

            if "DataInternalVersion" not in Movie:
                Movie["DataInternalVersion"] = 0
                FileIsDirty = True

            if Movie.get("DataInternalVersion") < CurrentMovieDataFileVersion:
                print(
                    "Old file version. Setting update dirty bit for "
                    + Movie["Filename"]
                )
                Movie["DataInternalVersion"] = CurrentMovieDataFileVersion
                FileIsDirty = True

            # FIX1: strip .avi from filename [done, did once]
            # if Movie['Filename'][-8:] == '.avi':
            # 	print("Updating Filename for "+Movie['Filename'])
            # 	Movie['Filename']=StripExtension(Movie['Filename'])
            # 	FileIsDirty = True

            # FIX2: strip ::AuthorName from plot tags [done, did once]
            # if "Plot" in Movie:
            # 	Movie['Plot'] = RemoveAuthorFromPlot(Movie['Plot'])
            # 	print("Stripping Author from Plot for "+Movie['Filename'])
            # 	FileIsDirty = True

            # FIX3: find language that are encloded as 2 words
            """
			if Movie.get('Languages'):
				for index in range(len(Movie['Languages'])):
					Lang=Movie['Languages'][index]
					if len(Lang) == 2:
						Movie['Languages'][index] = LanguageNameByCode(Lang)
						FileIsDirty = True
			if Movie.get('Countries'):
				for index in range(len(Movie['Countries'])):
					Country = Movie['Countries'][index]
					if len(Country) == 2:
						Movie['Countries'][index] = CountryNameByCode(Country)
						FileIsDirty = True
			"""
            # FIX4: update all files so that the 1st actor in the list, gets order=0 (Should need to run once only)
            """
			if "Kind" in Movie and Movie["Kind"] not in ["Unknown"]:
				if "Cast" in Movie:
					if len(Movie["Cast"])> 0:
						if not"Order" in Movie["Cast"][0]:
							Movie["Cast"][0]["Order"] = 0
							FileIsDirty = True
						else:
							print("error, Actor" + Movie["Cast"][0]["Name"]+" already has order set in " + Movie['Title'])
					else:
						print("error, empty Cast list in " + Movie['Title'])
				else:
					print("error, no Cast in " + Movie['Title'])
			"""

            if doesFileExist(
                CachePath, Movie["Filename"], "poster.jpg"
            ) and not doesFileExist(
                CachePath, Movie["Filename"], "poster_thumbnail.jpg"
            ):
                GenerateGalleryThumbnail(
                    CachePath,
                    Movie["Filename"],
                    "poster.jpg",
                    "poster_thumbnail.jpg",
                    DefaultThumbnailWidth,
                )
                # print("Generating Thumbnail for movie "+Movie['Filename'])

            if FileIsDirty == True:
                UpdateMovieDataFile(CachePath, Movie["Filename"], Movie)
                print("Writing Changes for movie file  " + Movie["Filename"])

            # if 'ImdbID' in Movie:
            # if Movie['ImdbID']==54698 or Movie['ImdbID']==6628102 or Movie['ImdbID']==499262 or Movie['Status'] == "Unimported" or Movie['ImdbID']==2675914:
            # 	tmpString=Movie['Filename']

        BuildIndex(MyMoviesCatalog)
        print("\n================= Done ================")
        PickleMyCatalog = False
        if PickleMyCatalog:
            file_Name = os.path.join(CachePath, "fulldump.tmp")
            fileObject = open(file_Name, "wb")
            pickle.dump(MyMoviesCatalog, fileObject)
            fileObject.close()

        JSONMyCatalog = False
        if JSONMyCatalog:
            file_Name = os.path.join(CachePath, "fulldump.json")
            with open(file_Name, "w") as JSONFile:
                json.dump(MyMoviesCatalog, JSONFile)
    else:
        print("Path " + CachePath + " does not exist")


if __name__ == "__main__":
    main(sys.argv[1:])
