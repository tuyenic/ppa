__author__ = ''


class CadenceMetric:
    @staticmethod
    def get_cadence_metrics(list_of_files, test_case, tool):
        from Metrics.OrganizeMetric import OrganizeMetric
        from FileParsers.Cadence.QorReportCad import CaQorReport
        from FileParsers.Cadence.RunTime import CaRunTime
        from FileParsers.Cadence.StaMaxQor import StaMaxQor
        from FileParsers.Cadence.StaMinQor import StaMinQor
        from FileParsers.Cadence.CalibreErrors import CalibreErrors
        from FileParsers.Cadence.AprRunLog import AprRunLog
        from FileParsers.DynamicParser import DynamicParser
        # from FileParsers.Cadence.SignOffSum import CadenceSignOffSum
        from FileParsers.Cadence.GateCount import CadenceGateCount
        # fromFileParsers.Cadence.PowerReport import CadencePowerRpt
        # from FileParsers.Cadence.Violations import CadenceViolations
        metric_collections = []

        for file in list_of_files:
            if file.endswith('.qor.rpt'):
                if 'reports_max' in file:
                    sta_max_qor = StaMaxQor.search_file(file)
                    metric_collections.extend(sta_max_qor)
                elif 'reports_min' in file:
                    sta_min_qor = StaMinQor.search_file(file)
                    metric_collections.extend(sta_min_qor)
                elif '.final.qor.rpt' in file:
                    cadence_qor = CaQorReport.search_file(file)
                    metric_collections.extend(cadence_qor)
            elif file.endswith('sta.max.log'):
                cadence_runtime = CaRunTime.search_file(file)
                metric_collections.extend(cadence_runtime)
            elif file.endswith('drc.sum'):
                calibre_errors = CalibreErrors.search_file(file)
                metric_collections.extend(calibre_errors)
            elif file.endswith("lvs.report"):
                calibre_fail_errors = CalibreErrors.search_file(file)
                metric_collections.extend(calibre_fail_errors)
            elif file.endswith('apr_run.log'):
                apr_run_log = AprRunLog.search_file(file)
                metric_collections.extend(apr_run_log)
            elif file.endswith('block_stats_signoff.rpt'):
                gate_count = CadenceGateCount.search_file(file)
                metric_collections.extend(gate_count)
            else:
                metric_collections.extend(DynamicParser.search_file(file, tool))

            # elif file.endswith('post_route_hold_optDesign.summary'):
            #     route_design = CadenceSignOffSum.search_file(file)
            #     metric_collections.append(route_design)
            # elif file.endswith('signoff.power.rpt'):
            #     pwr_rpt_data = CadencePowerRpt.search_file(file)
            #     metric_collections.append(pwr_rpt_data)
            # elif file.endswith('.final.all_violators.rpt'):
            #     cadence_violations = CadenceViolations.search_file(file)
            #     metric_collections.append(cadence_violations)


        temp_metric_collections = OrganizeMetric.add_missing_metrics_old(metric_collections, test_case, tool)

        return temp_metric_collections
