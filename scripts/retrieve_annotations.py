# -*- coding: utf-8 -*-
# @Author: Marylette B. Roa
# @Date:   2019-04-19 10:36:19
# @Last Modified by:   Marylette B. Roa
# @Last Modified time: 2019-04-19 16:20:25

import requests
import json
from pprint import  pprint
import datetime
from sys import  argv, exit
import  re

def getOrganismsInfo(results):
    annotations = results["annotations"]
    terms = {}
    for annotation in annotations:
        exact = annotation["exact"]
        section = annotation["section"].split(' ')[0]
        if section not in terms:
            terms[section] = []
            terms[section].append(exact)
        else:
            if exact.lower() not in map(str.lower,terms[section]):
                terms[section].append(exact)
    source = {}
    for h in ["extId", "pmcid", "source"]:
        try:
            source[h] = results[h]
        except KeyError:
            source[h] = ""
    organisms_info = {**source, **terms}
    return organisms_info

def runRetrieveAnnotation(ids, type_):
# check if there is an outbound network first
    URL = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?"
    for id_ in ids:
        data = {
            "articleIds" : f"{id_}",
            "type" : f"{type_}", #only one type to retreive per run
            "section" : "",
            "provider" : "",
            "format" : "",
        }
        try: 
            response = requests.get(URL, params=data)
            if response:
                try:
                    results = json.loads(response.text[1:-1]) # remove start and end parenthesis to convert into json properly
                    if type_ == "Organisms":
                        annotations = getOrganismsInfo(results)
                        yield annotations
                    # if type_ == "Accession Numbers":
                    #     accession_numbers_info = getAccessionNumbersInfo(results)
                except json.decoder.JSONDecodeError:
                    # because API does not otherwise return a non-200
                    pprint(f"The query did not parse correctly. Check the input.")# but returned with the following message: \n\t{response.text}")
            else:
                print(f"An error occurred. {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("\nA connection error occured. Check your network.")
    

def collateInfo(annotations,ids):
    annots = {}
    for annotation in annotations:
        for header in annotation:
            if header not in annots:
                annots[header] = []
                annots[header].append(annotation[header])
            else:
                annots[header].append(annotation[header])
    headers = list(annots.keys())
    print("\t".join(headers))
    # pprint(annots)
    for i, id_ in enumerate(ids):
        vals = []
        for header in headers:
            if id_ == f'{annots["source"][i]}:{annots["extId"][i]}':
                if header in ["extId", "pmcid", "source"]:
                    vals.append(annots[header][i])
                    # print(vals)
                else:
                    try:
                        vals.append(", ".join(annots[header][i]))
                    except IndexError:
                        vals.append("")
        print("\t".join(vals))



## TO BE DONE
def getAccessionNumbersInfo(results):
    annotations = results["annotations"]
    accession_numbers = []
    for annotation in annotations:
        prefix = annotation["prefix"]
        exact = annotation["exact"]
        postfix = annotation["postfix"]
        accession_number = f"{prefix}{exact}{postfix}"
        if accession_number not in accession_numbers:
            accession_numbers.append(accession_number)
    pprint(accession_numbers)


if __name__ == "__main__":
    now = datetime.datetime.now()
    print("Date and time of query:", now)
    ids = ["MED:26039313","MED:30497052"]
    type_ = "Organisms"
    annotations = runRetrieveAnnotation(ids, type_)
    collateInfo(annotations, ids)