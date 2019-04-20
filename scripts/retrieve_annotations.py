# -*- coding: utf-8 -*-
# @Author: Marylette B. Roa
# @Date:   2019-04-19 10:36:19
# @Last Modified by:   Marylette B. Roa
# @Last Modified time: 2019-04-20 16:38:22

"""
This script accesses the European PMC API using a user-supplied list of publication ids
    and returns a tab-delimied file containing annotated Organism terms present in each of these publications

comment tagged [MODIFY THIS]
    Only the "Organisms" annotations are retrieved for now 
    Also query data parameters can be further customized

API documentation at: https://europepmc.org/AnnotationsApi#!/annotations45api45controller/getAnnotationsArticlesByIdsUsingGET
"""


import requests
import json
from pprint import  pprint
import datetime
from sys import  argv, exit
import  re

def retrieveAnnotations(ids,type_):

    # didn't break this up into smaller functions (e.g. retrieve, parse, collate) but could be

    infos = []
    counter_ids = 0

    # connect to API
    URL = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?"
    for id_ in ids:
        counter_ids += 1
        print(f"Retrieving annotations for {id_} ... {counter_ids}", end="\r") #\r for carriage return
        data = {
            "articleIds" : f"{id_}",
            "type" : f"{type_}",
            "section" : "",
            "provider" : "",
            "format" : "",
        } ## [MODIFY THIS]

        try: 
            response = requests.get(URL, params=data)
            # check if response == 200 
            if response:
                try:
                    results = json.loads(response.text[1:-1]) # remove start and end parenthesis to convert into json properly
                except json.decoder.JSONDecodeError:
                    # because API does not otherwise return a non-200
                    pprint(f"The query did not parse correctly")# but returned with the following message: \n\t{response.text}")
                    exit()
            else:
                print(f"An error occurred. {response.status_code}")
                exit()
        except requests.exceptions.ConnectionError:
            print("\nA connection error occured. Check your network.")
            exit()


        ## parse results 
        hs = [
            "extId",
            "source",
            "pmcid",
        ]
        sources = [results[h] for h in hs if results.get(h) != None] ## some records do not contain pmcid
                ## also used .get instead of try except to chatch KeyErrors!! 
        exacts = [annot["exact"] for annot in results.get("annotations")] ## the exact match to an Organism term

        ## some records do not contain "section" infos
        sections = []
        for annot in results["annotations"]:
            if annot.get("section") != None:
                sections.append(annot["section"].split(" (")[0])
            else:
                sections.append("?No description") # means missing section description

        info = {"id" : id_}
        info.update(dict(zip(hs, sources)))
        info_ = {}
        for s, e in zip(sections, exacts):
            if s not in info_ :
                info_[s] = []
                info_[s].append(e)
            else:
                if e.lower() not in map(str.lower,info_[s]):
                    info_[s].append(e)
        info.update(info_)
        infos.append(info)

    # collate results

    ## get headers
    ## I sampled around 40 ids to scope the headers but
    ## in case there are other headers and/or using
    ## more pubids, use the next 4 hashed lines
    ## and comment out the 'headers' list
    ## defining headers ahead of time saves another loop
    ## and also ensures that the headers are sorted
    ## but may result to some columns being blank in the output

    # _ = []
    # for info in infos:
    #     _ += list(info.keys())
    # headers = list(set(_))
    
    headers = ["id",
        "source",
        "extId",
        "pmcid",
        "Title",
        "Abstract",
        "Introduction",
        "Methods",
        "Results",
        "Discussion",
        "Conclusion",
        "Article",
        "Figure",
        "Table",
        "Supplementary material",
        "Author Contributions",
        "?No description",
    ] 

    outf_name = "annotations.txt" 
    with open(outf_name,"w") as outf:
        print("\t".join(headers), file=outf)

        # collate information
        for info in infos:
            vals = []   
            for header in headers:
                if info.get(header) != None:
                    if header in ["extId", "source", "pmcid", "id"]:
                        vals.append(info[header])
                    else:
                        vals.append(", ".join(info[header]))
                else:
                    vals.append("")
            print("\t".join(vals), file=outf)

    print(f"Retrieved a total of {counter_ids} annotations. Outfile written in '{outf_name}'. Done")

def getIds(path):
    try:
        with open(path) as infile:
            ids = [line.strip() for line in infile.readlines()]
        print(f"Found {len(ids)} ids")
        return(ids)
    except FileNotFoundError:
        print(f"Error. '{path}' not found.")
        exit()


############
## MAIN ###
############

if __name__ == "__main__":

    try:
        query = argv[1]
    except IndexError:
        print( """This script accesses the European PMC API using a user-supplied list of publication ids
    and returns a tab-delimited file containing annotated Organism terms present in each of these publications.  
    Format of the ids should be <SOURCE>:<ID_NUMBER> e.g. MED:30497052. Multiple ids are separated by
    new lines. ID_NUMBER should be relevant to the corresponding SOURCE.

    Usage: 
        python foo.py '<path_to_ids>' 
            e.g. python foo.py ids.txt
        Save to file
            e.g. python foo.py ../samples/ids.txt
                

    Allowed SOURCEs are:
        MED: PubMed MEDLINE, 
        PMC: PubMedCentral not in (PubMed), 
        PAT: Patents,
        AGR: Agricola (USDA/NAL), 
        CBA: Chinese biological abstracts, 
        HIR: NHS Evidence (UK HIR), 
        CTX: CiteXplore submission, 
        ETH: EThOS theses (BL), 
        CIT: CiteSeer (PSU),
        PPR: Preprints, 
        NBK: NLM Books (not in PubMed)

    """)
        exit()

    now = datetime.datetime.now()
    print("Date and time of query:", now)

    ids = getIds(argv[1])
    type_ = "Organisms" ## [MODIFY THIS] Only Organisms annotations are retrieved
    infos = retrieveAnnotations(ids,type_)




