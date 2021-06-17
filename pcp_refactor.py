import pyperclip
from typing import List, Dict
import collections
import copy
from doctordata import Doctor
import json
import pprint
import re
from difflib import get_close_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import htmlGen4
import html_utilities

pcp_data_file = 'dat/pcp.txt'
tag = htmlGen4.create_html_object


def any_item_found(search_list: List, data_to_search: List):
    return any(ele in data_to_search for ele in search_list)


def item_found(item_to_match, data_to_search):
    return item_to_match in data_to_search


def filter_match_item(lines, match_item):
    return [line for line in lines if not item_found(match_item, line)]


def filter_multi_match_items(lines, search_list):    
    return [line for line in lines if not any_item_found(search_list, line)]


def match_partial(text, *match_items):
    for item in match_items:
        if item_found(item, text): 
            return True
    return False


def split_string_into_lines(data):
    return data.splitlines()


def read_data(data_file):
    with open(data_file, 'r') as file:
        return file.read()


def merge_found_item_from_next_line(item_list, lines):
    i = 1
    max_iters = len(lines)
    merged_list = [lines[0]]
    while i < max_iters:
        current_string = lines[i]
        found_item = any_item_found(item_list, current_string)
        if(found_item):
            merged_list[-1] += " " + current_string
        else:
            merged_list.append(current_string)
        i += 1
    return merged_list


def find_regex(pattern, test_string):
    if re.search(pattern, test_string):
        return True
    else:
        return False


def merge_not_found_item(regex_pattern, lines):
    i = 1
    max_iters = len(lines)
    merged_list = [lines[0]]
    while i < max_iters:
        current_string = lines[i]
        found_item = find_regex(regex_pattern, current_string)
        if not found_item:            
            merged_list[-1] += " " + current_string
        else:
            merged_list.append(current_string)
        i += 1
    return merged_list


def group_doctor_info(lines, regex_pattern, prefix_sep="", suffix_sep=""):
    merged_list = []
    for i in range(len(lines)):
        current_string = lines[i]
        found_item = find_regex(regex_pattern, current_string)
        if found_item:
            merged_list.append([current_string])
            # merged_list.append(current_string + suffix_sep)
        else:
            # merged_list[-1] += prefix_sep + current_string + suffix_sep
            merged_list[-1].append(current_string)
    return merged_list


def doctor_info_as_text(doc_obj):
    return ("{}\n{}")


def doctor_lines_to_dict(doctor_lines, separator):
    name = doctor_lines.pop(0)
    credentials = doctor_lines.pop(0)
    practice = doctor_lines.pop(0)
    phone_num = doctor_lines.pop(-1)
    address = separator.join(doctor_lines)
    doctor_dict = {'name': name, 'credentials': credentials,
                   'phone_num': phone_num, 'address': address,
                   'practice': practice}
    return doctor_dict


def create_Doctor_obj_from_list(grouped_doctor_data_as_list, id_num, separator=" "):    
    this_doc = Doctor()
    this_doc.id_num = id_num
    this_doc.name = grouped_doctor_data_as_list.pop(0)
    this_doc.credentials = ((grouped_doctor_data_as_list.pop(0)).split(", "))
    this_doc.practice = grouped_doctor_data_as_list.pop(0)
    this_doc.phone_num = grouped_doctor_data_as_list.pop(-1)
    this_doc.address = separator.join(grouped_doctor_data_as_list)    
    return this_doc


def remove_string_from_list(lines, string_to_replace, replacement):
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace(string_to_replace, replacement)


def remove_duplicate_practices():
    practices = []
    for curr_doctor in doctors:
        if curr_doctor.practice not in practices:
            practices.append(curr_doctor.practice)
    return practices
    pp.pprint(practices)


def final_data_cleanup(this_list):
    for item in this_list:
        remove_string_from_list(item, '? ', '')
    return this_list

def merge_lists(*lists):
    merged_list = []
    for this_list in lists:
        merged_list += this_list            
    return merged_list


def remove_list_duplicates(this_list):
    return list(set(this_list))


def update_list_no_dupls(item, list_to_update):
    if not item_found(item, list_to_update):
        list_to_update.append(item)
    remove_list_duplicates(list_to_update)
    list_to_update.sort()


def convert_list_to_dict(lst, default_factory):
    return {value: default_factory() for value in lst}


def new_collection(item, item_type):
    return item_type(item)


def merge_sets_until_equal(this_set, merged_set, this_dict):
    for item in this_set:
        merged_set.update(this_dict['{}'.format(item)])        
    if this_set != merged_set:        
        # if the set gets larger as result of updates, 
        # it means some matches are missing in the original set.
        # Update the original set and do it again with the new list

        # TODO: try to find a way to remove the already checked items
        # and do it over with only the new items
        this_set.update(merged_set)
        merge_sets_until_equal(this_set, merged_set, this_dict)
    else:
        print("equal")


