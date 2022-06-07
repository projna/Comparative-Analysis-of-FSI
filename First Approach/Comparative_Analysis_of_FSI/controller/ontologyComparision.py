import owlready2.entity
import shutup
from flask import render_template, request
from owlready2 import *
# from main import app
from flask import current_app
from controller import utils
import os


def spo_ontology_defintion(ontology, indicator):
    first_spo = []
    spodefinition = list(ontology.SPODefinition.subclasses())
    for spo in spodefinition:
        print(spo)
        if spo.commment[0] == indicator:
            first_spo.append(spo)
    return first_spo


def other_ontology_defintion(ontology, indicator):
    first_spo = []
    for i in ontology.classes():
        if len(i.label) > 0:
            if i.label[0] == indicator:
                first_spo.append(i)
    return first_spo


def indicator_validation(indicator):
    result = False
    spo_validation = []
    file_list = os.listdir('./ontology')
    for ls in file_list:
        temp_onto = get_ontology('./ontology/' + ls).load()
        if len(spo_validation) > 0:
            break
        print(temp_onto)
        if 'spo' in ls:
            spo_validation = spo_ontology_defintion(temp_onto, indicator)
        else:
            spo_validation = other_ontology_defintion(temp_onto, indicator)
    if len(spo_validation) > 0:
        print(indicator)
        result = True
    return result


