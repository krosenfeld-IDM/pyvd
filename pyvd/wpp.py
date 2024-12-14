""" wpp.py
scripts to process the WPP data
"""

import json
import pyvd
import numpy as np
from pathlib import Path

__all__ = ['make_pop_dat', 'make_fert_dat']

DATA_DIR = Path(pyvd.data.__file__).parent

# Rules for name cleaning
def reprule(revval):

    # Upper case
    revval = revval.upper()

    # Diacritics
    revval = revval.replace('Â', 'A')
    revval = revval.replace('Á', 'A')
    revval = revval.replace('Ç', 'C')
    revval = revval.replace('Ê', 'E')
    revval = revval.replace('É', 'E')
    revval = revval.replace('È', 'E')
    revval = revval.replace('Ï', 'I')
    revval = revval.replace('Ã¯', 'I')
    revval = revval.replace('Í', 'I')
    revval = revval.replace('Ñ', 'NY')
    revval = revval.replace('Ô', 'O')
    revval = revval.replace('Ó', 'O')
    revval = revval.replace('Ü', 'U')
    revval = revval.replace('Û', 'U')
    revval = revval.replace('Ú', 'U')

    # Alias characters to underscore
    revval = revval.replace(' ', '_')
    revval = revval.replace('-', '_')
    revval = revval.replace('/', '_')
    revval = revval.replace(',', '_')
    revval = revval.replace('\\', '_')

    # Remove ASCII characters
    revval = revval.replace('\'',   '')
    revval = revval.replace('"',    '')
    revval = revval.replace('’',    '')
    revval = revval.replace('.',    '')
    revval = revval.replace('(',    '')
    revval = revval.replace(')',    '')
    revval = revval.replace('\x00', '')

    # Remove non-ASCII characters
    revval = revval.encode('ascii', 'replace')
    revval = revval.decode()
    revval = revval.replace('?', '')

    # Condence and strip underscore characters
    while (revval.count('__')):
        revval = revval.replace('__', '_')
    revval = revval.strip('_')

    return revval


def make_pop_dat(TLC=''):

    # Name references
    tlc_wpp_dict = dict()

    fname = DATA_DIR / 'tlc_wpp_countries.json'
    with open(fname) as fid01:
        n_dict = json.load(fid01)
    tlc_wpp_dict.update(n_dict)

    fname = DATA_DIR / 'tlc_wpp_groups.json'
    with open(fname) as fid01:
        n_dict = json.load(fid01)
    tlc_wpp_dict.update(n_dict)

    # Parse CSVs
    wppf1 = DATA_DIR / 'WPP2022_POP_F02_1_POPULATION_BY_AGE_BOTH_SEXES_ESTIMATES.csv'
    with open(wppf1, errors='ignore') as fid01:
        flines_rev = [val.strip().split(',') for val in fid01.readlines()]

    wppf2 = DATA_DIR / 'WPP2022_POP_F02_1_POPULATION_BY_AGE_BOTH_SEXES_MEDIUM_VARIANT.csv'
    with open(wppf2, errors='ignore') as fid01:
        flines_fwd = [val.strip().split(',') for val in fid01.readlines()]

    # Construct output data structure
    rng = range(11, 32)
    pop_dat = np.zeros((0, 22), dtype=int)

    # Add values from retrospective estimates
    for rval in flines_rev:
        if TLC in tlc_wpp_dict and reprule(rval[2]) == tlc_wpp_dict[TLC]:
            year_val = int(rval[10])
            if (year_val % 5):
                continue
            if len(rval) > max(rng): bpop = [int(1000*float(rval[idx].replace(' ', ''))) for idx in rng]
            pop_dat = np.vstack((pop_dat, np.array([year_val]+bpop)))

    # Add values from forward projections
    for rval in flines_fwd:
        if (reprule(rval[2]) == tlc_wpp_dict[TLC]):
            year_val = int(rval[10])
            if (year_val % 5):
                continue
            if pop_dat.size > 0 and (year_val == pop_dat[-1, 0]):
                continue
            bpop = [int(1000*float(rval[idx].replace(' ', ''))) for idx in rng]
            pop_dat = np.vstack((pop_dat, np.array([year_val]+bpop)))

    return pop_dat.T


def make_fert_dat(TLC=''):

    # Name references
    tlc_wpp_dict = dict()

    fname = DATA_DIR / 'tlc_wpp_countries.json'
    with open(fname) as fid01:
        n_dict = json.load(fid01)
    tlc_wpp_dict.update(n_dict)

    fname = DATA_DIR / 'tlc_wpp_groups.json'
    with open(fname) as fid01:
        n_dict = json.load(fid01)
    tlc_wpp_dict.update(n_dict)

    # Parse CSVs
    wppf1 = DATA_DIR / 'WPP2022_FERT_F02_FERTILITY_RATES_BY_AGE_ESTIMATES.csv'
    with open(wppf1, errors='ignore') as fid01:
        flines_rev = [val.strip().split(',') for val in fid01.readlines()]

    wppf2 = DATA_DIR / 'WPP2022_FERT_F02_FERTILITY_RATES_BY_AGE_MEDIUM_VARIANT.csv'
    with open(wppf2, errors='ignore') as fid01:
        flines_fwd = [val.strip().split(',') for val in fid01.readlines()]

    # Construct output data structure
    rng = range(11, 20)
    fert_dat = np.zeros((0, 21), dtype=float)

    # Add values from retrospective estimates
    for rval in flines_rev:
        if (reprule(rval[2]) == tlc_wpp_dict[TLC]):
            year_val = int(rval[10])
            if (year_val % 5):
                continue
            bpop = [float(rval[idx].replace(' ', '')) for idx in rng]
            fert_row = np.zeros(20, dtype=float)
            fert_row[2:11] = bpop
            fert_row = fert_row.tolist()
            fert_dat = np.vstack((fert_dat, np.array([year_val]+fert_row)))

    # Add values from forward projections
    for rval in flines_fwd:
        if (reprule(rval[2]) == tlc_wpp_dict[TLC]):
            year_val = int(rval[10])
            if (year_val % 5):
                continue
            if (year_val == fert_dat[-1, 0]):
                continue
            bpop = [float(rval[idx].replace(' ', '')) for idx in rng]
            fert_row = np.zeros(20, dtype=float)
            fert_row[2:11] = bpop
            fert_row = fert_row.tolist()
            fert_dat = np.vstack((fert_dat, np.array([year_val]+fert_row)))

    return fert_dat.T

if __name__ == '__main__':
    print(DATA_DIR)

    pop_dat = make_pop_dat('IND')
    print(pop_dat.shape)

    fert_dat = make_fert_dat('GHA')
    print(fert_dat.shape)