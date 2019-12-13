from docx import Document
from docxtpl import DocxTemplate
import csv


list_of_states = ['Maine',
                'Wisconsin',
                'Wyoming']


dict_of_combos = {state: [] for state in list_of_states}


with open('stid.csv', 'r') as csv_file:
    data_csv = list(csv.DictReader(csv_file)) 
    
    for state in list_of_states:
        if [row ['State'] for row in data_csv if row['Unemployment'] == 'Seperate Unemployment Registration']:
            dict_of_combos[state].append('sep_ui')
        elif [row ['State'] for row in data_csv if row['Unemployment'] == 'On Withholding Registration']:
            dict_of_combos[state].append('ui_with_wh')
        elif [row ['State'] for row in data_csv if row['Unemployment'] == 'On Sales Tax Registration']:
            dict_of_combos[state].append('ui_with_str')
        elif [row ['State'] for row in data_csv if row['Withholding'] == 'On Sales Tax Registration']:
            dict_of_combos[state].append('wh_with_str')
        elif [row ['State'] for row in data_csv if row['Withholding'] == 'Seperate Withholding Registration']:
            dict_of_combos[state].append('sep_wh')
        elif [row ['State'] for row in data_csv if row['Do we currently get the UIID at the time of registration?'] == 'Yes']:
            dict_of_combos[state].append('immediate_ui')
        elif [row ['State'] for row in data_csv if row['Do we currently get the WHID at the time of registration?'] == 'Yes']:
            dict_of_combos[state].append('immediate_wh')
        else:
            dict_of_combos[state].append('none')

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
    context = dict_of_combos[state][3] # 3 is index 3 of the context list we created up above
    if 'skip' in dict_of_combos[state]:
        continue
    elif 'ui_with_str' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]:
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            self.templatee(state, 'FULL_imme', 'FULL')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WHUI_imme', 'WHUI')

        else:
            self.templatee(state, 'FULL_nonim', 'FULL')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WHUI_nonim', 'WHUI')

    elif ('sep_ui' in dict_of_combos[state] and 'wh_with_str' in dict_of_combos[state]) or ('sep_ui' in dict_of_combos[state] and 'sep_wh' in dict_of_combos[state]):
        if 'immediate_ui' in dict_of_combos[state] and 'immediate_wh' in dict_of_combos[state]:
            self.templatee(state, 'UI_imme', 'UI')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WH_imme', 'WH')
            self.templatee(state, 'WHUI_imme', 'WHUI')

        
        elif 'immediate_ui' in dict_of_combos[state] and not 'immediate_wh' in dict_of_combos[state]:
            self.templatee(state, 'UI_imme', 'UI')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WH_nonim', 'WH')
            self.templatee(state, 'WHUI_nonim', 'WHUI')
            
        
        elif 'immediate_wh' in dict_of_combos[state] and not 'immediate_ui' in dict_of_combos[state]:
            self.templatee(state, 'UI_nonim', 'UI')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WH_imme', 'WH')
            self.templatee(state, 'WHUI_nonim', 'WHUI')
        
        else:
            self.templatee(state, 'UI_nonim', 'UI')
            self.templatee(state, 'ADP', 'ADP')
            self.templatee(state, 'WH_nonim', 'WH')
            self.templatee(state, 'WHUI_nonim', 'WHUI')

    elif 'ui_with_wh' in dict_of_combos[state]:
        if 'immediate_ui' in dict_of_combos[state] or 'immediate_wh' in dict_of_combos[state]:
            self.templatee(state, 'WHUI_imme', 'WHUI')
            self.templatee(state, 'ADP', 'ADP')
        else:
            self.templatee(state, 'WHUI_nonim', 'WHUI')
            self.templatee(state, 'ADP', 'ADP')

    else:
        print(f'{state} failed to template.')