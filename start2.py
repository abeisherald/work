from docx import Document
from docxtpl import DocxTemplate
import csv


list_of_states = ['Maine',
                'Wisconsin',
                'Wyoming']


dict_of_combos = {state: [] for state in list_of_states}

context_str = {}
context_ui = {}
context_wh = {}

with open('stid.csv', 'r') as csv_file:
    data_csv = list(csv.DictReader(csv_file))
    states_ui_sep_ui = [row ['State'] for row in data_csv if row['Unemployment'] == 'Seperate Unemployment Registration']
    states_ui_same_wh = [row ['State'] for row in data_csv if row['Unemployment'] == 'On Withholding Registration']
    states_ui_same_str = [row ['State'] for row in data_csv if row['Unemployment'] == 'On Sales Tax Registration']
    states_wh_same_str = [row ['State'] for row in data_csv if row['Withholding'] == 'On Sales Tax Registration']
    states_wh_sep_wh = [row ['State'] for row in data_csv if row['Withholding'] == 'Seperate Withholding Registration']
    states_immediate_ui = [row ['State'] for row in data_csv if row['Do we currently get the UIID at the time of registration?'] == 'Yes']
    states_immediate_wh = [row ['State'] for row in data_csv if row['Do we currently get the WHID at the time of registration?'] == 'Yes']
    for state in list_of_states:
        if state in states_ui_sep_ui:
            dict_of_combos[state].append('1')
        elif state in states_ui_same_wh:
            dict_of_combos[state].append('2')
        elif state in states_ui_same_str:
            dict_of_combos[state].append('3')
        else:
            dict_of_combos[state].append('0')

        if state in states_wh_same_str:
            dict_of_combos[state].append('4')
        elif state in states_wh_sep_wh:
            dict_of_combos[state].append('5')
        else:
            dict_of_combos[state].append('0')
        
        if state in states_immediate_ui:
            dict_of_combos[state].append('6')
        elif state in states_immediate_wh:
            dict_of_combos[state].append('7')
        else:
            dict_of_combos[state].append('0')

for state in list_of_states:
    user_input = input(f'Do you want to skip this state? {state}  |   y/n:')
    if user_input == 'n':
        context_str = {}
        context_ui = {}
        context_wh = {}
        if '3' in dict_of_combos[state] and '4' in dict_of_combos[state]:
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
        elif ('1' in dict_of_combos[state] and '4' in dict_of_combos[state]) or ('1' in dict_of_combos[state] and '5' in dict_of_combos[state]):
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
        elif '2' in dict_of_combos[state]:
            context_ui = {'department_ui' : input(f'UI: Department for {state}:'),
                'state_ui' : state,
                'phone_ui' : input(f'UI: Phone for {state}:'),
                'next_steps_ui' : input(f'UI: Next Steps for {state}:')
                }

        dict_of_combos[state].append(context_ui)
        dict_of_combos[state].append(context_wh)
        dict_of_combos[state].append(context_str)     
        full_combo = {**context_ui, **context_wh, **context_str}
        dict_of_combos[state].append(full_combo)
        print(dict_of_combos)
    
    elif user_input == 'y':
        print(f'{state} not templated')
        dict_of_combos[state].append('skip')
    else:
        print('please enter y or n')


for state in list_of_states:
    if 'skip' in dict_of_combos[state]:
        continue
    elif '3' in dict_of_combos[state] and '4' in dict_of_combos[state]:
        # 6 = get immediate ui 7 = get immediate wh
        if '6' in dict_of_combos[state] or '7' in dict_of_combos[state]:
            fulldoc = DocxTemplate('FULL_imme_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'FULL_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'WHUI_{state}.docx')


        else:
            fulldoc = DocxTemplate('FULL_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'FULL_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')

    elif ('1' in dict_of_combos[state] and '4' in dict_of_combos[state]) or ('1' in dict_of_combos[state] and '5' in dict_of_combos[state]):
        if '6' in dict_of_combos[state] and '7' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_imme_template.docx')
            fulldoc.render(dict_of_combos[state][4])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')
        
        elif '6' in dict_of_combos[state] and not '7' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][4])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')
        
        elif '7' in dict_of_combos[state] and not '6' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_imme_template.docx')
            fulldoc.render(dict_of_combos[state][4])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')
        
        else:
            fulldoc = DocxTemplate('UI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][4])
            fulldoc.save(f'WH_{state}.docx')
            wfulldoc =DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')

    elif '2' in dict_of_combos[state]:
        if '6' in dict_of_combos[state] or '7' in dict_of_combos[state]:
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')
        else:
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][6])
            fulldoc.save(f'WHUI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][3])
            fulldoc.save(f'ADP_{state}.docx')

    else:
        print(f'{state} failed to template.')