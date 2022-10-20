"""
This example shows how to display content in columns.
The data is pulled from https://randomuser.me
"""

import json
from urllib.request import urlopen

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.console import Group
from rich.layout import Layout


def buttonResize(text, count_in_line):
	buttonSize = 30
	buttonSize = int(buttonSize / count_in_line) - count_in_line
	space = buttonSize - len(text)
	spaceLeft = int(space / 2)
	return ' '*spaceLeft + text + ' '*(space-spaceLeft)


def get_content(item):
	"""Extract text from user dict."""
	'''
	name = item['name']
	value = item['value']
	return f"[b]{name}[/b]\n[yellow]{value}"
	'''
	title = item['name']
	panel = Panel.fit('test', title=title)

	panel_group = Group(
		Panel.fit("Hello"),
		Panel.fit("Hello"),
	)
	panel_group = Group(
		Panel.fit("Hello"),
		#Columns(line)
	)

	keyboard = []
	buttons_color = 'yellow'
	keyboard_text = '[on yellow]'
	for line in item['keyboard']:
		line_keys = []
		for button in line:
			keyboard_text += f'[black on {buttons_color}] {buttonResize(button["text"], len(line))} [on black] '
		keyboard_text += '\n\n'
	

	panelFinal = Panel.fit(Group(
		Panel('\n\n' + item['text'] + '\n\n[black on yellow]button 1'),
		'\n\n',
		keyboard_text
	), title=title)

	#return panel
	return panelFinal


console = Console()

keyboard = [
			[
				{'text': 'data', 'color': 'negative'},
				{'text': 'carusel', 'color': 'primary'},
			],
			[
				{'text': '+', 'color': 'positive'},
				{'text': '-', 'color': 'negative'},
			],
			[
				{'text': 'settings', 'color': 'positive'},
				{'text': 'advertising', 'color': 'positive'},
			],
			[
				{'text': 'full line', 'color': 'positive'},
			],
			[
				{'text': '1', 'color': 'positive'},
				{'text': '2', 'color': 'positive'},
				{'text': '3', 'color': 'positive'},
			],
		]

items = [
	{'name': 'Profil', 'text': '[ PROFIL ]\nВыберети пункт', 'keyboard': keyboard},
	]
items_renderables = [get_content(item) for item in items]
console.print(Columns(items_renderables))