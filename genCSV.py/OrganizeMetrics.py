__author__ = 'tjstickx'


class OrganizeFoundMetrics:
    @staticmethod
    def add_missing_metrics(metric_collections, test_case, tool):
        import json
        metric_names = []
        new_metrics_collections = []
        # Open the JSON file and get the default list of metrics
        with open(r'config.json', 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            default_metric_names = json_data['default_list_of_metrics']
        # Add each metric name that was captured from parsing the files to the list metric_names
        metric_name = 0
        for metric_collection in metric_collections:
            # Because metric_collection is a list that might have different lengths we use range(len(metric_collection))
            # in the following for loop
            for metric_pair in range(len(metric_collection)):
                metric_names.append(metric_collection[metric_pair][metric_name])
        for default_metric_name in default_metric_names:
            if default_metric_name not in metric_names:
                # '\t' is the default value for blank metrics
                new_metric = default_metric_name, "\t"
                new_metrics_collections.append(new_metric)
        metric_collections.append(new_metrics_collections)
        temp_metric_collections = OrganizeFoundMetrics.sort_metrics(metric_collections, test_case, tool)
        return temp_metric_collections

    # This method is used to add the metrics that don't appear after parsing the required files
    @staticmethod
    def sort_metrics(metric_collections, test_case, tool):
        import os
        from datetime import datetime
        from operator import itemgetter
        temp_metric_collections, syn, apr, calibre, drc, pv_max, pv_min, pv_power, pv_noise, sta = [], [], [], [], [], [], [], [],[],[]
        # metric_pairs = [GetSynopsysMetrics.MetricPair("syn", syn), GetSynopsysMetrics.MetricPair("apr", apr),
        #                 GetSynopsysMetrics.MetricPair("drc", drc),  GetSynopsysMetrics.MetricPair("pv_max", pv_max),
        #                 GetSynopsysMetrics.MetricPair("pv_min", pv_min),
        #                 GetSynopsysMetrics.MetricPair("pv_power", pv_power),
        #                 GetSynopsysMetrics.MetricPair("pv_noise", pv_noise),
        #                 ]
        metric_collections = filter(None, metric_collections)
        metric_count = 0
        metric_name = 0
        # This loop is to arrange the files in the correct order
        for metric_collection in metric_collections:
            # Metric_collection needs to be converted to list/tuple from a object reference
            metric_list = tuple(metric_collection)
            for metric_pair in range(len(metric_list)):
                metric_count += 1
                if "syn" in metric_list[metric_pair][metric_name]:
                    syn.append(metric_list[metric_pair])

                elif "apr" in metric_list[metric_pair][metric_name]:
                    apr.append(metric_list[metric_pair])

                elif "drc" in metric_list[metric_pair][metric_name]:
                    drc.append(metric_list[metric_pair])

                elif "pv_max" in metric_list[metric_pair][metric_name]:
                    pv_max.append(metric_list[metric_pair])

                elif "pv_min" in metric_list[metric_pair][metric_name]:
                    pv_min.append((metric_list[metric_pair]))

                elif "pv_power" in metric_list[metric_pair][metric_name]:
                    pv_power.append((metric_list[metric_pair]))

                elif "pv_noise" in metric_list[metric_pair][metric_name]:
                    pv_noise.append((metric_list[metric_pair]))

                elif "calibre" in metric_list[metric_pair][metric_name]:
                    calibre.append(metric_list[metric_pair])
                elif "sta" in metric_list[metric_pair][metric_name]:
                    sta.append(metric_list[metric_pair])
                # for metric_pair in metric_pairs:
                #     metric_count += 1
                #     if(GetSynopsysMetrics.organize_metrics(metric_pair.metric_pair, metric_list[metric_pair][0],
                #                                            metric_list, metric_pair.state_list)):
                #         break

                # if GetSynopsysMetrics.organize_metrics("syn", metric_list[metric_pair][0],  metric_list, syn):
                #     continue
                #

        print(metric_count)
        # If the file name given ends with a / or a \ then os.path.basename() would return "" therefore we do the
        # following "if" statements when gathering the test case name and the kit name
        if os.path.basename(test_case) != "":
            test_case_name = os.path.basename(test_case)
            kit_name = os.path.basename(os.path.dirname(test_case))
        else:
            test_case_name = os.path.basename(os.path.dirname(test_case))
            kit_name = os.path.basename(os.path.dirname(os.path.dirname(test_case)))

        default_metrics_collection = [("Testcase_Name", test_case_name), ("kit", kit_name),
                                      ("DateTime", str(datetime.now())), ("Tool", tool)]
        temp_metric_collections = [default_metrics_collection, tuple(sorted(syn, key=itemgetter(0))),
                                   tuple(sorted(apr, key=itemgetter(0))), tuple(sorted(drc, key=itemgetter(0))),
                                   tuple(sorted(calibre, key=itemgetter(0))), tuple(sorted(pv_max, key=itemgetter(0))),
                                   tuple(sorted(pv_min, key=itemgetter(0))), tuple(sorted(pv_power, key=itemgetter(0))),
                                   tuple(sorted(pv_noise, key=itemgetter(0))), tuple(sorted(sta, key=itemgetter(0)))]

        return temp_metric_collections

    # # The last two methods are for future refactoring
    # @staticmethod
    # def organize_metrics(match_metric_name, metric_name, metric_names, stage_list):
    #     result = False
    #
    #     if match_metric_name in metric_names[metric_name][0]:
    #         stage_list.append(metric_names[metric_name])
    #         result = True
    #
    #     return result
    #
    # class MetricPair:
    #     def __init__(self, metric_name, state_list):
    #         self.metric_name = metric_name
    #         self.state_list = state_list