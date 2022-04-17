from logo import logo

colors = {}
colors['popcorn'] = '#D4B773' # CU gold: '#D4B773'
colors['mountains_edge'] = '#636363' # lighter gray: '#9fa3a6'
colors['mountains_snow'] = '#FFFFFF'
colors['border'] = '#636363'
colors['border_contrast'] = '#FFFFFF'
colors['header_tag'] = '#636363'
colors['header_text'] = '#FFFFFF'
colors['footer_lines'] = '#636363'
colors['footer_text'] = '#FFFFFF'
colors['sky'] = '#85E2FF' # some other blues to try: '#C0F5FA', '#9DD1F1', '#9ED8DB'
colors['sky'] = '#ADF7FF' # some other blues to try: '#C0F5FA', '#9DD1F1', '#9ED8DB', '#99F5FF', #ADF7FF

logo('dept_logo.png', colors, ratio='5:4', shape='default')