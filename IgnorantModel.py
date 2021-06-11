import trio
import httpx
import re
import phonenumbers
from ignorant.modules.shopping.amazon import amazon
from ignorant.modules.social_media.snapchat import snapchat
from ignorant.modules.social_media.instagram import instagram


class IgnorantModel:
    def __init__(self, parent):
        self.parent = parent
        self.phone_number = ""
        self.region_code = ""

    def report(self, dictionary1):
        """
        Tests the phone number validity with phonenumbers
        Tests the phone number presence within platforms selected
        Builds  and returns a dictionary of widgets infos to build
        :param dictionary1:
        :return: a dictionary with widgets parameters to build
        """
        phone_num = dictionary1["phone_entry_var"].get()
        region_num = dictionary1["region_entry_var"].get()
        plateforms = dictionary1["check_button_vars"]
        check_phone_rep = {}
        phone_number_bag = self._tel_control(phone_num, region_num)
        if "phone_num_error" in phone_number_bag.keys():
            return phone_number_bag
        self.region_code = str(phone_number_bag["phonenumber"].country_code)
        self.phone_number = str(phone_number_bag["phonenumber"].national_number)
        for key, value in plateforms.items():
            if value == 1:
                pattern = re.compile('^(\w+)(_)(\w+)(_)(\w+)(_)(\w+)$')
                match = pattern.match(key)
                if match:
                    plateform_name = match.group(3)
                    string_var_id = match.group(3) + match.group(4) + "label_var"
                    check_phone_rep[string_var_id] = trio.run(self._check_phone, plateform_name)
        return self._set_obj_dict(check_phone_rep, phone_num)

    async def _check_phone(self, plateform):
        """
        Use the ignorant module from Megadose https://github.com/MegaDose. Launches a searc according to the platform
        argument given
        :param plateform:
        :return: out, a search result packed in a dictionary
        """
        phone = self.phone_number
        country_code = self.region_code
        client = httpx.AsyncClient()
        out = []
        if plateform == "amazon":
            await amazon(phone, country_code, client, out)
        if plateform == "instagram":
            await instagram(phone, country_code, client, out)
        if plateform == "snapchat":
            await snapchat(phone, country_code, client, out)

        await client.aclose()
        return out

    def _tel_control(self, phonenumber, regioncode):
        """
        Uses the phonenumbers module from  daviddrysdale https://github.com/daviddrysdale. Launches the phonenumbers
        parser and gives a phone number object with the national number and the international code. Then the phone
        number and its international code is checked. If the phone number is false or a number parsing exception is
        raised , an error message box is returned.
        :param phonenumber:
        :param regioncode:
        :return: a dictionary including a formated phone number for display and the phone number dictionary.
        """
        international_pn = "+" + regioncode + phonenumber
        try:
            phone_number = phonenumbers.parse(international_pn, None)
        except phonenumbers.phonenumberutil.NumberParseException:
            return {"phone_num_error": True}
        else:
            if not phonenumbers.is_valid_number(phone_number):
                return {"phone_num_error": True}
            else:
                return {"formatedphone":
                        phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                        "phonenumber": phone_number}

    def _set_obj_dict(self, dictionary, text):
        """
        Reads a dictionary of lists build by Ignorant and returns a dictionary with widgets parameters to build
        :param dictionary:
        :param text:
        :return: a dictionary with widgets parameters to build
        """
        del dictionary["all_label_var"]
        obj_dict = {}
        for key, value in dictionary.items():
            report_dict = value[0]
            if report_dict["exists"]:
                pattern = re.compile('^(\w+)(_)(\w+)(_)(\w+)$')
                match = pattern.match(key)
                if match:
                    object_name = match.group(1) + match.group(2) + match.group(3)
                    obj_dict[object_name] = {"widget": "Label", "text": text}
        return obj_dict
