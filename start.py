from docx import Document
from docxtpl import DocxTemplate

# doc = Document('Blank_ADP.docx')

# doc.save('test.docx')
list_of_states = ['Alabama',
                'Alaska',
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
                'Louisiana',
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

doc = DocxTemplate('test_template.docx')
for state in list_of_states:
    context = {'department' : input(f'Department for {state}:'),
                'state' : state,
                'phone' : input(f'Phone for {state}:'),
                'next_steps' : input(f'Next Steps for {state}:')
                }
    doc.render(context)
    doc.save(f'ADP_{state}.docx')