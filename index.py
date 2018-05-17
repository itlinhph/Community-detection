import yaml

data = []
with open('users.yaml', 'r') as input_file:
  data = yaml.load(input_file)

id_map = {}

for item in data:
  id_map[str(item['index'])] = item['user']

print id_map

content = ''
with open('edges_150.csv', 'r') as csv_file:
  content = csv_file.read()

lines = content.split('\n')

pairs = []

for line in lines:
  pair = line.split('\t')
  pairs.append([id_map[pair[0]], id_map[pair[1]]])


with open('edges_2.csv', 'w') as output_file:
  for pair in pairs:
    output_file.write(pair[0])
    output_file.write('\t')
    output_file.write(pair[1])
    output_file.write('\n')
