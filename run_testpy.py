from main import minion
import os

try:
    iterations = int(os.getenv("iterations"))
except Exception as e:
    iterations=1
#m = minion('vcst.sample.test.test')
#m = minion('vcst.sample.vm.vmotion')
m = minion('vcst.rest.vcenter.recertify',True)

#m.preprocessTestFile()
m.initializeTestObj()
m.testMe(iterations, 2)