'''
Load an old simulation to test regression.

Saved file originally generated by checking out Covasim v1.7.0 (with this file
not checked in) and running:

    import test_regression as tr
    tr.make_sim(do_save=True)
'''

import sciris as sc
import covasim as cv
import pytest

pop_size = 500
filename = 'example_regression.sim'
version = '1.7.0'


def make_sim(do_save=False, **kwargs):

    # Shared settings
    pars = dict(pop_size=pop_size, verbose=0)
    pars.update(kwargs)

    # Versioning was introduced in 2.0
    if cv.check_version('2.0.0', verbose=False) >= 0:
        pars.update({'version':version})

    sim = cv.Sim(**pars)
    sim.run()

    if do_save:
        print(sim.summary)
        sim.save(filename)

    return sim


def test_migration_regression():
    sc.heading('Testing migration and regression...')

    sim1 = cv.load(filename)
    sim2 = make_sim()

    # Check that they match
    cv.diff_sims(sim1, sim2, die=True)

    # Confirm that non-matching sims don't match
    sim3 = make_sim(beta=0.02123)
    with pytest.raises(ValueError):
        cv.diff_sims(sim1, sim3, die=True)

    return sim1, sim2



#%% Run as a script
if __name__ == '__main__':

    # Start timing and optionally enable interactive plotting
    T = sc.tic()

    sim1, sim2 = test_migration_regression()

    sc.toc(T)
    print('Done.')
