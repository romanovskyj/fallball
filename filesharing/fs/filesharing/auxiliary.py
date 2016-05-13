#
# get all marked ids from filled form
#
def marked_elements(form_data):
    marked_elmts = []
    for elmt in form_data:
                if elmt.startswith('mark'):
                    if form_data[elmt] == True:
                        id = elmt.split('_')[1]
                        marked_elmts.append(int(id))

    return marked_elmts