def Comparision():
    first_spo = []
    second_spo = []
    comparative_type = current_app.config['COMPARATIVE_TYPE']
    ontologies = []
    spo_ontology = []
    filelist = os.listdir('./ontology')
    for ls in filelist:
        if 'spo' in ls:
            spo_ontology.append(True)
            print("SPO food")
        else:
            spo_ontology.append(False)
        temp_ontology = get_ontology('./ontology/' + ls)
        temp_ontology = temp_ontology.load()
        ontologies.append(temp_ontology)
    print(ontologies)
    print(spo_ontology)
    ############ information for ontologies ##########
    first_SPO_information = []
    second_SPO_information = []
    ##################################################
    if comparative_type == 'intra':
        if spo_ontology[0]:
            first_spo = spo_ontology_defintion(ontologies[0], current_app.config['INDICATOR_1'])
            second_spo = spo_ontology_defintion(ontologies[0], current_app.config['INDICATOR_2'])

        else:
            first_spo = other_ontology_defintion(ontologies[0], current_app.config['INDICATOR_1'])
            second_spo = other_ontology_defintion(ontologies[0], current_app.config['INDICATOR_2'])

    else:
        for i in range(0, 2):
            if spo_ontology[i]:
                print(str(i) + str(i) + str(i))
                print("From SPO")
                if len(first_spo) < 1:
                    first_spo = spo_ontology_defintion(ontologies[i], current_app.config['INDICATOR_1'])
                if len(second_spo) < 1:
                    second_spo = spo_ontology_defintion(ontologies[i], current_app.config['INDICATOR_2'])
                if len(first_spo) == 1:
                    first_SPO_information.append(ontologies[i])
                    first_SPO_information.append(spo_ontology[i])
                if len(second_spo) == 1:
                    second_SPO_information.append(ontologies[i])
                    second_SPO_information.append(spo_ontology[i])
            else:
                print(str(i) + str(i) + str(i))
                print("From Other")
                if len(first_spo) < 1:
                    first_spo = other_ontology_defintion(ontologies[i], current_app.config['INDICATOR_1'])
                if len(second_spo) < 1:
                    second_spo = other_ontology_defintion(ontologies[i], current_app.config['INDICATOR_2'])
                if len(first_spo) == 1:
                    first_SPO_information.append(ontologies[i])
                    first_SPO_information.append(spo_ontology[i])
                if len(second_spo) == 1:
                    second_SPO_information.append(ontologies[i])
                    second_SPO_information.append(spo_ontology[i])
    print(len(first_spo))
    print(len(second_spo))
    print(first_spo)
    print(second_spo)
    print(first_SPO_information)
    print(second_SPO_information)
    output_indicator_1_property = ""
    output_indicator_2_property = ""
    indicator1_matched_propery_output = {}
    indicator2_matched_propery_output = {}

    property_output = {}
    if len(first_spo) <= 0 or len(second_spo) <= 0:
        return False, property_output
        # return render_template('indicator.html',form=utils.IndicatorValidator())
    sp1_allproperty = []
    sp2_allproperty = []
    sp1_all_property_value_pair = {}
    sp2_all_property_value_pair = {}
    sp1_class_property = {}
    sp2_class_property = {}
    if comparative_type == 'intra':
        if spo_ontology[0]:
            sp1_allproperty, sp1_all_property_value_pair, sp1_class_property = extract_value_spo(ontologies[0],
                                                                                                 first_spo)
            sp2_allproperty, sp2_all_property_value_pair, sp2_class_property = extract_value_spo(ontologies[0],
                                                                                                 second_spo)
        else:
            sp1_allproperty, sp1_all_property_value_pair, sp1_class_property = extract_value(ontologies[0], first_spo)
            sp2_allproperty, sp2_all_property_value_pair, sp2_class_property = extract_value(ontologies[0], second_spo)
    else:
        if first_SPO_information[1]:
            sp1_allproperty, sp1_all_property_value_pair, sp1_class_property = extract_value_spo(
                first_SPO_information[0],
                first_spo)
        else:
            sp1_allproperty, sp1_all_property_value_pair, sp1_class_property = extract_value(
                first_SPO_information[0],
                first_spo)
        if second_SPO_information[1]:
            sp2_allproperty, sp2_all_property_value_pair, sp2_class_property = extract_value_spo(
                second_SPO_information[0], second_spo)
        else:
            sp2_allproperty, sp2_all_property_value_pair, sp2_class_property = extract_value(second_SPO_information[0],
                                                                                             second_spo)

    print("###############################################")
    # print(sp1_all_property_value_pair)
    # print(sp1_allproperty)
    # print(sp1_class_property)
    # print(sp2_all_property_value_pair)
    # print(sp2_allproperty)
    # print(sp2_class_property)
    print("################################################")
    matched_property = list(set(sp1_allproperty).intersection(sp2_allproperty))
    miss_property = list(
        set(sp1_allproperty).union(sp2_allproperty) - set(sp1_allproperty).intersection(sp2_allproperty))
    if current_app.config['METHOD'] == 'property':
        print('Property')
        property_output['indicator1'] = current_app.config['INDICATOR_1']
        property_output['indicator2'] = current_app.config['INDICATOR_2']

        output_indicator_1_property = indicator_property_set(sp1_class_property)
        output_indicator_2_property = indicator_property_set(sp2_class_property)
        indicator1_matched_propery_output = matched_property_subclass(matched_property, sp1_class_property)
        indicator2_matched_propery_output = matched_property_subclass(matched_property, sp2_class_property)
        indicator1_missed_property = missed_property_subclass(miss_property, sp1_class_property)
        indicator2_missed_property = missed_property_subclass(miss_property, sp2_class_property)
        property_output['output_indicator_1_property'] = output_indicator_1_property
        property_output['output_indicator_2_property'] = output_indicator_2_property
        property_output['matched_property'] = matched_property
        property_output['miss_property'] = miss_property
        property_output['indicator1_matched_propery_output'] = indicator1_matched_propery_output
        property_output['indicator2_matched_propery_output'] = indicator2_matched_propery_output
        property_output['indicator1_missed_property'] = indicator1_missed_property
        property_output['indicator2_missed_property'] = indicator2_missed_property
        property_output['missed_percentage'] = str(round(
            (len(miss_property) / (len(matched_property) + len(miss_property))) * 100, 2))
        property_output['matched_percentage'] = str(round(
            (len(matched_property) / (len(matched_property) + len(miss_property))) * 100, 2))
        print("##################################")
        print(len(matched_property))
        print(matched_property)
        print(len(miss_property))
        print(miss_property)
        print(str(round(
            (len(matched_property) / (len(matched_property) + len(miss_property))) * 100, 2)))
        print("##################################")

    else:
        property_output['indicator1'] = current_app.config['INDICATOR_1']
        property_output['indicator2'] = current_app.config['INDICATOR_2']
        property_output['indicator1_property_value'] = indicator_property_value_set(sp1_class_property,
                                                                                    sp1_all_property_value_pair)
        property_output['indicator2_property_value'] = indicator_property_value_set(sp2_class_property,
                                                                                    sp2_all_property_value_pair)
        match_property = []
        mismatch_property = []
        for value in matched_property:
            if sp2_all_property_value_pair.get(value) == sp1_all_property_value_pair.get(value):
                match_property.append(value)
            else:
                mismatch_property.append(value)
        property_output['match_property_value'] = match_property
        property_output['mismatch_property_value'] = mismatch_property
        property_output['miss_property_value'] = miss_property

        property_output['missed_percentage'] = str(round(
            (len(miss_property) / (
                    len(miss_property) + len(match_property) + len(mismatch_property))) * 100, 2))

        property_output['matched_percentage'] = str(round(
            (len(match_property) / (
                    len(miss_property) + len(match_property) + len(mismatch_property))) * 100, 2))

        property_output['mismatched_percentage'] = str(round(
            (len(mismatch_property) / (
                    len(miss_property) + len(match_property) + len(mismatch_property))) * 100, 2))

        property_output['indicator1_matched_property_value'] = property_value_output(match_property, sp1_class_property,
                                                                                     sp1_all_property_value_pair)
        property_output['indicator1_mismatched_property_value'] = property_value_output(mismatch_property,
                                                                                        sp1_class_property,
                                                                                        sp1_all_property_value_pair)
        property_output['indicator1_miss_property_value'] = missing_property_value_output(miss_property,
                                                                                          sp1_class_property,
                                                                                          sp1_all_property_value_pair)
        property_output['indicator2_matched_property_value'] = property_value_output(match_property, sp2_class_property,
                                                                                     sp2_all_property_value_pair)
        property_output['indicator2_mismatched_property_value'] = property_value_output(mismatch_property,
                                                                                        sp2_class_property,
                                                                                        sp2_all_property_value_pair)
        property_output['indicator2_miss_property_value'] = missing_property_value_output(miss_property,
                                                                                          sp2_class_property,
                                                                                          sp2_all_property_value_pair)
    return True, property_output


