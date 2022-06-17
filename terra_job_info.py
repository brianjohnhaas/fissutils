#!/usr/bin/env python3

from firecloud import fiss


import os, sys, re
import logging
import argparse
import pandas as pd

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description="get Terra job information", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--project", "-p",  dest="project", type=str, required=True, help="Terra project or namespace")

    parser.add_argument("--workspace", "-w",  dest="workspace", type=str, required=True, help="Terra workspace")

    parser.add_argument("--job_id", "-j", dest="job_id", type=str, required=False, help="provide details for job/submission id")

    parser.add_argument("--failures_to_sampleset", type=str, required=False, default=None, help="make a sampleset from the failed jobs")
    

    args = parser.parse_args()


    project = args.project
    workspace = args.workspace
    samplesetname = args.failures_to_sampleset

    if args.job_id:

        response = fiss.fapi.get_submission(project, workspace, args.job_id).json()
        df = pd.DataFrame(response["workflows"])
        if samplesetname:
            write_failure_sampleset(df, samplesetname)
        else:
            print(df.to_csv(sep="\t"))
            
        
    else:
        
        response = fiss.fapi.list_submissions(project, workspace).json()
        df = pd.DataFrame(response)
        print(df.to_csv(sep="\t"))


    sys.exit(0)



def write_failure_sampleset(df, samplesetname):

    print("\t".join(["membership:sample_set_id", "sample"]))
    
    df = df[ df['status'] != 'Succeeded' ]
    if len(df) > 0:
        for _, row in df.iterrows():
            jsinfo = row['workflowEntity']
            samplename = jsinfo['entityName']
            print("\t".join([samplesetname, samplename]))
        
    return



if __name__=='__main__':
    main()
