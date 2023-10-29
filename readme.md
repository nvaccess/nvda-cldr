## NVDA - cldr

The CLDR repository is quite large, and takes a long time to clone.
NVDA only requires ~14MB of data from CLDR, and it is changed infrequently.
Rather than pull the whole CLDR repository into NVDA, this repo us used to create
the `source/locale/*/cldr.dic` files, from CLDR data.


## Requirements
- Python 3.11-32
  - Intention: Match the NVDA python version, reduce tooling complexity for developers. 

## Run
1. Ensure the output directory is empty or non-existent.
1. `py -3.7-32` build.py

## Output
See `out\` directory.
- `locale` directory contains all the generated cldr dictionaries.
- `cldrLocaleDicts.zip` is the `locale` directory zipped.

The contents of the `cldrLocaleDicts.zip` should be extracted to the NVDA `source/locale/` directory.
Example path after extraction: `source\locale\en\cldr.dic`.

## Logging
Default log level in `INFO`.
Change the level in `build.py` to `DEBUG` for higher verbosity.
