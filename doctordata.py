class Doctor:
    """A Doctor object. Used to break up doctors into
    a unique ID, Full Name, Work Credentials (as a list),
    the Practice they work for, Address, and Phone Number
    similar_practices is a list of Doctor IDs that have a
    similar name to this one. identical entries is a list of
    items on the similar practice list with an address that's
    similar too. Different Elements are elements that arent similar
    at all. Mostly used to speed up processing
    """
    def __init__(self, id_num="", name="", credentials=[""], practice="",
                 address="", phone_num=""):
        self.id_num = id_num
        self.name = name
        self.credentials = credentials
        self.practice = practice
        self.address = address
        self.phone_num = phone_num

    def to_dict(self):
        """Returns the Doctor Object as a Dictionary"""
        return {"id_num": self.id_num, "name": self.name,
                "credentials": self.credentials, "practice": self.practice,
                "address": self.address, "phone_num": self.phone_num}

    def full_info(self):
        """Returns all of the data inside of the object"""
        return ("ID: " + str(self.id_num)  + "\n" +
                "Name: " + self.name + "\n" +
                "Credentials: " + str(self.credentials) + "\n" +
                "practice: " + self.practice + "\n" +
                "address: " + self.address + "\n" +
                "phone_num: " + self.phone_num + "\n")

    def info(self):
        """Returns basic data inside of the object, without ID#"""
        return ("Name: " + self.name + "\n" +
                "Credentials: " + str(self.credentials) + "\n" +
                "Practice: " + self.practice + "\n" +
                "address: " + self.address + "\n" +
                "phone_num: " + self.phone_num + "\n")

    def get_info(self, name=True, creds=True, pract=True, addr=True, phone=True, id=False, titles=True):
        full_info = ''
        id_title = ''
        name_title = ''
        cred_title = ''
        pract_title = ''
        addr_title = ''
        phone_title = ''
        if titles:
            id_title = "ID: "
            name_title = "Name: "
            cred_title = "Credentials: "
            pract_title = "Practice: "
            addr_title = "Address: "
            phone_title = "Phone Num: "
        title_list = list()
        content_list = list()
        if id:
            title_list.append(id_title)
            content_list.append(self.id_num)
        if name:
            title_list.append(name_title)
            content_list.append(self.name)
        if creds:
            title_list.append(cred_title)
            content_list.append(str(self.credentials))
        if pract:
            title_list.append(pract_title)
            content_list.append(self.practice)
        if addr:
            title_list.append(addr_title)
            content_list.append(self.address)
        if phone:
            title_list.append(phone_title)
            content_list.append(self.phone_num)
        for i, info_item in enumerate(title_list):
            full_info += title_list[i] + content_list[i] + "\n"
        return full_info
