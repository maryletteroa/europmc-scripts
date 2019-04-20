# -*- coding: utf-8 -*-
# @Author: Marylette B. Roa
# @Date:   2019-04-18 13:35:13
# @Last Modified by:   Marylette B. Roa
# @Last Modified time: 2019-04-20 17:00:13

"""
This script accesses the European PMC API with queries written inside the
'data' dictionary. Output is a tab-delimited list of information from these publications.

tagged in the comment as [MODIFY THIS]: 
    pay attention to these values when editing this script

API documentation at: https://europepmc.org/RestfulWebService#!/Europe32PMC32Articles32RESTful32API
"""

import requests
import json
from pprint import  pprint
import datetime
from sys import  argv, exit


def getInfo(results):
    hits = results["resultList"]["result"]
    # [MODIFY THIS] add or remove information from "infos" list
    # see search_result.txt for keys inside results["resultList"]["result"]
    infos = ["isOpenAccess",
            "citedByCount",
            "id",
            "pmcid",
            "pmid", 
            "authorString",
            "title",
            "journalTitle",
            "pubYear",
            "journalVolume",
            "pageInfo",
            "doi",
            ]
    outf_name = "records.txt"
    with open(outf_name, "a") as outf:

        txt = f"Total records retrieved: {len(hits)}"
        print(txt)
        print(txt , file=outf)

        print("\t"+"\t".join(infos), file=outf)
        for hit in hits:
            ret_infos = [] 
            for info in infos:   
                try:
                    ret_infos.append(str(hit[info]))
                except KeyError:
                    ret_infos.append("")
            print("\t"+"\t".join(ret_infos), file=outf)
    print(f"Output written in {outf_name}")

def runSearch(url, data):
# check if there is an outbound network first
    try: 
        response = requests.get(url, params=data)
        # check if response == 200 
        if response:
            try:
                results = json.loads(response.text[1:-1]) # remove start and end parenthesis to convert into json properly
                outf_name = "records.txt"
                now = datetime.datetime.now()
                with open(outf_name, "w") as outf:
                    ## put all printables to both STDOUT and file to a list called txt
                    txts = [f"Date and time of query: {now}",
                    f"Query: {results['request']['query']}",
                    f"Hit count: {results['hitCount']}"
                    ]
                    for txt in txts:
                        print(txt)
                        print(txt, file=outf)
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




