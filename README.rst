pyvd
====

pyvd calculates birth and mortality rates from UN WPP projections for a single country. 

Quickstart
----------

Install via pip::

    pip install pyvd

In a python terminal or script, calculate demography (e.g., birth rates by year)::

    import pyvd
    pop_input = pyvd.make_pop_dat('IND')
    year_vec = pop_input[0, :] - pyvd.constants.BASE_YEAR
    year_init = pyvd.constants.BASE_YEAR - pyvd.constants.BASE_YEAR
    pop_mat = pop_input[1:, :] + 0.1
    vd_tup = pyvd.demog_vd_calc(year_vec, year_init, pop_mat)

Additional examples can be found in the `documentation <https://krosenfeld-idm.github.io/pyvd/>`.

More about the data
-------------------
You can learn about the data at https://population.un.org/wpp/. We combine both the retrospective (past) and projection (future) estimate, using the medium variant for the projects.