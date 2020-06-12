from main import minion
import os


try:
    testname = os.getenv("testname")
except Exception as e:
    print(str(e))
try:
    iterations = int(os.getenv("iterations"))
except Exception as e:
    iterations=1


#m = minion('vcst.sample.test.test')
#m = minion('vcst.sample.vm.vmotion')
m = minion(testname,True)

#m.preprocessTestFile()
m.initializeTestObj()
m.testMe(iterations, 2)