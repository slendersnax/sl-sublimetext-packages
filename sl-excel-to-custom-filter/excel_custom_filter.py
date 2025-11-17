import sublime
import sublime_plugin

class excelToCustomFilterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sel = self.view.sel()
            sel_text = self.view.substr(sel[0])

            ids = sel_text.split("\n")
            id_type = ids[0]
            ids = ids[1:]

            # sometimes we may have an empty line at the end
            while "" in ids:
                ids.remove("")

            query = "%s in %s" % (id_type, str(ids))

            self.view.replace(edit, sel[0], query)
        except Exception as e:
            print(e)