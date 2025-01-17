import copy
from pandas import DataFrame
import random
import numpy as np


def find_node_by_id(all_nodes, id):
    for n in all_nodes:
        if id == n.id:
            return n


def split_recursive(string, father_diff_par):
    arguments = []
    arg = ''
    offset = 0
    off = 0
    diff_num_parentesis = string.count(')') - string.count('(') - 1
    for idx in range(len(string)):
        current_idx = idx + offset
        if current_idx >= len(string):
            break
        char = string[current_idx]
        if char != '(' and char != "," and char != ')':
            arg += char
            off += 1
        elif char == ',':
            arguments.append(arg)
            off += 1
            arg = ''
        elif char == '(':
            nau, new_offset = split_recursive(string[current_idx + 1:], diff_num_parentesis)
            offset += new_offset
            off += new_offset + 1
            arg = nau
        elif char == ')':
            if diff_num_parentesis > father_diff_par:
                arguments.append(arg)
                break
            else:
                diff_num_parentesis -= 1
                arguments.append(arg)

    return arguments, off + 1


def split_composed_arguments(string):
    parentesis_count = 0
    composed_arguments = []
    start = 0
    end = 0
    for idx, char1 in enumerate(string):
        if char1 == '(':
            parentesis_count += 1
        elif char1 == ')':
            parentesis_count -= 1
            if parentesis_count == 0:
                end = idx + 1
                comp_arg = string[start:end]
                comp_arg = remove_first_last_space(comp_arg)
                composed_arguments.append(comp_arg)
                start = idx + 1
    return composed_arguments


def replace_nodes(all_nodes, fast_dict_search):
    """
    Replace the arguments of the ID of neighbor nodes with the neighbor nodes themselves. 
    This creates edges in the graph.
    
    Args:
        all_nodes: List of FlatNodes with IDs of their neighbor nodes in the `parameters` fields.
        fast_dict_search: Dictionary mapping IDs (e.g., '#1234') to node objects.
    """
    def normalize_key(key):
        """Normalize keys by stripping whitespace."""
        return key.strip() if isinstance(key, str) else key

    for node in all_nodes:
        for i1, par1 in enumerate(node.parameters):
            if isinstance(par1, str) and len(par1) > 0 and par1[0] == '#':
                key = normalize_key(par1)  # Normalize the key
                if "-" not in key:  # Check for valid IDs
                    if key in fast_dict_search:
                        node.parameters[i1] = fast_dict_search[key]
                    else:
                        print(f"Warning: ID '{key}' not found in fast_dict_search")
                else:
                    print(f"Weird ID format: '{key}'")
            elif isinstance(par1, list):
                for i2, par2 in enumerate(par1):
                    if isinstance(par2, str) and len(par2) > 0 and par2[0] == '#':
                        key = normalize_key(par2)  # Normalize the key
                        if key in fast_dict_search:
                            node.parameters[i1][i2] = fast_dict_search[key]
                        else:
                            print(f"Warning: ID '{key}' not found in fast_dict_search")
                    elif isinstance(par2, list):
                        for i3, par3 in enumerate(par2):
                            if isinstance(par3, str) and len(par3) > 0 and par3[0] == '#':
                                key = normalize_key(par3)  # Normalize the key
                                if key in fast_dict_search:
                                    node.parameters[i1][i2][i3] = fast_dict_search[key]
                                else:
                                    print(f"Warning: ID '{key}' not found in fast_dict_search")


def hyphen_split(string, split_word, num_occurance=2):
    if string.count(split_word) == 1:
        return string.split(split_word)[0]
    splitted = string.split(split_word, num_occurance)
    first = split_word + splitted[1]
    second = splitted[2]
    return [first, second]


def histogram_intersection(h1, h2):
    sm = 0
    sum1 = sum(h1.values())
    sum2 = sum(h2.values())
    all_keys = set(h1.keys())
    all_keys.add(k for k in h2.keys())
    for k in all_keys:
        v1, v2 = 0, 0
        if k in h1.keys():
            v1 = h1[k]/sum1
        if k in h2.keys():
            v2 = h2[k]/sum2
        sm += min(v1, v2)
    return sm


def remove_first_last_space(string):
    fixed_string = string
    if fixed_string[0] == " ":
        fixed_string = fixed_string[1:]
    if fixed_string[-1] == " ":
        fixed_string = fixed_string[:-1]
    return fixed_string


def make_schema(matrix, names):
    schema = DataFrame(matrix)
    schema.columns = [n for n in names]
    schema.index = [n for n in names]
    print(schema)
    return schema


def split_training_testset(all_set, perc, shuffle=True):
    all_set = copy.deepcopy(all_set)
    num_elem = len(all_set)
    num_train_elem = int(num_elem * perc)
    num_test_elem = num_elem - num_train_elem
    new_set = all_set
    if shuffle:
        new_set = copy.deepcopy(all_set)
        random.shuffle(new_set)
    training_set = new_set[:num_train_elem]
    test_set = new_set[-num_test_elem:]

    # print("\nTrainset dim: " + str(num_train_elem))
    # print("Testset dim: " + str(num_test_elem))
    # print()

    return training_set, test_set


