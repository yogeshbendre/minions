from main import minion
import os
iterations = int(os.getenv("iterations"))
#m = minion('vcst.sample.test.test')
m = minion('vcst.sample.vm.vmotion')
m.preprocessTestFile()
m.initializeTestObj()
m.testMe(iterations, 2)