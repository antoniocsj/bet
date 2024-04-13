from bs4 import BeautifulSoup

# Opening the html file and Reading the file
with open('apostas.html', 'r') as HTMLFile:
    file_content = HTMLFile.read()

# Creating a BeautifulSoup object and specifying the parser
S = BeautifulSoup(file_content, 'lxml')

# # Using the select-one method to find the second element from the li tag
# Tag = S.select_one('li:nth-of-type(2)')
#
# # Using the decompose method
# Tag.decompose()

# Using the prettify method to modify the code
with open('apostas_body.html', 'w') as HTMLFile:
    pretty = S.body.prettify()
    HTMLFile.write(pretty)
