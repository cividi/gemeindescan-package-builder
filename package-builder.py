import json
import argparse
from ruamel import yaml
import warnings

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--project", required=False, help="Folder name/File name.yml")
ap.add_argument("-s", "--snapshot", required=False, help="Only generate named snapshot from project")

args = vars(ap.parse_args())

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

project = "sample-project" if args['project'] == None else args['project']
yml_file = project+"/"+project+".yml"

viewSpecKey = ["title","description","bounds","attribution"]
dpSpecKey = ["title","description","version","datapackage_version","gemeindescan_version","gemeindescan_meta","format","keywords","license","maintainers","contributors","sources"]

with open("template.yml", 'r', encoding="utf-8") as tf:
    template = yaml.load(tf)
    dp_template = template["snapshot"]
    legend_template = template["legend"]

try:
    with open(yml_file, 'r', encoding="utf-8") as fp:
        projectData = yaml.load(fp)
        for entries in projectData["snapshots"]:
            for name, snapshotData in entries.items():
                if (args['snapshot'] != None and name == args['snapshot']) or args['snapshot'] == None:
                    dp = dp_template.copy()
                    legends = []
                    dp["name"] = name
                    for key, d in snapshotData.items():
                        if key in dpSpecKey:
                            if isinstance(d, list):
                                dp[key] = d + dp[key]
                            else:
                                dp[key] = d
                        if key in viewSpecKey:
                            dp["views"][0]["spec"][key] = d
                        if key == "resources":
                            dpResources = []
                            for res in d:
                                for r, val in res.items():
                                    dpR = {}
                                    dpR["name"] = r
                                    resourcePath = project+"/data/"+r+".geojson"
                                    with open(resourcePath, 'r', encoding="utf-8") as rf:
                                        dpR["data"] = json.load(rf)
                                    dpR["mediatype"] = val["mediatype"]
                                    dpResources.append(dpR)
                            dp["resources"] = dpResources + dp["resources"]
                            resource_flatlist = [d["name"] for d in dp["resources"]]
                            dp["views"][0]["resources"] = resource_flatlist

                            for item in resource_flatlist:
                                if item in projectData["legends"]:
                                    for label, legendSymbol in projectData["legends"][item].items():
                                        tmp_legend = legend_template.copy()
                                        tmp_legend["label"] = label
                                        for styleKey, styleValue in legendSymbol.items():
                                            tmp_legend[styleKey] = styleValue
                                        legends.append(tmp_legend.copy())
                            dp["views"][0]["spec"]["legend"] = legends

                    dp_file = project+"/snapshots/"+name+".json"
                    with open(dp_file + "", 'w') as outfile:
                        json.dump(dp, outfile)
                        print("🎉 Sucessfully written ",dp_file)
                else:
                    print("❌ Snapshot '"+args["snapshot"]+"' not found in "+project+".yml")
except:
    print("❌ Project '"+project+"' YML ("+project+"/"+project+".yml) not found.")