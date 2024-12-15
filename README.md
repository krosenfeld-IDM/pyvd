# pyvd

`pyvd` calculates birth and mortality rates from UN WPP projections for a single country.

## Basic usage

0. Install
```bash
pip install pyvd
```
1. In a python terminal or script, calculate demography (e.g., birth rates by year)
```python
pop_input = make_pop_dat('IND')
year_vec = pop_input[0, :] - pyvd.constants.BASE_YEAR
year_init = pyvd.constants.BASE_YEAR - pyvd.constants.BASE_YEAR
pop_mat = pop_input[1:, :] + 0.1
pop_init = [np.interp(year_init, year_vec, pop_mat[idx, :])
            for idx in range(pop_mat.shape[0])]
vd_tup = demog_vd_calc(year_vec, year_init, pop_mat, pop_init)
```

## More about the data
You can learn about the data [here](https://population.un.org/wpp/). We combine both the retrospective (past) and projection (future) estimate, using the medium variant for the projects.

## Coming soon
- Subnational estimates

