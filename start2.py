from docx import Document
from docxtpl import DocxTemplate
import csv


list_of_states = ['Maine',
                'Wisconsin',
                'Wyoming']


dict_of_combos = {state: [] for state in list_of_states}


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
            dict_of_combos[state].append(ui_status='sep_ui')
        elif state in states_ui_same_wh:
            dict_of_combos[state].append(ui_status='ui_with_wh')
        elif state in states_ui_same_str:
            dict_of_combos[state].append(ui_status='ui_with_str')
        else:
            dict_of_combos[state].append(ui_status='none')

        if state in states_wh_same_str:
            dict_of_combos[state].append(wh_status='wh_with_str')
        elif state in states_wh_sep_wh:
            dict_of_combos[state].append(wh_status='sep_wh')
        else:
            dict_of_combos[state].append(wh_status='none') 
        
        if state in states_immediate_ui:
            dict_of_combos[state].append(immediacy_status='immediate_ui')
        elif state in states_immediate_wh:
            dict_of_combos[state].append(immediacy_status='immediate_wh')
        else:
            dict_of_combos[state].append(immediacy_status='none')

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
    
        dict_of_combos[state].append(context_full={**context_ui, **context_wh, **context_str})
    
    elif user_input == 'y':
        print(f'{state} not templated')
        dict_of_combos[state].append('skip')
    else:
        print('please enter y or n')


for state in list_of_states:
    context = 3
    if 'skip' in dict_of_combos[state]:
        continue
    elif 'ui_with_str' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]:
        # immediate_ui = get immediate ui immediate_wh = get immediate wh
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            fulldoc = DocxTemplate('FULL_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'FULL_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')


        else:
            fulldoc = DocxTemplate('FULL_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'FULL_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')

    elif ('sep_ui' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]) or ('sep_ui' in dict_of_combos[state] and 'sep_wh' in dict_of_combos[state]):
        if 'immediate_ui' in dict_of_combos[state] and 'immediate_wh' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')
        
        elif 'immediate_ui' in dict_of_combos[state] and not 'immediate_wh' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')
        
        elif 'immediate_wh' in dict_of_combos[state] and not 'immediate_ui' in dict_of_combos[state]:
            fulldoc = DocxTemplate('UI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WH_{state}.docx')
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')
        
        else:
            fulldoc = DocxTemplate('UI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'UI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
            fulldoc = DocxTemplate('WH_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WH_{state}.docx')
            wfulldoc =DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')

    elif 'ui_with_wh' in dict_of_combos[state]:
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            fulldoc = DocxTemplate('WHUI_imme_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')
        else:
            fulldoc = DocxTemplate('WHUI_nonim_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'WHUI_{state}.docx')
            fulldoc = DocxTemplate('ADP_template.docx')
            fulldoc.render(dict_of_combos[state][context])
            fulldoc.save(f'ADP_{state}.docx')

    else:
        print(f'{state} failed to template.')