# return all matched subclass property pair of given indicator
def matched_property_subclass(match_property, spo_class_property):
    result_list = {}
    for match in match_property:
        temp_string = '| '
        for indicator in spo_class_property:
            for properties in spo_class_property.get(indicator):
                if properties == match:
                    temp_string = temp_string + str(indicator) + ' |'
        result_list[match] = temp_string
    # print(result_list)
    return result_list


# return all matched and mismatched subclass property pair of given indicator
def property_value_output(property_list, spo_class_property, property_value_pair):
    result_list = {}
    for prop in property_list:
        temp_string = '[ '
        for indicator in spo_class_property:
            for properties in spo_class_property.get(indicator):
                if properties == prop:
                    if len(property_value_pair.get(properties)) == 0:
                        temp_string = temp_string + str(
                            indicator) + '--->' + ' ' + properties + '  : ' + 'No Values' + '  ]  '
                    else:
                        temp_string = temp_string + str(
                            indicator) + '--->' + ' ' + properties + '  : ' + property_value_pair.get(properties) + \
                                      '  ]  '
        result_list[prop] = temp_string
    return result_list


# return all missing property and values

def missing_property_value_output(property_list, spo_class_property, property_value_pair):
    result_list = {}
    for prop in property_list:
        temp_string = '[ '
        flag = True
        for indicator in spo_class_property:
            for properties in spo_class_property.get(indicator):
                if properties == prop:
                    flag = False
                    if len(property_value_pair.get(properties)) == 0:
                        temp_string = temp_string + str(
                            indicator) + '--->' + ' ' + properties + '  : ' + 'No Values' + '  ]  '
                    else:

                        temp_string = temp_string + str(
                            indicator) + '--->' + ' ' + properties + '  : ' + property_value_pair.get(properties) + \
                                      '  ]  '
        if flag:
            temp_string = temp_string + ' Missing ]'
        result_list[prop] = temp_string
    return result_list


# return all missed subclass property pair of given indicator
def missed_property_subclass(miss_property, spo_class_property):
    result_list = {}
    for match in miss_property:
        temp_string = '| '
        flag = True
        for indicator in spo_class_property:
            for properties in spo_class_property.get(indicator):
                if properties == match:
                    flag = False
                    temp_string = temp_string + str(indicator) + ' |'
        if flag:
            temp_string = temp_string + ' Missing |'
        result_list[match] = temp_string
    # print(result_list)
    return result_list


# return all property of given indicator
def indicator_property_set(sp1_class_property):
    property_set = []
    for indicator in sp1_class_property:
        temp = ''
        temp = temp + str(indicator) + ' -> ['
        for value in sp1_class_property.get(indicator):
            temp = temp + ' ' + value
        temp = temp + '  ]'
        property_set.append(temp)
    print(property_set)
    return property_set


# return all property and their value of given indicator
def indicator_property_value_set(sp_class_property, all_property_value_pair):
    property_value_set = []
    for indicator in sp_class_property:
        temp_value_set = ''
        temp_value_set = temp_value_set + str(indicator) + ' --> ['
        for value in sp_class_property.get(indicator):
            if len(all_property_value_pair.get(value)) == 0:
                temp_value_set = temp_value_set + ' [' + value + ' : ' + "No Value" + ' ]'
            else:
                temp_value_set = temp_value_set + ' [' + value + ' : ' + all_property_value_pair.get(value) + ' ]'
        property_value_set.append(temp_value_set)
    # print(property_value_set)
    return property_value_set


