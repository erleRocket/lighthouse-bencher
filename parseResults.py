#!/usr/bin/python

import os
import sys
import json
import re
import pandas as pd
import sys, getopt

resultDir = "/lighthouse_bench/reports/lighthouse-auto/"
results = []

fileName = sys.argv[1]

report = {}
parsedName = re.findall(r"([^-]+)-(\d+-?\d+)-([^_]+_?[^-]+)-.*", fileName)
if len(parsedName)>0:
    report['name'] = str(parsedName[0][0])
    report['date'] = parsedName[0][1]
    report['scope'] = str(parsedName[0][2])
    report['tags'] = report['scope'].split("_")

    with open(resultDir+fileName) as f:
        data = json.load(f)
        report['requestedUrl'] = data['requestedUrl']
        report['finalUrl'] = data['finalUrl']
        report['fetchTime'] = data['fetchTime']
        report['benchmarkIndex'] = data['environment']['benchmarkIndex']
        
        audits = data['audits']
        numRawSwicth = 'numericValue' if 'numericValue' in audits['speed-index'].keys() else 'rawValue'

        report['speedIndex_score'] = audits['speed-index']['score']
        report['speedIndex_numericValue'] = audits['speed-index'][numRawSwicth]
        report['FCP_score'] = audits['first-contentful-paint']['score']
        report['FCPnumericValue'] = audits['first-contentful-paint'][numRawSwicth]
        report['FMP_score'] = audits['first-meaningful-paint']['score']
        report['FMP_numericValue'] = audits['first-meaningful-paint'][numRawSwicth]
        report['TTFB_score'] = audits['time-to-first-byte']['score']
        report['TTFB_numericValue'] = audits['time-to-first-byte'][numRawSwicth]
        report['JsThread_score'] = audits['mainthread-work-breakdown']['score']
        report['JsThread_numericValue'] = audits['mainthread-work-breakdown'][numRawSwicth]
        report['JsBootup_score'] = audits['bootup-time']['score']
        report['JsBootup_numericValue'] = audits['bootup-time'][numRawSwicth]

        metrics = audits['metrics']
        metrics_item = metrics['details']['items'][0]
        report['firstContentfulPaint'] = metrics_item['firstContentfulPaint']
        report['firstMeaningfulPaint'] = metrics_item['firstMeaningfulPaint']
        report['firstCPUIdle'] = metrics_item['firstCPUIdle']
        report['interactive'] = metrics_item['interactive']
        report['speedIndex'] = metrics_item['speedIndex']
        report['estimatedInputLatency'] = metrics_item['estimatedInputLatency']
        report['observedNavigationStart'] = metrics_item['observedNavigationStart']
        report['observedNavigationStartTs'] = metrics_item['observedNavigationStartTs']
        report['observedFirstPaint'] = metrics_item['observedFirstPaint']
        report['observedFirstPaintTs'] = metrics_item['observedFirstPaintTs']
        report['observedFirstContentfulPaint'] = metrics_item['observedFirstContentfulPaint']
        report['observedFirstContentfulPaintTs'] = metrics_item['observedFirstContentfulPaintTs']
        report['observedFirstMeaningfulPaint'] = metrics_item['observedFirstMeaningfulPaint']
        report['observedFirstMeaningfulPaintTs'] = metrics_item['observedFirstMeaningfulPaintTs']
        report['observedTraceEnd'] = metrics_item['observedTraceEnd']
        report['observedTraceEndTs'] = metrics_item['observedTraceEndTs']
        report['observedLoad'] = metrics_item['observedLoad']
        report['observedLoadTs'] = metrics_item['observedLoadTs']
        report['observedDomContentLoaded'] = metrics_item['observedDomContentLoaded']
        report['observedDomContentLoadedTs'] = metrics_item['observedDomContentLoadedTs']
        report['observedFirstVisualChange'] = metrics_item['observedFirstVisualChange']
        report['observedFirstVisualChangeTs'] = metrics_item['observedFirstVisualChangeTs']
        report['observedLastVisualChange'] = metrics_item['observedLastVisualChange']
        report['observedLastVisualChangeTs'] = metrics_item['observedLastVisualChangeTs']
        report['observedSpeedIndex'] = metrics_item['observedSpeedIndex']
        report['observedSpeedIndexTs'] = metrics_item['observedSpeedIndexTs']

        diagnostics = audits['diagnostics']
        diagnostics_item = diagnostics['details']['items'][0]
        report['diagnostics_numRequests'] = diagnostics_item['numRequests']
        report['rtt'] = diagnostics_item['rtt']
        report['maxServerLatency'] = diagnostics_item['maxServerLatency']
        report['totalByteWeight'] = diagnostics_item['totalByteWeight']
        report['totalTaskTime'] = diagnostics_item['totalTaskTime']
        report['mainDocumentTransferSize'] = diagnostics_item['mainDocumentTransferSize']
        #report['diagnostics_numScripts'] = diagnostics_item['numScripts']
        #report['diagnostics_numStylesheets'] = diagnostics_item['numStylesheets']
        #report['diagnostics_numFonts'] = diagnostics_item['numFonts']
        #report['numTasks'] = diagnostics_item['numTasks']
        #report['numTasksOver10ms'] = diagnostics_item['numTasksOver10ms']
        #report['numTasksOver25ms'] = diagnostics_item['numTasksOver25ms']
        #report['numTasksOver50ms'] = diagnostics_item['numTasksOver50ms']
        #report['numTasksOver100ms'] = diagnostics_item['numTasksOver100ms']
        #report['numTasksOver500ms'] = diagnostics_item['numTasksOver500ms']

        results.append(report)


df = pd.DataFrame(results)
with open(resultDir+'/'+fileName.replace('.json','')+'-results.json', 'w') as outfile:
    for row in df.iterrows():
        row[1].to_json(outfile)
        outfile.write("\n")
