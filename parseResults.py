#!/usr/bin/python

import os
import json
import re
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys, getopt

resultDir = "./results"
results = []

def main(argv):
    argument = ''
    usage = 'usage: parseResult.py -t <testName> -m <metric>'

    # parse incoming arguments
    try:
        opts, args = getopt.getopt(argv,"h:tm")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit()  
        elif opt in ("-t"):
            test = arg
        elif opt in ("-m"):
            metric = arg

    for file in os.listdir(resultDir):
        if file.endswith(".json"):
            test = {}
            parsedName = re.findall(r"([^-]+)-(\d+-?\d+)-([^_]+_?[^-]+)-.*", file)
            if len(parsedName)>0:
                test['name'] = str(parsedName[0][0])
                test['date'] = parsedName[0][1]
                test['scope'] = str(parsedName[0][2])
                with open(resultDir+"/"+file) as f:
                    data = json.load(f)

                    test['speedIndex'] = data['audits']['metrics']['details']['items'][0]['speedIndex']
                    test['observedSpeedIndex'] = data['audits']['metrics']['details']['items'][0]['observedSpeedIndex']
                    test['firstContentfulPaint'] = data['audits']['metrics']['details']['items'][0]['firstContentfulPaint']
                    test['observedLoad'] = data['audits']['metrics']['details']['items'][0]['observedLoad']
                    test['diagnostics_numRequests'] = data['audits']['diagnostics']['details']['items'][0]['numRequests']
                    #test['diagnostics_numScripts'] = data['audits']['diagnostics']['details']['items'][0]['numScripts']
                    #test['diagnostics_numStylesheets'] = data['audits']['diagnostics']['details']['items'][0]['numStylesheets']
                    #test['diagnostics_numFonts'] = data['audits']['diagnostics']['details']['items'][0]['numFonts']
                    #test['numTasks'] = data['audits']['diagnostics']['details']['items'][0]['numTasks']
                    #test['numTasksOver10ms'] = data['audits']['diagnostics']['details']['items'][0]['numTasksOver10ms']
                    #test['numTasksOver25ms'] = data['audits']['diagnostics']['details']['items'][0]['numTasksOver25ms']
                    #test['numTasksOver50ms'] = data['audits']['diagnostics']['details']['items'][0]['numTasksOver50ms']
                    #test['numTasksOver100ms'] = data['audits']['diagnostics']['details']['items'][0]['numTasksOver100ms']
                    #test['numTasksOver500ms'] = data['audits']['diagnostics']['details']['items'][0]['numTasksOver500ms']
                    test['rtt'] = data['audits']['diagnostics']['details']['items'][0]['rtt']
                    test['maxServerLatency'] = data['audits']['diagnostics']['details']['items'][0]['maxServerLatency']
                    test['totalByteWeight'] = data['audits']['diagnostics']['details']['items'][0]['totalByteWeight']
                    test['totalTaskTime'] = data['audits']['diagnostics']['details']['items'][0]['totalTaskTime']
                    test['mainDocumentTransferSize'] = data['audits']['diagnostics']['details']['items'][0]['mainDocumentTransferSize']

                    test['speedIndex_score'] = data['audits']['speed-index']['score']
                    test['speedIndex_rawValue'] = data['audits']['speed-index']['rawValue']

                    test['FCP_score'] = data['audits']['first-contentful-paint']['score']
                    test['FCPrawValue'] = data['audits']['first-contentful-paint']['rawValue']

                    test['FMP_score'] = data['audits']['first-meaningful-paint']['score']
                    test['FMP_rawValue'] = data['audits']['first-meaningful-paint']['rawValue']

                    test['TTFB_score'] = data['audits']['time-to-first-byte']['score']
                    test['TTFB_rawValue'] = data['audits']['time-to-first-byte']['rawValue']

                    #test['JsThread_score'] = data['audits']['mainthread-work-breakdown']['score']
                    #test['JsThread_rawValue'] = data['audits']['mainthread-work-breakdown']['rawValue']

                    #test['JsBootup_score'] = data['audits']['bootup-time']['score']
                    #test['JsBootup_rawValue'] = data['audits']['bootup-time']['rawValue']

                    #test['JsBootup_rawValue'] = data['audits']['bootup-time']['rawValue']

                    results.append(test)

    with open(resultDir+'/results.csv', 'w') as csvFile:
        #fields = ['name', 'date', 'scope', 'diagnostics_numRequests', 'diagnostics_numScripts', 'diagnostics_numStylesheets', 'diagnostics_numFonts', 'numTasks','numTasksOver10ms','numTasksOver25ms', 'numTasksOver50ms', 'numTasksOver100ms', 'numTasksOver500ms','rtt','maxServerLatency','totalByteWeight','totalTaskTime','mainDocumentTransferSize','speedIndex_score', 'speedIndex_rawValue','FCP_score','FCPrawValue', 'FMP_score','FMP_rawValue','TTFB_score', 'TTFB_rawValue','JsThread_score', 'JsThread_rawValue', 'JsBootup_score', 'JsBootup_rawValue']
        fields = ['name', 'date', 'scope', 'speedIndex', 'observedSpeedIndex', 'firstContentfulPaint', 'observedLoad','diagnostics_numRequests','rtt','maxServerLatency','totalByteWeight','totalTaskTime','mainDocumentTransferSize','speedIndex_score', 'speedIndex_rawValue','FCP_score','FCPrawValue', 'FMP_score','FMP_rawValue','TTFB_score', 'TTFB_rawValue',]
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

        print("writing completed")
        csvFile.close()

    df = pd.read_csv(resultDir+'/results.csv')

    #fig, ax = plt.subplots()
    #g = sns.barplot(x='name', y='speedIndex', hue='scope', data=df)

    def compareTest(aTests, df):
        #fig, ax = plt.subplot()
        df = df.loc[df['name'].isin(aTests)]
        df = df.sort_values(by=['scope'])
        ax = sns.barplot(x='scope', y=metric, hue='name', data=df)
        plt.xticks(rotation=90)
        fig = ax.get_figure()
        fig.set_size_inches(15, 10)
        fig.savefig(resultDir+'/output.png', dpi=400)

    compareTest(['vanilla', test], df)

if __name__ == "__main__":
    main(sys.argv[1:])
