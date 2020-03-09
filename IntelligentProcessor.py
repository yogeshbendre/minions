
import logging


class IntelligentProcessor:

    srcPath = None
    destPath = None


    def __init__(self,srcPath,destPath):

        self.srcPath = srcPath
        self.destPath = destPath


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

        mynewcontent = ""
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
                        make_prev_print_stmt = sp + "print('Finished  "+prevdef+"')"+"\n"
                    currdef = line.split("def ")[1].split("(")[0]
                    make_print_stmt = sp + "print('Perform "+currdef+"')"

                    mynewcontent = mynewcontent+"\n"+make_prev_print_stmt+"\n"+line+"\n"+make_print_stmt
                    firstfuncdone = True
                    prevdef = currdef

                elif 'except ' in line:
                    print('Found exception line')
                    e_obj = line.split("as ")[1].split(":")[0]
                    sp = self.getNextLineSpaces(line, mylines[nextlineind])
                    make_print_stmt = sp + "print('Failed in " + prevdef + ": '+str("+e_obj+"))"
                    mynewcontent = mynewcontent + "\n" + line + "\n" + make_print_stmt



                else:
                    mynewcontent = mynewcontent+"\n"+line

            else:
                mynewcontent = mynewcontent +"\n"+ line

            with open(self.destPath,'w') as fp:
                fp.write(mynewcontent)







