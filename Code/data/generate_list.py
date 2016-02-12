import re

input_file = open('List_of_companies_of_the_United_States.txt', 'r').read()
output_file = open('entities_list.txt', 'w')

extract_lines = re.compile(r'<li><a.+?</a></li>')
extract_links = re.compile(r'<.+?>')

lines = extract_lines.findall(input_file)
links = []
for line in lines:
	links.append(''.join(extract_links.sub('', line)))

for link in links:
	output_file.write(link + "\n")