# dmdb_project_clean_restaurants

#### Run instructions
- Install dependencies
- Run script main_run.py
    - If just a simple cleaning run is desired nothing needs to be changed
    - For recreation of/appending to the results_data simply comment out
     line [] and comment in line []

#### Dependencies
- MongoDB (i.e. mongoexport) available in PATH variable
- Python Libraries
  - pymongo
  - dnspython
  - requests
  - py_stringmatching
    - This package also needs a C/C++ compiler, as some elements are developed in cython. For
      more information please visit
      https://sites.google.com/site/anhaidgroup/projects/magellan/issues and 
      http://anhaidgroup.github.io/py_stringmatching/v0.4.1/Installation.html#c-compiler-required
    