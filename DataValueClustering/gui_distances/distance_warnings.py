import re

import numpy as np

from gui_distances.costmapinput_helper import regex_alphabet, regex_alphabet_capitalized, regex_digits, \
    regex_alphabet_pure, regex_alphabet_capitalized_pure, regex_digits_pure
from gui_general import CreateToolTip


WARNING_REDUNDANT_1 = "Warning: The following characters are already contained in this or a previous group: "
WARNING_REDUNDANT_2 = ". Only their first occurrence will have an impact on the dissimilarities."
WARNING_UNDEFINED_1 = "Warning: The following characters do not occur in the abstracted data values: "
WARNING_UNDEFINED_2 = ". Thus, their weights will have no impact on the dissimilarities."
warning_color = "#ffbb00"


def create_array_of_empty_lists(n):
    arr = np.empty(n, dtype=object)
    arr[...] = [[] for _ in range(arr.shape[0])]
    return arr


def redundant_char_warning(entry):
    entry.configure(highlightbackground=warning_color, highlightcolor=warning_color)


def update_label_text(char, label, mapping):
    string = label.cget("text")
    if string != "":
        string += "\n"
    string += "'" + char + "' - " + mapping
    label.config(text=string)


def undefined_char_warning(entry):
    entry.configure(highlightbackground=warning_color, highlightcolor=warning_color)


def update_warning_for_entry(i, tool_tips_entries, redundant_chars_per_entry,
                             undefined_chars_per_entry):
    if undefined_chars_per_entry[i]:
        if tool_tips_entries[i] != "":
            tool_tips_entries[i] += "\n"
        tool_tips_entries[i] += WARNING_UNDEFINED_1 + str(set(undefined_chars_per_entry[i])) + WARNING_UNDEFINED_2
    if redundant_chars_per_entry[i]:
        if tool_tips_entries[i] != "":
            tool_tips_entries[i] += "\n"
        tool_tips_entries[i] += WARNING_REDUNDANT_1 + str(set(redundant_chars_per_entry[i])) + WARNING_REDUNDANT_2


def redundant_char_warning_global(label_warning, redundant_chars):
    warning_text = label_warning["text"]
    new_warning = "Warning: The following characters are specified multiple times: " + str(redundant_chars) + ". Only their first occurrence will have an impact on the dissimilarities."
    if warning_text is not None and warning_text != "":
        label_warning.configure(text=warning_text + "\n" + new_warning, bg=warning_color, borderwidth=1)
    else:
        label_warning.configure(text=new_warning, bg=warning_color, borderwidth=1)


def undefined_char_warning_global(label_warning, undefined_chars):
    warning_text = label_warning["text"]
    new_warning = "Warning: The following characters do not occur in the abstracted data values: " + str(undefined_chars) +". Thus, their weights will have no impact on the dissimilarities."
    if warning_text is not None and warning_text != "":
        label_warning.configure(text=warning_text + "\n" + new_warning, bg=warning_color, borderwidth=1)
    else:
        label_warning.configure(text=new_warning, bg=warning_color, borderwidth=1)


def update_global_warning(label_warning, redundant_chars_per_entry, undefined_chars_per_entry):
    label_warning.configure(text="")
    redundant_chars = set([item for sublist in redundant_chars_per_entry for item in sublist])
    undefined_chars = set([item for sublist in undefined_chars_per_entry for item in sublist])
    if undefined_chars:
        undefined_char_warning_global(label_warning, undefined_chars)
    if redundant_chars:
        redundant_char_warning_global(label_warning, redundant_chars)


def detect_undefined_chars_in_entry(chars_in_abstraction, entry):
    undefined_chars = list()
    for j, char in enumerate(entry.get()):
        if not char in chars_in_abstraction:
            undefined_chars.append(char)
            undefined_char_warning(entry)
    return undefined_chars


def hide_all_tool_tips(tooltips):
    for tip in tooltips:
        if tip is not None:
            tip.hidetip()
    tooltips = list()


def set_tool_tips(tooltips, entrylist, label_list, n, tool_tips_abstraction_info, tool_tips_warning, omit_first):
    hide_all_tool_tips(tooltips)
    for i in range(0, n):
        if i == 0 and omit_first:
            tooltips.append(CreateToolTip(entrylist[i], "This row contains the weights for the insertion of characters."))
        elif i == n - 1:
            tooltips.append(CreateToolTip(entrylist[i], "<rest> represents all characters not covered above."))
        else:
            tooltips.append(CreateToolTip(entrylist[i], tool_tips_warning[i], color=warning_color if tool_tips_warning[i].startswith("Warning") else None))
        tooltips.append(CreateToolTip(label_list[i], tool_tips_abstraction_info[i]))


