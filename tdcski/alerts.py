# coding=utf-8
__author__ = 'bob'

type_dict = {
    "error": ("alert-error", "Erreur"),
    'info': ('alert-info', "Info"),
    'success': ("alert-success", "Ok!"),
    'warning': ("", "Attention !")
}

class Alerts():
    def __init__(self):
        self.list = []

    def add(self, *args, **kwargs):
        self.list.append(Alert(*args, **kwargs))

    def get(self):
        output = "\n"
        for a in self.list:
            output += a.to_html()
        for a in self.list:
            if not a.persistent:
                self.list.remove(a)
        return output

class Alert():
    def __init__(self, text, persistent=False, type='info', title=None):
        self.text = text
        self.persistent = persistent
        self.type = type
        self.title = title

    def to_html(self):
        output = '<div class="alert alert-block {}">\n'.format(type_dict[self.type][0])
        if not self.persistent:
            output += '<button type="button" class="close my-alert" data-dismiss="alert">&times;</button>\n'
        if self.title is None:
            output += '<h4>{}</h4>\n'.format(type_dict[self.type][1])
        else:
            output += '<h4>{}</h4>\n'.format(self.title)
        output += '{}\n</div>\n'.format(self.text)
        return output

alerts_list = Alerts()

def get_alerts():
    return alerts_list.get()

def add_alert(*args, **kwargs):
    alerts_list.add(*args, **kwargs)