# About
Scripts to programmatically access and retrieve information from publications through the [Europe PMC API](https://europepmc.org/RestfulWebService).

# Status
Currently *in development!*  

| Start date | Up to |  
| ---------- | ------|  
| April 18, 2019 | Indefinite |  

Developed and tested using Python 3.7.2 and Linux environment
 

# Installation
**Requirement**: At least Python 3.6  

Ideally, create and activate a virtual environment  

    ```
    python -m venv env
    source env/bin/activate
    ```  

Install  

    ```
    pip install -r requirements.txt
    ```

# Components
Scripts are found inside the [scripts](scripts) directory. Run the scripts as is in order to view the full help/usage prompt. *Substitute `foo.py` with the script name.*  This directory contains the following:  

- `search_europmc_api.py`  
    Queries the [European PMC API](https://europepmc.org/RestfulWebService) using a user-supplied term
    and returns a tab-delimited list of information on papers corresponding to the said term. 

    ```
    Usage: python foo.py '<query_term>'
            e.g. python foo.py 'metagenomic&reptile'
        Save to file
            e.g. python foo.py 'metagenomic&reptile'
    ```

    **Output**  
    See [`records.txt`](samples/records.txt)


- `retrieve_annotations.py`  
    Accesses the [European PMC  Annotations API](https://europepmc.org/AnnotationsApi) using a user-supplied list of publication ids. Returns a tab-delimited file containing annotated Organism terms present in each of these publications. 
    ```
    Usage: 
        python foo.py '<path_to_ids>' 
            e.g. python foo.py ids.txt
        Save to file
            e.g. python foo.py ../samples/ids.txt
    ```

    **Input**  
    See [`ids.txt`](samples/ids.txt)  

    **Output**  
    See [`annotations.txt`](samples/annotations.txt)


# Instructions to modify
- Check the API documentation [here](https://europepmc.org/RestfulWebService).
- Start with the parts tagged as `[MODIFY THIS]` inside the script

# License
[MIT License](license.txt)

# Attribution
[Marylette Roa](www.twitter.com/MaryletteRoa)