def extract_value(ontology, spo):
    dcterms = ontology.get_namespace('http://purl.org/dc/terms/')
    dc = ontology.get_namespace('http://purl.org/dc/elements/1.1/')
    sp_allproperty = []
    sp_property = []
    sp_class_property = {}
    sp_all_property_value_pair = {}

    # print(list(spo[0].is_a))
    temp_list = []
    for ind11 in list(spo[0].is_a):
        list_property = []
        flag = True
        if isinstance_python(ind11, owlready2.entity.ThingClass):
            flag = False
            for i in list(ind11.get_properties(ind11)):
                if 'label' in str(i):
                    if len(ind11.label) > 0:
                        sp_allproperty.append(str(i))
                        sp_all_property_value_pair[str(i)] = ind11.label[0]
                        list_property.append(str(i))
                        # print(ind11)
                        # print(ind11.label[0])
                if 'comment' in str(i):
                    if len(ind11.comment) > 0:
                        sp_allproperty.append(str(i))
                        sp_all_property_value_pair[str(i)] = ind11.comment[0]
                        list_property.append(str(i))
                    print(i)
                if 'description' in str(i):
                    if len(dcterms.description[ind11]) > 0:
                        sp_allproperty.append(str(i))
                        sp_all_property_value_pair[str(i)] = dcterms.description[ind11][0]
                        temp_list.append((str(i)))
        else:
            temp = str(ind11).split('.')
            if len(temp) <= 2:
                key = temp[0] + '.' + temp[1]
                temp_list.append(key)
                sp_allproperty.append(key)
                sp_all_property_value_pair[key] = ""
            else:
                if 'om-1' in temp:
                    key = temp[0] + '.' + temp[1] + '.' + temp[2]
                    temp_list.append(key)
                    value = ""
                    for val in range(3, len(temp)):
                        value = value + temp[val] + " "
                    sp_allproperty.append(key)
                    sp_all_property_value_pair[key] = value
                else:
                    key = temp[0] + '.' + temp[1]
                    temp_list.append(key)
                    value = ""
                    for val in range(2, len(temp)):
                        value = value + temp[val] + " "
                    sp_allproperty.append(key)
                    sp_all_property_value_pair[key] = value
        if not flag:
            sp_class_property[ind11] = list_property
    for prop in list(spo[0].get_properties(spo[0])):
        # print(prop)
        if 'label' in str(prop):
            if len(spo[0].label) > 0:
                sp_allproperty.append(str(prop))
                sp_all_property_value_pair[str(prop)] = spo[0].label[0]
                temp_list.append(str(prop))
        if 'comment' in str(prop):
            if len(spo[0].comment) > 0:
                sp_allproperty.append(str(prop))
                sp_all_property_value_pair[str(prop)] = spo[0].comment[0]
                temp_list.append(str(prop))
        if 'description' in str(prop):
            if len(dcterms.description[spo[0]]) > 0:
                sp_allproperty.append(str(prop))
                sp_all_property_value_pair[str(prop)] = dcterms.description[spo[0]][0]
                temp_list.append((str(prop)))

    sp_class_property[spo[0]] = temp_list

    return sp_allproperty, sp_all_property_value_pair, sp_class_property


# Original One
def extract_value_spo(ontology, spo):
    dc = ontology.get_namespace('http://purl.org/dc/elements/1.1/')
    sp_allproperty = []
    sp_property = []
    sp_class_property = {}
    sp_all_property_value_pair = {}
    temp_dict = {}
    for ind11 in list(spo[0].subclasses()):
        temp = list(ind11.get_properties(ind11))
        temp_list = []
        for j in temp:
            if 'label' in str(j):
                if len(ind11.label) > 0:
                    sp_allproperty.append(str(j))
                    sp_all_property_value_pair[str(j)] = ind11.label[0]
                    temp_list.append(str(j))
            if 'comment' in str(j):
                if len(ind11.comment) > 0:
                    sp_allproperty.append(str(j))
                    sp_all_property_value_pair[str(j)] = ind11.comment[0]
                    temp_list.append(str(j))
            if 'description' in str(j):
                if len(dc.description[ind11]) > 0:
                    sp_allproperty.append(str(j))
                    sp_all_property_value_pair[str(j)] = dc.description[ind11][0]
                    temp_list.append(str(j))
        temp_dict[ind11] = temp_list
    print(temp_dict)
    for ind11 in list(spo[0].subclasses()):
        temp_list = []
        sp_property.append(ind11.is_a)
        for j in ind11.is_a:
            temp = str(j).split('.')
            if len(temp) <= 2:
                key = temp[0] + "." + temp[1]
                temp_list.append(key)
                sp_allproperty.append(key)
                sp_all_property_value_pair[key] = ""
            else:
                key = temp[0] + "." + temp[1]
                temp_list.append(key)
                value = ""
                for val in range(2, len(temp)):
                    value = value + temp[val] + " "
                sp_allproperty.append(key)
                sp_all_property_value_pair[key] = value
        print(ind11)
        if len(temp_dict.get(ind11)) > 0:
            for val in temp_dict.get(ind11):
                temp_list.append(val)
        sp_class_property[ind11] = temp_list
    return sp_allproperty, sp_all_property_value_pair, sp_class_property
