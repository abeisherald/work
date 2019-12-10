from docx import Document
from docxtpl import DocxTemplate
import csv


list_of_states = ['Alabama / Remote Seller',
                'Alabama / Physical Presence',
                'Alaska / Remote Seller',
                'Arizona',
                'Arkansas',
                'California',
                'Colorado',
                'Connecticut',
                'Delaware',
                'Florida',
                'Georgia',
                'Hawaii',
                'Idaho',
                'Illinois',
                'Indiana',
                'Iowa',
                'Kansas',
                'Kentucky',
                'Louisiana / Remote Seller',
                'Louisiana / Physical Presence',
                'Maine',
                'Maryland',
                'Massachusetts',
                'Michigan',
                'Minnesota',
                'Mississippi',
                'Missouri',
                'Montana',
                'Nebraska',
                'Nevada',
                'New Hampshire',
                'New Jersey',
                'New Mexico',
                'New York',
                'North Carolina',
                'North Dakota',
                'Ohio',
                'Oklahoma',
                'Oregon',
                'Pennsylvania',
                'Rhode Island',
                'South Carolina',
                'South Dakota',
                'Tennessee',
                'Texas',
                'Utah',
                'Vermont',
                'Virginia',
                'Washington',
                'West Virginia',
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

for state in list_of_states:
    if input(f'Do you want to skip this state? {state}  |   y/n:') == 'n':
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

for state in list_of_states:
    if '3' in dict_of_combos[state] and '4' in dict_of_combos[state]:
        with DocxTemplate('full_template.docx') as fulldoc:
            fulldoc.render(full_combo)
            fulldoc.save(f'FULL_{state}.docx')
        with DocxTemplate('UI_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'UI_{state}.docx')
        with DocxTemplate('ADP_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'ADP_{state}.docx')
        with DocxTemplate('WH_template.docx') as fulldoc:
            fulldoc.render(context_wh)
            fulldoc.save(f'WH_{state}.docx')
        with DocxTemplate('WHUI_template.docx') as fulldoc:
            fulldoc.render(context_str)
            fulldoc.save(f'WHUI_{state}.docx')

    elif ('1' in dict_of_combos[state] and '4' in dict_of_combos[state]) or ('1' in dict_of_combos[state] and '5' in dict_of_combos[state]):
        with DocxTemplate('UI_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'UI_{state}.docx')
        with DocxTemplate('ADP_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'ADP_{state}.docx')
        with DocxTemplate('WH_template.docx') as fulldoc:
            fulldoc.render(context_wh)
            fulldoc.save(f'WH_{state}.docx')
        with DocxTemplate('WHUI_template.docx') as fulldoc:
            fulldoc.render(context_str)
            fulldoc.save(f'WHUI_{state}.docx')
    
    elif '2' in dict_of_combos[state]:
        with DocxTemplate('UI_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'UI_{state}.docx')
        with DocxTemplate('ADP_template.docx') as fulldoc:
            fulldoc.render(context_ui)
            fulldoc.save(f'ADP_{state}.docx')

    else:
        print(f'{state} not templated')