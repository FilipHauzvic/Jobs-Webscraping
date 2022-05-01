## Installation
Tested using ***Python v3.9**.
Install packages from requirements.txt (pip install -r requirements.txt).

### Lists all part-time job offers from fajn-brigady.cz for given location
#### Usage: python brigada.py [city]
When entering city don't use diacritics or spaces and only use lower-case letters.
If no city is given, default to Prerov.
If given city is not found, only offers for the whole country will be listed.
The result if stored in output.txt file, that will be created in the current directory.