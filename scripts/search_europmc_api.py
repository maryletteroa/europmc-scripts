# -*- coding: utf-8 -*-
# @Author: Marylette B. Roa
# @Date:   2019-04-18 13:35:13
# @Last Modified by:   Marylette B. Roa
# @Last Modified time: 2019-04-18 18:13:35

"""
This script accesses the European PMC API with queries written inside the
'data' dictionary. STDOUT is a tab-delimited list of open access studies.

tagged in the comment as [MODIFY THIS]: 
    pay attention to these values when editing this script

API documentation at: https://europepmc.org/RestfulWebService#!/Europe32PMC32Articles32RESTful32API
"""

import requests
import json
# from pprint import  pprint
import datetime
from sys import  argv, exit


def getInfo(results):
    # print info of openAccess articles
    hits = results["resultList"]["result"]
    # [MODIFY THIS] add or remove information from "infos" list
    # see search_result.txt for keys inside results["resultList"]["result"]
    infos = ["isOpenAccess",
            "citedByCount",
            "id", 
            "authorString",
            "title",
            "journalTitle",
            "pubYear",
            "journalVolume",
            "pageInfo",
            "doi",
            ]
    print("\t"+"\t".join(infos))
    for hit in hits:
        # print("\t".join([hit[info] for info in infos]))
        ret_infos = [] 
        for info in infos:   
            try:
                ret_infos.append(str(hit[info]))
            except KeyError:
                ret_infos.append("")
        print("\t"+"\t".join(ret_infos))

def runSearch(url, data):
# check if there is an outbound network first
    now = datetime.datetime.now()
    print("Date and time of query:", now)
    try: 
        response = requests.get(url, params=data)
        # check if response == 200 
        if response:
            try:
                results = json.loads(response.text[1:-1]) # remove start and end parenthesis to convert into json properly
                print(f"Hit count:{results['hitCount']}")
                print(f"Query: {results['request']['query']}")
                # pprint(results)
                getInfo(results)
            except json.decoder.JSONDecodeError:
                # because API does not otherwise return a non-200
                pprint(f"The query did not parse correctly")# but returned with the following message: \n\t{response.text}")
        else:
            print(f"An error occurred. {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\nA connection error occured. Check your network.")


if __name__ == "__main__":

    try:
        query = argv[1]
    except IndexError:
        print( """This script accesses the European PMC API using a user-supplied query term
    and returns a tab-delimited list of information of papers corresponding to the said term.
    Use the logical operators &, insted of ',' and spaces. Enclose in single quote ('') rather than
    double quote ("") e.g. 'metagenomic&reptile' instead of "metagenomic, reptile".

    Usage: 
        python foo.py '<query_term>' 
            e.g. python foo.py 'metagenomic&reptile'
        Save to file
            e.g. python foo.py 'metagenomic&reptile' > output.txt
                """)
        exit()


    # Euro PMC API url 
    URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    URL_SEARCH = URL + "/search?" # using the /search access for now (there are other ways to query the API, see API docs)

    #[MODIFY THIS] enter custom value for each parameter
    data_search = {
        "query": f"{query}",
        "resultType" : "lite", 
        "synonymn": "",
        "cursorMark": "*",
        "pageSize": "1000", #valid page size 1-1000 only
        "sort": "",
        "format": "json",
        "callback": "",
        "email": "",
    }
    runSearch(URL_SEARCH, data_search)




