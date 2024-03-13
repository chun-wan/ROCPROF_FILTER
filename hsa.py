import time
import json
import argparse
"""
JSON_FILE_LIST={"JSON_FILE_0":"APP/GROMACS/adhd/0/adhd.json",
                "JSON_FILE_1":"APP/GROMACS/adhd/1/adhd.json",
                "JSON_FILE_2":"APP/GROMACS/adhd/2/adhd.json",
                "JSON_FILE_3":"APP/GROMACS/adhd/3/adhd.json"}
"""

JSON_FILE_LIST={"JSON_FILE_0":"results.json"}

def readAndMerge(np_size,outputName ):
    json_store_out = {}
    json_store_out["traceEvents"]=[]
    offset=0
    remove_hsa=1
    #import the partition
    for np_id in range(0, np_size):
        JSON_FILE_NAME = "JSON_FILE_" + str(np_id)

        #print(JSON_FILE_NAME)
        with open(JSON_FILE_LIST[JSON_FILE_NAME], 'r') as reader:
            json_new_list = []
            j_array = json.loads(reader.read())
            for j_idx in range(0, len(j_array['traceEvents'])):
                if 'args' in j_array['traceEvents'][j_idx].keys() and 'name' in j_array['traceEvents'][j_idx].keys():
                    if 'BeginNs' in j_array['traceEvents'][j_idx]['args'].keys():
                        if remove_hsa == True:
                            if "hsa_" not in j_array['traceEvents'][j_idx]['name'] :
                                  j_array['traceEvents'][j_idx]['args']['BeginNs'] = int(
                                      j_array['traceEvents'][j_idx]['args']['BeginNs']) - offset
                                  j_array['traceEvents'][j_idx]['args']['EndNs'] = int(
                                      j_array['traceEvents'][j_idx]['args']['EndNs']) - offset
                                  j_array['traceEvents'][j_idx]['ts'] = int(
                                      j_array['traceEvents'][j_idx]['args']['BeginNs'] / 1000)
                                  j_array['traceEvents'][j_idx]['dur'] = int(
                                      j_array['traceEvents'][j_idx]['args']['EndNs'] - j_array['traceEvents'][j_idx]['args'][
                                          'BeginNs']) / 1000
                                  json_new_list.append(j_array['traceEvents'][j_idx])

            json_store_out["traceEvents"] = json_store_out["traceEvents"] + json_new_list
    #TODO there is no debug information for NULL result.
    with open(outputName, 'w') as outfile:
        json.dump(json_store_out, outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--combine_file', help='Given a name for new json file..', default='combine.json', type=str)

    args = parser.parse_args()
    np_size=len(JSON_FILE_LIST)
    combine_file = args.combine_file
    readAndMerge(np_size,combine_file)

