#!/usr/env python
import math
import os
from sys import argv, stdout
import sys


def read_file( fd ):
    os.system("cp ../basis4 .")
    lineit = iter(fd)
    mol=""
    states = "[3,3,0,3]"
    nh = 0
    hydrogen = False
    nc = 0
    carbon = False
    nn = 0
    nitrogen = False
    no = 0
    oxygen = False
    nf = 0
    fluorine = False
    ns = 0
    sulfur = False
    ncl = 0
    chlorine = False
    for line in lineit:
#Getting geometry
        if '$molecule' in line:
            curline = next(lineit)
            file = open("geo", "w")
            while (not "end" in curline):
                file.write(curline)
                atom = curline.split()[0]
                if (atom=="H"): 
                    nh += 1
                    hydrogen = True
                if (atom=="C"): 
                    nc += 1
                    carbon = True
                if (atom=="N"): 
                    nn += 1
                    nitrogen = True
                if (atom=="O"): 
                    no += 1
                    oxygen = True
                if (atom=="F"): 
                    nf += 1
                    fluorine = True
                if (atom=="S"): 
                    ns += 1
                    sulfur = True
                if (atom=="Cl"): 
                    ncl += 1
                    chlorine = True
                curline = next(lineit)
            
            file.close()
            if (carbon): 
                mol=mol+"c"
                if (nc>1): mol=mol+str(nc)
            if (hydrogen): 
                mol=mol+"h"
                if (nh>1): mol=mol+str(nh)
            if (nitrogen): 
                mol=mol+"n"
                if (nn>1): mol=mol+str(nn)
            if (oxygen): 
                mol=mol+"o"
                if (no>1): mol=mol+str(no)
            if (fluorine): 
                mol=mol+"f"
                if (nf>1): mol=mol+str(nf)
            if (sulfur): 
                mol=mol+"s"
                if (ns>1): mol=mol+str(ns)
            if (chlorine): 
                mol=mol+"cl"
                if (ncl>1): mol=mol+str(ncl)
            print(mol)
#Getting basis
        if '$rem' in line:
            curline = next(lineit)
            while (not 'basis' in curline):
                curline = next(lineit)
            rem_bas = curline.split()[1]
        if '$basis' in line:
            curline = next(lineit)
            file1 = open("basis1", "w")
            file2 = open("basis2", "w")
            file3 = open("basis3", "w")
            while (not "end" in curline):
#                print("Hi")
                if 'aug-cc-pVTZ' in curline:
                    file1.write("aug-cc-pCVQZ\n")
                    file2.write("aug-cc-pCVTZ\n")
                    file3.write(curline)
                elif 'cc-pVTZ' in curline:
                    file1.write("cc-pVQZ\n")
                    file2.write(curline)
                    file3.write(curline)
                elif 'cc-pVDZ' in curline:
                    file1.write("cc-pVQZ\n")
                    file2.write(curline)
                    file3.write(curline)
                else:
                    file1.write(curline)
                    file2.write(curline)
                    file3.write(curline)                    
                curline = next(lineit)
            file1.close()
            file2.close()
            file3.close()




    ncores=nc+nn+no+nf+ns*5+ncl*5
    fgeo = open("geo", "r")
    geo = fgeo.read()
#Writing input file for carbon edge
    while(carbon or nitrogen or oxygen):
        if (carbon):
            carbon = False
            x = "c" 
            fc = "fc"
            shift = 10000
        elif (nitrogen):
            nitrogen = False
            x = "n"
            fc = str(ncores-nc)
            shift = 14000
        elif (oxygen):
            oxygen = False
            x = "o" 
            fc = str(ncores-nc-nn)
            shift = 19000


        for i in range(5):
            j = i+1
            if (j<5):
                fbasis = open("basis%i" %j, "r")
                bas = fbasis.read()
            if (j==1):
                basis="aCQ/Q/Q"
                rem_basis=rem_bas
            elif (j==2):
                basis="aCT/T/D"
                rem_basis=rem_bas
            elif (j==3):
                basis="aT/T/D"
                rem_basis=rem_bas
            elif (j==4):
                basis="uncontracted 6-311++G**"
                rem_basis="general"
            elif (j==5):
                basis="6-311++G**"
                rem_basis="6-311++G**"

            name = mol + "_%s_"%x + str(j)
            file = open("%s.in" %name, "w")
      #comment
            file.write("$comment\n")
            file.write("molecule: %s \n" %mol)
            file.write("basis: %s \n" %basis)
            file.write("edge: %s \n" %x)
            file.write("$end\n\n")
      #molecule
            file.write("$molecule\n")
            file.write(geo)
            file.write("$end\n\n")
      #rem
            file.write("$rem\n")
            file.write("method = eom-ccsd\n")
            file.write("basis = %s \n" %rem_basis)
            file.write("print_general_basis = true \n")
            file.write("cvs_ee_states = %s \n" %states)
            if (j < 4):
                file.write("purecart = 1111 \n")
            file.write("n_frozen_core = %s \n" %fc)
            file.write("cc_trans_prop = true \n")
            file.write("cc_memory = 40000 \n")
            file.write("eom_davidson_convergence = 4 \n")
            file.write("eom_shift = %i \n" %shift)
            file.write("$end\n\n")
      #basis
            if (j < 5):
                file.write("$basis\n")
                file.write(bas)
                file.write("$end\n\n")
            file.close()


if __name__ == '__main__':
    with open(argv[1],'r') as fd:
        read_file(fd)
        os.system("rm basis*")
        os.system("rm geo")