def undo_highlight_entries(entrylist, label_warning):
    for i, entry in enumerate(entrylist):
        entry.configure(highlightbackground="white", highlightcolor="white")
    label_warning.configure(text="", bg="white", borderwidth=0)


def update_warnings_vars(entry_list, label_warning, n, label_list, abstraction, tooltips, start_index, entry_var_list, disable_input=None, enable_input=None, omit_first=False):
    update_warnings(entry_list, label_warning, n, label_list, abstraction, tooltips, start_index, entry_var_list=entry_var_list, disable_input=disable_input, enable_input=enable_input, regex_index=None, text=None, omit_first=omit_first)


def update_warnings_no_vars(entry_list, label_warning, n, label_list, abstraction, tooltips, start_index, regex_index, text, disable_input=None, enable_input=None, omit_first=False):
    update_warnings(entry_list, label_warning, n, label_list, abstraction, tooltips, start_index, entry_var_list=None, disable_input=disable_input, enable_input=enable_input, regex_index=regex_index, text=text, omit_first=omit_first)


def update_warnings(entry_list, label_warning, n, label_list, abstraction, tooltips, start_index, entry_var_list=None, disable_input=None, enable_input=None, regex_index=None, text=None, omit_first=False):
    undo_highlight_entries(entry_list, label_warning)
    tool_tips_labels = np.full(n, "").tolist()
    tool_tips_entries = np.full(n, "").tolist()
    for st in label_list:
        st.config(text="")
    chars_in_abstraction = [item for mapping in abstraction for item in list(mapping[1])]
    redundant_chars_per_entry = create_array_of_empty_lists(n)
    undefined_chars_per_entry = create_array_of_empty_lists(n)
    for l, mapping in enumerate(abstraction):
        for j, abstraction_char in enumerate(mapping[1]):
            abstraction_char_occurred = False
            for i, entry in enumerate(entry_list):
                if text is not None:
                    value = text if i == regex_index else entry.get()
                else:
                    value = entry_var_list[i].get()
                if i < len(entry_list) - 1 and i >= start_index:
                    if value == "":
                        if disable_input is not None:
                            disable_input(i)
                        tool_tips_entries[i] = "This row will be ignored as its entry is empty."
                        tool_tips_labels[i] = "This row will be ignored as its entry is empty."
                    else:
                        if enable_input is not None:
                            enable_input(i)
                        for k, entry_char in enumerate(value):
                            enum_match = False
                            if 0 < k < len(value) - 1:
                                s = value[k - 1] + entry_char + value[k + 1]
                                match_alphabet = re.search(regex_alphabet_pure, s)
                                match_alphabet_capitalized = re.search(regex_alphabet_capitalized_pure, s)
                                match_digits = re.search(regex_digits_pure, s)
                                enum_match = not (match_alphabet is None and match_alphabet_capitalized is None and match_digits is None)
                            if abstraction_char == entry_char:
                                if abstraction_char_occurred:
                                    if not enum_match:
                                        redundant_chars_per_entry[i].append(abstraction_char)
                                        redundant_char_warning(entry)
                                elif len(mapping[1]) == 1:
                                    update_label_text(abstraction_char, label_list[i], mapping[0])
                                    if tool_tips_labels[i] != "":
                                        tool_tips_labels[i] += "\n"
                                    tool_tips_labels[i] += mapping[3]
                                abstraction_char_occurred = not enum_match
                            elif l == j == 0 and entry_char not in chars_in_abstraction and entry_char not in \
                                    undefined_chars_per_entry[i] and not enum_match:
                                undefined_chars_per_entry[i].append(entry_char)
                                undefined_char_warning(entry)
    for i, entry in enumerate(entry_list):
        if i < len(entry_list) - 1:
            update_warning_for_entry(i, tool_tips_entries, redundant_chars_per_entry, undefined_chars_per_entry)
    update_global_warning(label_warning, redundant_chars_per_entry, undefined_chars_per_entry)
    set_tool_tips(tooltips, entry_list, label_list, n, tool_tips_labels, tool_tips_entries, omit_first)