def initialize_html_list():
    html_list = htmlGen4.new_html_document()
    tag(html_list, 'meta', 'head', [{'charset': 'utf-8'}])
    tag(html_list, 'link', 'head', [{'rel': 'stylesheet'},
        {'type': 'text/css'}, {'href': 'normalize.css'}])
    tag(html_list, 'link', 'head', [{'rel': 'stylesheet'},
        {'type': 'text/css'}, {'href': 'css\\styles.css'}])
    tag(html_list, 'title', 'head', [], ("Doctors"))
    return html_list

def outputHTMLDocument(htmlDocument, fileName):
    htmlDoc = open('%s%s.html' % (htmlExportPath, fileName), 'w')
    numBytes = htmlDoc.write(htmlDocument)  # Just to stifle the return
    print('Created HTML Document at %s%s.html' % (htmlExportPath, fileName))
    htmlDoc.close()

htmlExportPath = 'E:\\export\\'



def main():
    pp = pprint.PrettyPrinter()
    data = read_data(pcp_data_file)
    search_list = ["Closest Location", "View Details ", " of 703"]
    split_data = split_string_into_lines(data)
    split_data = filter_multi_match_items(split_data, search_list)
    addr_strings = ["(PCP)", "Floor", "Apartment", "Suite", "HT-", "HT4", 
                    "Room 307", "Room 1C3", "Room 018", "Room A1-19", "M506", 
                    "of Medicine F"]  # Merge Extra like PCPs/Address Data
    split_data = merge_found_item_from_next_line(addr_strings, split_data)      
    split_data = merge_not_found_item(r'\s', split_data)  # Remove Orphan Lines
    grouped_doctors_list = group_doctor_info(split_data, r'\? ', "", "\n")
    # grouped_doctors_as_lines = split_string_into_lines(grouped_doctors_list[0])
    doctor_dict_list = []
    doctor_objs = []  
    grouped_doctors_list = final_data_cleanup(grouped_doctors_list)

    for i in range(len(grouped_doctors_list)):
        doctor_obj = create_Doctor_obj_from_list(grouped_doctors_list[i], i)
        doctor_objs.append(doctor_obj)
        doctor_dict_list.append(doctor_obj.to_dict())
    
    full_id_list = list(range(len(doctor_objs)))
    list_of_doctor_objs = copy.deepcopy(doctor_objs)

    practice_list = []
    for doc_object in list_of_doctor_objs:
        practice_list.append(doc_object.practice)
    
    
    
    practice_list.sort()
    # print(practice_list)
     # print(str(len(practice_list)))
    practice_dict = convert_list_to_dict(practice_list, set)
    practice_list = remove_list_duplicates(practice_list)
    practice_list.sort()
    print(len(practice_dict))


    html_list = initialize_html_list()

    practice_set = set()
    practice_dicts = collections.defaultdict(list)
    for doc_object in list_of_doctor_objs:
        practice_name = str(doc_object.practice)
        practice_dicts[practice_name].append(doc_object)

    sorted_practices = list(practice_dicts.keys())
    sorted_practices.sort()

    for a_practice in sorted_practices:
        tag(html_list, 'br', 'body')
        convert_to_google_search(html_list, a_practice)
        tag(html_list, 'h1', 'a', [{'class': 'practice'}],
            '{}'.format(a_practice)) #nesting within the just created a tag from #convert_to_google_search
        doctor_name_list = list()
        doc_info_list = list()
        tag(html_list, 'ul', 'body', [{'class': 'pcp-list'}])
        for a_doctor in practice_dicts[a_practice]:
            doctor_name_list.append(a_doctor.name)
            doc_info = '\n'
            for cred in a_doctor.credentials:
                doc_info += cred + "\n"
            doc_info += a_doctor.address + "\n"
            doc_info += a_doctor.phone_num + "\n\n"
            doc_info_list.append(doc_info)
        # a_practice_doctor_name_list.sort()
        for i, doc_name in enumerate(doctor_name_list):
            tag(html_list, 'li', 'ul', [{'class': 'pcp-item'}])
            convert_to_google_search(html_list, doc_name, 'li', doc_name)
            tag(html_list, 'span', 'li', [{'class': 'doc-info'}], doc_info_list[i].replace('\n','<br>'))


    htmlDocument = htmlGen4.parseHtmlDocumentList(html_list)
    outputHTMLDocument(htmlDocument, "pcps")



def convert_to_google_search(html_list, link_text, destination='body', content=''):
    google_search_query = "http://google.com/search?q="
    tag(html_list, 'a', destination, [{'href': google_search_query + '{}'.format(link_text)},
        {'target': '_blank'}], content)


if __name__ == "__main__":
    main()
