## NVDA - cldr

The CLDR repository is quite large, and takes a long time to clone.
NVDA only requires ~60MB of data from CLDR, and it is changed infrequently.
Rather than pull the whole CLDR repository into NVDA, this repo us used to create
the `source/locale/*/cldr.dic` files, from CLDR data.


## Requirements
- Python 3.7-32
  - Intention: Match the NVDA python version, reduce tooling complexity for developers. 

## Run
1. Ensure the `build` directory is empty or non-existent.
1. `py -3.7-32` build.py

## Output
See `build\locale\`

## Logging
Default log level in `INFO`.
Change the level in `build.py` to `DEBUG` for higher verbosity.
