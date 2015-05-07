__author__ = ''


class CadenceStaMaxQorData:
    pass


class CadenceStaMaxQor:
    @staticmethod
    def mathcLine(line, regex1):
        import re
        match_word = regex1.replace(" ", "[\s]*")
        line_variables = '.*(%s)[\s]*([-\d\.]*).*' % match_word
        result = re.search(line_variables, line)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        # close the file after reading the lines.
        f.close()
        data_items = []
        found_section = False
        sta_max_qor_data = CadenceStaMaxQorData()

        for line in lines:
            found_reg2reg_section = CadenceStaMaxQor.mathcLine(line, "Timing Path Group 'REG2REG' \(max_delay\/setup\)")
            found_crit_path = CadenceStaMaxQor.mathcLine(line, 'Critical Path Slack:')
            found_total_neg_slack = CadenceStaMaxQor.mathcLine(line, 'Total Negative Slack:')
            found_cell_count = CadenceStaMaxQor.mathcLine(line, 'Leaf Cell Count:')
            found_max_trans_count = CadenceStaMaxQor.mathcLine(line, 'max_transition Count:')
            found_max_cap_count = CadenceStaMaxQor.mathcLine(line, 'max_capacitance Count:')
            found_next_section = CadenceStaMaxQor.mathcLine(line, 'Timing Path Group')

            if found_reg2reg_section:
                found_section = True
            elif found_section:
                if found_crit_path:
                    sta_max_qor_data.found_crit_path = CadenceStaMaxQor.replace_space('sta max tttt REG2REG worst setup viols'), found_crit_path.group(2)
                    data_items.append(sta_max_qor_data.found_crit_path)
                elif found_total_neg_slack:
                    sta_max_qor_data.found_total_neg_slack = CadenceStaMaxQor.replace_space('sta max tttt REG2REG TNS'), found_total_neg_slack.group(2)
                    data_items.append(sta_max_qor_data.found_total_neg_slack)
                elif found_next_section:
                    found_section = False
            elif found_cell_count:
                sta_max_qor_data.found_cell_count = CadenceStaMaxQor.replace_space('sta Cell Count'), found_cell_count.group(2)
                data_items.append(sta_max_qor_data.found_cell_count)
            elif found_max_trans_count:
                sta_max_qor_data.found_max_trans_count = CadenceStaMaxQor.replace_space('sta max trans viols'), found_max_trans_count.group(2)
                data_items.append(sta_max_qor_data.found_max_trans_count)
            elif found_max_cap_count:
                sta_max_qor_data.found_max_cap_count = CadenceStaMaxQor.replace_space('sta max cap viols'), found_max_cap_count.group(2)
                data_items.append(sta_max_qor_data.found_max_cap_count)

        return data_items