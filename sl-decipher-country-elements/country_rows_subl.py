import sublime
import sublime_plugin
import re

# helper functions
def getPropertyValueFromElement(element, prop):
    prop = prop + '''="'''
    
    i_start = element.index(prop)
    i_end = i_start + len(prop) + element[i_start + len(prop):].index("\"")

    i_start += len(prop)

    return element[i_start:i_end]

def getSeparatedLabel(label):
    digit_start = re.search(r"\d", label).start()

    return (label[:digit_start], label[digit_start:])

# assumes that element labels have the following format "[characters][numbers]" without any underscores or other characters
# and that the [numbers] part is an integer greater than or equal to 0
class makeCountryElementHiddenCommand(sublime_plugin.TextCommand):
    '''
    transforms a series of elements into elements that can be more easily filtered based on a 
    previous question

    e.g.

    question 1:
    r1, r2, r3

    question 2:
    r101, r102, r201, r202, r203, r303, r304, etc.
    '''
    def run(self, edit, prefix):
        try:
            sels = self.view.sel()

            prefix = int(prefix)

            for sel in sels:
                vrange = self.view.substr(sel).strip("\n").split("\n")

                # in order: element id (r, c, ch, etc.), prefix, number of necessary zeroes, number from original label
                # the value template doesn't have an element id
                # also we assume that the label (sans element id) and value are matching (because they should be)
                label_template = '''label="%s%d%s%s"'''
                value_template = '''value="%d%s%s"'''

                # in order to append the proper number of zeroes, we have to find out where the largest label is 
                # in the  elements we're selecting
                # usually it's at the end, but not always, so...
                all_label_vals = [int(getSeparatedLabel(getPropertyValueFromElement(vrange[i], "label"))[1]) for i in range(len(vrange))]

                max_label_index = all_label_vals.index(max(all_label_vals))

                max_label = getPropertyValueFromElement(vrange[max_label_index], "label")
                max_nums = getSeparatedLabel(max_label)[1]

                # in case the max row is r9 we still have to add a zero
                # to make it r109
                if all_label_vals[max_label_index] < 10:
                    label_template = '''label="%s%d0%s%s"'''
                    value_template = '''value="%d0%s%s"'''

                for i in range(len(vrange)):
                    original_label = getPropertyValueFromElement(vrange[i], "label")
                    original_chars, original_nums = getSeparatedLabel(original_label)

                    n_zeroes = len(max_nums) - len(original_nums)

                    modified_label = label_template % (original_chars, prefix, "0" * n_zeroes, original_nums)

                    vrange[i] = vrange[i].replace('''label="%s"''' % original_label, modified_label)

                    # I suppose we could just run the value replacement and so replace the label as well in one move
                    # but that runs the risk of modifying any numbers outside of our properties
                    # food for thought
                    if '''value="''' in vrange[i]:
                        original_value = getPropertyValueFromElement(vrange[i], "value")

                        modified_value = value_template % (prefix, "0" * n_zeroes, original_value)

                        vrange[i] = vrange[i].replace('''value="%s"''' % original_value, modified_value)

                vrange = "\n".join(vrange)
                
                self.view.replace(edit, sel, vrange)

                prefix += 1
        except Exception as e:
            print(e)

class makeCountryElementCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("First Country prefix:", "", self.on_done, None, None)

    def on_done(self, prefix):
        try:
            self.window.active_view().run_command("make_country_element_hidden", {"prefix": prefix})
        except Exception as e:
            print(e)