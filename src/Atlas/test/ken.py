import os
import unittest

from scipy.io import loadmat

from openmdao.main.api import set_as_top, Assembly
from openmdao.main.test.test_derivatives import SimpleDriver

from Atlas.aero import Aero, Aero2

Npoint = 2
comp = Aero(Npoint)

# populate inputs
path = os.path.join(os.path.dirname(__file__), 'aero.mat')
data = loadmat(path, struct_as_record=True, mat_dtype=True)

comp.b        = int(data['b'][0][0])
comp.yN       = data['yN'].flatten()[:Npoint+1]
comp.Ns       = max(comp.yN.shape) - 1
comp.R        = 10.0
comp.dr       = [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.][:Npoint]
comp.r        = [ 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5][:Npoint]
comp.h        = data['h'][0][0]
comp.ycmax    = data['ycmax'][0][0]

comp.rho      = data['rho'][0][0]
comp.visc     = data['visc'][0][0]
comp.vw       = data['vw'][0][0]
comp.vc       = data['vc'][0][0]
comp.Omega    = data['Omega'][0][0]

comp.c        = data['cE'][:Npoint]
comp.Cl       = data['Cl'][:Npoint]
comp.d        = data['d'][:Npoint]

comp.yWire    = data['yWire'][0]
comp.zWire    = data['zWire'][0][0]
comp.tWire    = data['tWire'][0][0]

comp.Cm       = data['Cm'][:Npoint]
comp.xtL      = data['xtL'][:Npoint]
comp.xtU      = data['xtU'][:Npoint]

# run
comp.run()

model = set_as_top(Assembly())
model.add('aero', comp)
model.add('driver', SimpleDriver())
model.driver.workflow.add('aero')

model.run()

inputs = []
for item in comp.list_inputs():
    try:
        comp.get_flattened_value(item)
        inputs.append('aero.'+item)
    except:
        continue

outputs = []
for item in comp.list_outputs():
    try:
        comp.get_flattened_value(item)
        outputs.append('aero.'+item)
    except:
        continue

#inputs = ['aero.vc']
#model.driver.calc_gradient(inputs=inputs, outputs=outputs)
#model.driver.check_gradient(inputs=inputs, outputs=outputs)

inputs = [z.split('.')[1] for z in inputs]
outputs = [z.split('.')[1] for z in outputs]
inputs = ['yWire']
#model.aero.driver.gradient_options.atol = 1e-16
#model.aero.driver.gradient_options.rtol = 1e-16
model.aero.driver.check_gradient(inputs=inputs, outputs=outputs)


print "done"