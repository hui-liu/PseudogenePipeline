#Prepares a file for use by Z_1_1_makeEvalMotifTable.py by taking in 2 files,
#with motif and median intensity info, averaging the two medians, ordering the
#motifs by average median intensity and keeping only the top 200 results.  This
#Info is output in a format that will be understood by the aforementioned script.
#WARNING: HIGHLY SITUATION SPECIFIC
#WARNING: ASSUMES THE FIRST LINE IN THE FILE HAS THE HIGHEST INTESITY VALUE
#Created by David E. Hufnagel on Jan 15, 2013

import sys

inpA = open(sys.argv[1])
inpB = open(sys.argv[2])
out = open(sys.argv[3], "w")



def ImportFile(inp):
    dictX = {}
    first = True #says whether this is the first data line
    for line in inp:
        if not line.startswith("#"):
            lineLst = line.split("\t")
            #get max intensity value for normalization
            if first == True:
                maxIntensity = lineLst[3]
            
            #normalize intensity #WARNING: ASSUMES THE FIRST LINE IN THE FILE HAS THE HIGHEST INTESITY VALUE
            intensity = (float(lineLst[3]) / float(maxIntensity)) * 1000
            dictX[lineLst[0]] = (lineLst[1], intensity)
            if first == True:
                first = False

    return dictX




#import file info into dicts of key: motif val: (revComp, intensity)
inpAdict = ImportFile(inpA)
inpBdict = ImportFile(inpB)

#combine the 2 dicts into 1 list of tuples of: [(intensity, motif, revComp),], averaging their intensity values
bigList = []
cnt = 0
for motifA in inpAdict:
    #print cnt every 100 lines
    if not cnt % 100:
        print cnt
    
    for motifB in inpBdict:
        if motifA == motifB or motifA == inpBdict[motifB][0]:
            #average the intensity values
            intensity = (float(inpAdict[motifA][1]) + \
                         float(inpBdict[motifB][1])) / 2.0
            
            #add to list
            bigList.append((intensity, motifA, inpAdict[motifA][0]))
            
    cnt += 1

#sort the big list and output the info
bigList.sort(reverse=True)
cnt = 1
for group in bigList:
    if cnt > 200:
        break
    out.write("%s\t%s\t%s\r" % (group[1], group[2], group[0]))
    cnt += 1
    




inpA.close()
inpB.close()
out.close()
