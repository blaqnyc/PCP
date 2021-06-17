# TODO: Tally up numNestedTags based on num of references to each nestingID in the tagList[]

import copy


class Tag:
    "This is a docString"
    tagCount = 0
    tagCountDict = {}
    tagIDList = []
    htmlSpecTagList = ['body', 'head', 'html', 'title', 'p', 'div', 'meta', 'br', 'hr',
               'table', 'thead', 'tbody', 'th', 'td', 'tr', 'form', 'input', 'a', 'em',
               'strong', 'ul', 'ol', 'section', 'anchor','li', 'img', 'h1','h2','h3','h4','h5','h6',
               'nav', 'span']


    def __init__(self, name, parentID ='', attr = [], content ='', htmlObjectList = []):
        """
        Creates a tag "object" with various attributes.
        Stores data in dictionary: self.tagDict, to be used elsewhere.
        self.name = The name of the tag object. Ex: all <div> tags have the name 'div'

        self.attr = This is a list of Dictionaries containing Key Value Pairs representing the Tag's Attributes
        For example href, src, etc are all attributes.
        TODO: This should probably be changed to just 1 dictionary. There's no use in a list of Dict() order isnt used

        self.hasNestedContent = This value is changed if this element has descendent elements inside it

        self.numChildrenElems = This value calculates how many children Elements a tag has.

        self.tabLevel = The tab level is used to not only influence how the html is displayed but also
        how many levels 'deep' of a descendant it is compared to other elements.
        Higher values = more of a descendant.
        Lower values = More of an ancestor.
        HTML initializes with a tablevel of 0 because all other elements are its descendants.

        self.parentID = 'parentID'  is an ID value that represents the tagID for the tag this current tag is nested in.
        This is separate from the HTML attribute "id".
        This is used to tell functions where to place this tag, in terms of nesting positions
        For ex: If the <html> tag has a 'tagID' of 'html' and the <body> tag has a 'parentID' of 'html',
        the <body> tag will be nested within the <html> tag like this:
        <html>
              <body>
              </body>
        <html>
        'parentID' is useful not only for the tabbing functions, but also for tag ordering.
        """
        self.name = name
        self.attr = copy.deepcopy(attr) # Have to make this a copy or else every class will refer to this list
        self.hasNestedContent = False
        self.numChildrenElems = 0
        self.tabLevel = 0
        self.parentID = parentID
        self.tagNum = self.tagCount  # Creates unique tagID's for each new created tag. Tags are ID'd in order
        self.incrementTagCount()
        self.createTagID()
        self.selfClosing = False # Used for tag writing, to ignore
        self.specialNameFunctions()
        self.content = content
        self.parentObject = self.setParentObj(htmlObjectList)

    def to_dict(self):
        """Returns the Tag Object as a Dictionary"""
        return {"tagNum": self.tagNum, "name": self.name,
                "attributes": self.attr, "hasNestedContent": self.hasNestedContent,
                "numChildrenElems": self.numChildrenElems, "tabLevel": self.tabLevel,
                "parentID": self.parentID, "isSelfClosing": self.selfClosing,
                "content": self.content, "parentObject":  self.getObjName(self.parentObject)
                }

    def incrementTagCount(self):
        # Add items to the number of tags of that type created.
        # Used to create unique ids for each individual tag
        if self.name not in Tag.tagCountDict.keys():
            Tag.tagCountDict[self.name] = 1
            # print("Adding a new %s tag to the tagCountDictionary" %self.name)
        else:
            Tag.tagCountDict[self.name] += 1
            # print("Added another %s tag to the tagCountDictionary" % self.name)
        # print(Tag.tagCountDict)
        Tag.tagCount += 1

    def createTagID(self):
        if self.name in ['body', 'html', 'head']:
            # No reason to create unique tagID's for these since they are the foundation of an html document
            self.tagID = self.name
        else:
            # Creates unique tagID's for each new created tag. Tags are numerically ID'd in order of their creation
            self.tagID = self.name + "_" + str(Tag.tagCountDict[self.name])
        self.storeTagID()


    def storeTagID(self):
        Tag.tagIDList.append(self.tagID) # Add this object's tagID to the tagIDList

    def specialNameFunctions(self):
        # Special algorithms to run if the name of the tag matches certain values
        if self.name == 'html':
            self.parentID = 'none' # All tags rest within the <HTML> tag, so it wont be nested within anything
            self.hasNestedContent = True
        if self.name in ['hr', 'br', 'meta', 'img']:
            self.selfClosing = True


    def convertToDict(self):
        tagDict = {'tagName': '',
                   'attr': [],
                   'hasNestedContent': False,
                   'numChildrenElems': 0,
                   'parentID': 0,
                   'content': '',
                   'tagID': 0,
                   'selfClosing': False,
                   'tagNum': 0}
        # Use this to fill in the updated Dictionary values
        tagDict['tagNum'] = self.tagNum
        tagDict['tagName'] = self.name
        tagDict['attr'] = self.attr
        tagDict['hasNestedContent'] = self.hasNestedContent
        tagDict['numChildrenElems'] = self.numChildrenElems # TODO: Needs to be dynamically updated by counting the parentID references
        tagDict['parentID'] = self.parentID
        tagDict['content'] = self.content
        tagDict['tagID'] = self.tagID
        tagDict['selfClosing'] = self.selfClosing
        myDict = copy.deepcopy(tagDict)
        return myDict


    def appendAttrib(self, attributeList):
        # Must receive a LIST of dictionaries, not a Dictionary
        # If it receives a dictionary it will break
        # TODO #1: Add Try Except to check if its a dictionary if its a dictionary, convert it to a list
        # TODO #1: If its a list, check that the individual element is a dictionary type, if it's a dict type, then proceed
        # TODO #1: Pseudocode
        # if attributeList.type() == list:
        #       listLen = attributeList.length()
        #       if listLen > 0:
        #           for i in range(0, listLen):
        #               if i.type() == dict:
        #                   # Do Stuff
        # TODO #2: If the attribute is already in that element, overwrite its value, but dont add it again
        # TODO #2: Exception to this is the class attributes. Tags can have multiple classes
        # TODO #2: Pseudocode:
        # if i.keys() in self.attr:
        #   if 'class' in i.keys():
        #       append
        #   else:
        #       overwrite
        for i in range(0, len(attributeList)):
            (self.attr).append(attributeList[i])


    def appendContent(self, content):
        self.content = self.content + str(content)


    def overwriteContent(self, content):
        self.content = str(content)


    def setParentObj(self, htmlObjectList):
        if self.parentID == 'none':
            return 'none'
        elif (verify_id_in_list(Tag.tagIDList, self.parentID)):
            return find_obj_by_id(htmlObjectList, self.parentID)

    def parentObjName(self, htmlObjectList):
        if self.parentID == 'none':
            return 'none'
        elif (verify_id_in_list(Tag.tagIDList, self.parentID)):
            return find_obj_by_id(htmlObjectList, self.parentID).name
        else:
            return 'No Parent'


    def findParentObj(self, htmlObjectList):
        if (verify_id_in_list(Tag.tagIDList, self.parentID)):
            return find_obj_by_id(htmlObjectList, self.parentID)



#
# class p(Tag):
#     # Planning to make subclasses of each tagname to track their individual counts
#     # TODO: Figure out how to run a subclass' init AND the parent classes' init
#     pass

def find_obj_by_id(htmlObjectList, idToFind):
    # Returns an Object from the html object list that has a specific tagID
    for i in htmlObjectList:
        if i.tagID == idToFind:
            return i
    return False

def verify_id_in_list(htmlObjectList, idToFind):
    isInList = False
    if (idToFind in Tag.tagIDList):
        isInList = True
    return isInList

