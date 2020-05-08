import os
import logging
#import logging.config
import time
class IntelligentProcessor:

    srcPath = None
    destPath = None


    def __init__(self,srcPath,destPath):

        self.srcPath = srcPath
        self.destPath = destPath

    def createLogger(self):
        logging.config.fileConfig('logging.conf')
        # create logger
        self.logger = logging.getLogger('RunThisTest')

        # 'application' code
        #logger.debug('debug message')
        #logger.info('info message')
        #logger.warning('warn message')
        #logger.error('error message')
        #logger.critical('critical message')


    def getNextLineSpaces(self,myline1, myline2):
        sp = ""
        i = 0
        for i in range(0,len(myline2)):

            if myline2[i]==' ':
                sp = sp+' '
            else:
                break
        return sp


    def processContents(self):

        mycontent = None
        with open(self.srcPath,'r') as fp:
            mycontent = fp.read()

        mylines = mycontent.split('\n')

        mynewcontent = "import logging.config\n\n"
        nextlineind = 0
        firstfuncdone = False
        prevdef = ""
        for line in mylines:
            print(line)
            nextlineind = nextlineind + 1
            if nextlineind < len(mylines):
                nextline = mylines[nextlineind]

                if 'def ' in line:

                    print('Found '+line)
                    sp = self.getNextLineSpaces(line, mylines[nextlineind])

                    make_prev_print_stmt=""
                    if firstfuncdone:
                        make_prev_print_stmt = sp + "self.logger.info('Finished  "+prevdef+"')"+"\n"


                    currdef = line.split("def ")[1].split("(")[0]
                    make_print_stmt = sp + "self.logger.info('Perform "+currdef+"')"
                    myloggercall = ""
                    if '__init__' in line:
                        # This is an init function, must initialize a logger here
                        myloggercall = sp + "logging.config.fileConfig('logging.conf')\n"
                        myloggercall = myloggercall + sp + "self.logger = logging.getLogger('" + self.srcPath.replace("/",".").replace(".py","") + "')\n"
                        make_print_stmt = myloggercall + make_print_stmt

                    mynewcontent = mynewcontent+"\n"+make_prev_print_stmt+"\n"+line+"\n"+make_print_stmt
                    firstfuncdone = True
                    prevdef = currdef

                elif 'except ' in line:
                    print('Found exception line')
                    e_obj = line.split("as ")[1].split(":")[0]
                    sp = self.getNextLineSpaces(line, mylines[nextlineind])
                    make_print_stmt = sp + "self.logger.error('Failed in " + prevdef + ": '+str("+e_obj+"))"
                    mynewcontent = mynewcontent + "\n" + line + "\n" + make_print_stmt



                else:
                    mynewcontent = mynewcontent+"\n"+line

            else:
                mynewcontent = mynewcontent +"\n"+ line

        print(mynewcontent)
        #os.remove(self.destPath)
        #time.sleep(1)
        with open(self.destPath,'w') as fp:
            fp.write(mynewcontent)







