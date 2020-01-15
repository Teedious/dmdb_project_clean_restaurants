# dmdb_project_clean_restaurants

## Run instructions
- Run the following command in the desired directory:

      > git clone https://github.com/Teedious/dmdb_project_clean_restaurants.git
#### Without pipenv

- Install dependencies (see dependencies below) by yourself
- Configure 'config-file' src/main_run.py
- Run script:

      > python -m src.main_run
      
#### With pipenv
(mongodb still needs to be installed manually and be available via PATH)
- Run the following commands in a shell in the git repository to create an 
environment where the dependencies are installed and switch to the environment:

      > pipenv --python3.7
      > pipenv install
      > pipenv shell
- Configure 'config-file' src/main_run.py
- Run script:

      > python -m src.main_run

## Dependencies
- MongoDB (i.e. mongoexport) available in PATH variable
- Python Libraries
  - pymongo
  - dnspython
  - py_stringmatching
    - This package also needs a C/C++ compiler, as some elements are developed in cython. For
      more information please visit
      https://sites.google.com/site/anhaidgroup/projects/magellan/issues and 
      http://anhaidgroup.github.io/py_stringmatching/v0.4.1/Installation.html#c-compiler-required
    
