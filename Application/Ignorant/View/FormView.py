import re
from tkinter import *
from tkinter import messagebox
import os

class GuiView(Tk):

    INT_ATTRIBS = ("column", "row", "width", "height", "columnspan", "start")
    SPECIAL_ATTRIBS = ("textvariable", "variable")
    CHECK_DICT_NUM = 3

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.languages = None
        self.default_language = None
        self.form_dict = {"check_buttons": False}
        self.check_button_vars = {}
        self.default_widgets_grids = {"Label": {"column": 0, "columnspan": 2, "sticky": "ew"}}
        self.default_widgets_cnf = {"Label": {"justify": "left", "anchor": "w"}}
        self.added_widgets = []

    def display(self, dictionary):

        for key, value in dictionary.items():
            if key == "languages":
                self.languages = value
                self.default_language = value["english_text"]
            elif key == "widgets":
                self._unpack_dict(value)
        self.mainloop()

    def _unpack_dict(self, dictionary):
        if dictionary["widgets"]:
            self._set_widgets(dictionary=dictionary["widgets"])

    def _set_widgets(self, dictionary):
        for key, value in dictionary.items():
            if re.match('Root', key):
                self._set_attribs(value, self)
            elif re.match("OptionMenu", key):
                option_menu = OptionMenu(self, None, None)
                self._set_attribs(value, option_menu)
            elif re.match("Label", key):
                label = Label(self)
                self._set_attribs(value, label)
            elif re.match("Entry", key):
                entry = Entry(self)
                self._set_attribs(value, entry)
            elif re.match("Button", key):
                button = Button(self)
                self._set_attribs(value, button)
            elif re.match("Checkbutton", key):
                check_button = Checkbutton(self)
                self._set_attribs(value, check_button)

    def _set_attribs(self, dictionary, widget=None):

        for key, value in dictionary.items():
            if key == "attribs":
                attribs = self._parse_attribs_values(value)
                widget.config(**attribs)
            elif key in self.SPECIAL_ATTRIBS:
                attribs_dict = self._set_variables(key, value, widget)
                cnf = {key: attribs_dict["value"]}
                widget.config(**cnf)
            elif key == "title":
                attrib_dict = dictionary[key]
                attribs = attrib_dict["attribs"]
                title = self.default_language.texts[attribs["id"]]
                attribs["string"] = title
                del attribs["id"]
                getattr(widget, key)(**attribs)
            elif key == "validatecommand":
                valid_command = (self.register(self._check_entry), '%W', '%d', '%P')
                widget.config(validatecommand=valid_command)
            elif key == "command":
                widget.config(command=self._button_click)
            elif key == "iconbitmap":
                file_name = value["attribs"]["bitmap"]
                if os.name == "nt":
                    path_name = os.path.join("Application", "Ignorant", "Image", file_name + ".ico")
                else:
                    path_name = os.path.join("Application", "Ignorant", "Image", file_name + ".xbm")
                widget.iconbitmap(path_name)
            else:
                attrib_dict = dictionary[key]
                if "attribs" in attrib_dict.keys():
                    attribs = attrib_dict["attribs"]
                    attribs = self._parse_attribs_values(attribs)
                    getattr(widget, key)(**attribs)
                else:
                    getattr(widget, key)()

    def _parse_attribs_values(self, dictionary):
        for key, value in dictionary.items():
            if key in self.INT_ATTRIBS:
                dictionary[key] = int(value)
        return dictionary

    def _set_variables(self, key, dictionary, widget=None):

        attribs_dict = dictionary["attribs"]
        var_id = attribs_dict["id"] + "_var"

        if key == "textvariable":
            var = StringVar(name=var_id)
        if key == "variable":
            var = IntVar(name=var_id)

        for key, value in dictionary.items():
            if key == "attribs":
                try:
                    var_value = self.default_language.texts[value["id"]]
                except KeyError:
                    if "IntVar" in str(type(var)):
                        var_value = int(value["value"])
                    else:
                        var_value = ""
                var.set(var_value)
                if "stock" in value.keys():
                    getattr(self, value["stock"])[var_id] = var_value
            if key == "Menu":
                menu_list = [e for e in value.values()]
                var.set(menu_list[0])
                menu = widget.children["menu"]
                menu.delete(0, 'end')
                for v in menu_list:
                    menu.add_command(label=v,
                                     command=lambda option=v: var.set(option))
            if key == "trace":
                mode = value["attribs"]["mode"]
                var.trace(mode=mode, callback=self._on_trace_event)

        attribs_dict["value"] = var
        setattr(self, var_id, attribs_dict["value"])
        return attribs_dict

    def _add_widgets(self, dictionary):
        row_num = 1
        for key, widget_dict in dictionary.items():
            widget = None
            widg_type = widget_dict["widget"]
            if widg_type == "Label":
                widget = Label(self)

            text = self.default_language.texts[key] + ": "+widget_dict["text"]
            grid_infos = self._get_grid_infos(widg_type.lower())
            cnf_infos = self._get_cnf_infos(widg_type.lower(), ("textvariable"))
            cnf_infos["text"] = text
            label_default_parms = self.default_widgets_cnf[widg_type]
            for k, param in label_default_parms.items():
                cnf_infos[k] = param
            grid_cnf = self.default_widgets_grids[widg_type]
            grid_cnf["row"] = grid_infos["last_row"] + row_num
            widget.config(**cnf_infos)
            widget.grid(**grid_cnf)
            self.added_widgets.append(widget.winfo_name())
            row_num += 1

    def _delete_widgets(self):
        if len(self.added_widgets) > 0:
            for i, widget in enumerate(self.added_widgets):
                self.children[widget].grid_remove()
                del self.children[widget]
                self.added_widgets.pop(i)

    def _get_grid_infos(self, widg_name):
        rows = []
        columns = []
        default_grid = []
        infos = {}
        all_grids = self.grid_slaves()
        for w in all_grids:
            grid_info = w.grid_info()
            rows.append(grid_info["row"])
            columns.append(grid_info["column"])
            if widg_name == w.widgetName:
                default_grid.append(grid_info)
        rows.sort(reverse=True)
        columns.sort(reverse=True)
        infos["last_row"] = rows[0]
        infos["last_column"] = columns[0]
        infos["grid_default"] = default_grid[0]
        return infos

    def _get_cnf_infos(self, widg_name, attribs_to_exclude):
        all_widgs = self.children
        cnf = {}
        for widget in all_widgs.values():
            if widget.widgetName == widg_name:
                w_conf = widget.config()
                for key in w_conf.keys():
                    if widget.cget(key) and key not in attribs_to_exclude:
                        cnf[key] = widget.cget(key)
                return cnf

    def _on_trace_event(self, var, index, mode):
        if var == "selector_var":
            self._set_text_var_lang(var)
        elif var in getattr(self, "check_button_vars"):
            self._check_button_choice(getattr(self, var), var)

    def _check_entry(self, entry_name, action_code, new_text):
        """
        Check the string value before a manual input in texts fields (input or delete).
        Inputs from code are automatically accepted.
        Intercepts the full new text (already in the widget + the intercepted input). The full text
        must begin with a blank or a number and must ends with numbers.
        The form_check list is modified, according to the pattern matching and the new text length.
        Return True or false to the widget. The widget displays, or not the new full text, according to the function
        return.
        :param entry_name: the widget name
        :param action_code: 0 = delete, 1 = entry, -1 none
        :param new_text: widget text + new input
        :return: boolean action for tkinter widget targeted
        """
        boolean = False
        entry_name = entry_name.lstrip(".")
        if action_code == "0" or action_code == "1":
            pattern = re.compile('^\d?[0-9]*$')
            match = pattern.match(new_text)
            if match and len(new_text) > 0:
                getattr(self, "form_dict")[entry_name] = True
                boolean = True
            elif match and len(new_text) == 0:
                getattr(self, "form_dict")[entry_name] = False
                boolean = True
            else:
                getattr(self, "form_dict")[entry_name] = False
                boolean = False
        elif action_code == -1:
            boolean = True
        self._set_button_state()
        return boolean

    def _button_click(self):
        form_values = self._get_var_values(("phone_entry_var", "region_entry_var", "check_button_vars"))
        phone_return = self.parent.get_phone_infos(form_values)
        if "phone_num_error" in phone_return.keys():
            messagebox.showerror(self.default_language.texts["error_title"],
                                 self.default_language.texts["error_message"])
        else:
            self._add_widgets(phone_return)

    def _check_button_choice(self, int_var, var_name):

        if var_name == "check_all_int_var":
            for var in getattr(self, "check_button_vars").keys():
                int_var_c = getattr(self, var)
                int_var_c.set(int_var.get())

        if int_var.get() == 1:
            getattr(self, "form_dict")["check_buttons"] = True
            getattr(self, "check_button_vars")[var_name] = 1
        elif int_var.get() == 0:
            getattr(self, "form_dict")["check_buttons"] = False
            getattr(self, "check_button_vars")[var_name] = 0

        self._set_button_state()

    def _set_text_var_lang(self, var):
        selector = getattr(self, var)
        lang_selected = selector.get()
        self._set_default_lang(lang_selected)
        language = self.default_language.texts
        language.update({"phone_entry": "", "region_entry": "", "check_all_int": 0})
        self._set_var_values(language)
        self._delete_widgets()

    def _set_default_lang(self, lang_selected):
        for key, value in self.languages.items():
            if value.select_name == lang_selected:
                self.default_language = self.languages[key]
                break

    def _set_button_state(self):
        boolean = self._check_dict(getattr(self, "form_dict"), self.CHECK_DICT_NUM, True)
        button = self.children["!button"]
        if boolean:
            button.config(state=NORMAL)
        else:
            button.config(state=DISABLED)
            self._delete_widgets()

    def _set_var_values(self, dictionary):
        for key, value in dictionary.items():
            try:
                check_text = getattr(self, key + "_var")
                getattr(check_text, "set")(value)
            except AttributeError:
                pass

    def _get_var_values(self, var_tuple=()):
        var_values_dict = {}
        for var_name in var_tuple:
            var_values_dict[var_name] = getattr(self, var_name)
        return var_values_dict

    def _check_dict(self, dictionary, number, v_to_check):
        boolean = False
        if number == "All":
            number = len(dictionary)
        elif number == "None":
            number = 0

        num_check = 0
        for i, value in enumerate(dictionary.values()):
            if value == v_to_check:
                num_check += 1
            else:
                boolean = False

            if num_check == number:
                boolean = True
                break
        return boolean
