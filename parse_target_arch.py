options = {}
with open('config.gypi') as file:
    options = eval(file.read())

print options['variables']['target_arch']
