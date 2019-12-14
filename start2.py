from docx import Document
from docxtpl import DocxTemplate
import csv


list_of_states = ['New York',
                'Maine',
                'Wisconsin',
                'Wyoming']


dict_of_combos = {state: [] for state in list_of_states}


def reg_indx(data_source, state, row_columnx, row_columnx_filter, dict_append):
    if state in [row ['State'] for row in data_csv if row[row_columnx] == row_columnx_filter]:
        dict_of_combos[state].append(dict_append)
    else:
        dict_of_combos[state].append('none')


with open('stid.csv', 'r') as csv_file:
    data_csv = list(csv.DictReader(csv_file)) 
    
    for state in list_of_states:

        reg_indx(data_csv, state, 'Unemployment', 'Seperate Unemployment Registration', 'sep_ui')
        reg_indx(data_csv, state, 'Unemployment', 'On Withholding Registration', 'ui_with_wh')
        reg_indx(data_csv, state, 'Unemployment', 'On Sales Tax Registration', 'ui_with_str')
        reg_indx(data_csv, state, 'Withholding', 'On Sales Tax Registration', 'sep_wh')
        reg_indx(data_csv, state, 'Withholding', 'Seperate Withholding Registration', 'wh_with_str')
        reg_indx(data_csv, state, 'Do we currently get the UIID at the time of registration?', 'Yes', 'immediate_ui')
        reg_indx(data_csv, state, 'Do we currently get the WHID at the time of registration?', 'Yes', 'immediate_wh')
        
    print(dict_of_combos)

for state in list_of_states:
    user_input = input(f'Do you want to skip this state? {state}  |   y/n:')
    if user_input == 'n':
        context_str = {}
        context_ui = {}
        context_wh = {}
        if 'ui_with_str' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]:
            context_ui = {'department_ui' : input(f'UI: Department for {state}:'),
                'state_ui' : state,
                'phone_ui' : input(f'UI: Phone for {state}:'),
                'next_steps_ui' : input(f'UI: Next Steps for {state}:')
                }
            context_wh = {'department_wh' : input(f'WH: Department for {state}:'),
                'state_wh' : state,
                'phone_wh' : input(f'WH: Phone for {state}:'),
                'next_steps_wh' : input(f'WH: Next Steps for {state}:')
                }
            context_str = {'department_str' : input(f'STR: Department for {state}:'),
                'state_str' : state,
                'phone_str' : input(f'STR: Phone for {state}:'),
                'next_steps_str' : input(f'STR: Next Steps for {state}:')
            }
        elif ('sep_ui' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]) or ('sep_ui' in dict_of_combos[state] and 'sep_wh' in dict_of_combos[state]):
            context_ui = {'department_ui' : input(f'UI: Department for {state}:'),
                'state_ui' : state,
                'phone_ui' : input(f'UI: Phone for {state}:'),
                'next_steps_ui' : input(f'UI: Next Steps for {state}:')
                }
            context_wh = {'department_wh' : input(f'WH: Department for {state}:'),
                'state_wh' : state,
                'phone_wh' : input(f'WH: Phone for {state}:'),
                'next_steps_wh' : input(f'WH: Next Steps for {state}:')
                }
        elif 'ui_with_wh' in dict_of_combos[state]:
            context_ui = {'department_ui' : input(f'UI: Department for {state}:'),
                'state_ui' : state,
                'phone_ui' : input(f'UI: Phone for {state}:'),
                'next_steps_ui' : input(f'UI: Next Steps for {state}:')
                }
    
        dict_of_combos[state].append({**context_ui, **context_wh, **context_str})
    
    elif user_input == 'y':
        print(f'{state} not templated')
        dict_of_combos[state].append('skip')
    else:
        print('please enter y or n')



def templatee(state, inputfile, outputfile):
    fulldoc = DocxTemplate(f'{inputfile}_template.docx')
    fulldoc.render(context)
    fulldoc.save(f'{outputfile}_{state}.docx')



for state in list_of_states:
    context = dict_of_combos[state][7] # 7 is index of the context objects we created up above
    if 'skip' in dict_of_combos[state]:
        continue
    elif 'ui_with_str' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]:
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            templatee(state, 'FULL_imme', 'FULL')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WHUI_imme', 'WHUI')

        else:
            templatee(state, 'FULL_nonim', 'FULL')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WHUI_nonim', 'WHUI')

    elif ('sep_ui' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]) or ('sep_ui' in dict_of_combos[state] and 'sep_wh' in dict_of_combos[state]):
        if 'immediate_ui' in dict_of_combos[state] and 'immediate_wh' in dict_of_combos[state]:
            templatee(state, 'UI_imme', 'UI')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WH_imme', 'WH')
            templatee(state, 'WHUI_imme', 'WHUI')

        
        elif 'immediate_ui' in dict_of_combos[state] and not 'immediate_wh' in dict_of_combos[state]:
            templatee(state, 'UI_imme', 'UI')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WH_nonim', 'WH')
            templatee(state, 'WHUI_nonim', 'WHUI')
            
        
        elif 'immediate_wh' in dict_of_combos[state] and not 'immediate_ui' in dict_of_combos[state]:
            templatee(state, 'UI_nonim', 'UI')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WH_imme', 'WH')
            templatee(state, 'WHUI_nonim', 'WHUI')
        
        else:
            templatee(state, 'UI_nonim', 'UI')
            templatee(state, 'ADP', 'ADP')
            templatee(state, 'WH_nonim', 'WH')
            templatee(state, 'WHUI_nonim', 'WHUI')

    elif 'ui_with_wh' in dict_of_combos[state]:
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            templatee(state, 'WHUI_imme', 'WHUI')
            templatee(state, 'ADP', 'ADP')
        else:
            templatee(state, 'WHUI_nonim', 'WHUI')
            templatee(state, 'ADP', 'ADP')

    else:
        print(f'{state} failed to template.')