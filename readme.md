# About
Scripts to programmatically access publications.

# Status
Currently *in development!*  

| Start date | Up to |  
| ---------- | ------|  
| April 18, 2019 | Indefinite |  

Developed using Python 3.7.2

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
Scripts are found inside the [scripts](scripts) directory. Run the scripts as is in order to view the full help/usage prompt. *Substitute `foo.py` with the script name.*  This directory contains the following working script(s):  

- `search_europmc_api.py`
    This script queries the [European PMC API](https://europepmc.org/RestfulWebService#!/Europe32PMC32Articles32RESTful32API) using a user-supplied term
    and returns a tab-delimited list of information on papers corresponding to the said term. 

    ```
    Usage: python foo.py '<query_term>'
            e.g. python foo.py 'metagenomic&reptile'
        Save to file
            e.g. python foo.py 'metagenomic&reptile' > output.txt
    ```

    **Output**  
    See [output.txt](samples/output.txt)

    **Instructions to modify**  

    - See [`sample_result.txt`](samples/search_result.txt) to get an idea about the json structure. 
    - Check the API documentation [here](https://europepmc.org/RestfulWebService#!/Europe32PMC32Articles32RESTful32API).
    - Start with the parts tagged as `[MODIFY THIS]` inside the script

# License
[MIT License](https://spdx.org/licenses/MIT.html)

# Attribution
[Marylette Roa](www.twitter.com/MaryletteRoa)