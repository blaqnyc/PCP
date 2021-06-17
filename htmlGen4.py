import htmlgentools4
import pyperclip

# TODO: KEEP IN MIND THREE CONCEPTS:
# TODO #1: A FUNCTION IS A BLACK BOX THAT RECEIVES INPUT OF AN EXPECTED TYPE AND OUTPUTS VALUES FROM THAT TYPE
# TODO #2: AVOID USING GLOBALS AS MUCH AS POSSIBLE
# TODO #3: Don't Repeat Yourself

# TODO PROJECT ADDITIONS
# TODO: This alpha is basically done.
# TODO: The last things to do are to append or overwrite attributes that have the same name as existing ones
# TODO: For classes, you'll append them, for other duplicates, you overwrite.
# TODO: Consolidate htmlGen4 and htmlgentools4 into one HTML gen tools program/class

# Globals =[
# TODO: Try to find a way to eliminate the use of this global using recursion!
currentIndex = 0
Tags = htmlgentools4.Tag

# DEBUG GLOBALS
debug = False
verbose = False
specialDebug = True # 'When Debugging 1 specific thing'
busyNotificationShown = False

# CONSTANTS
endTag  = '>'
startAnchorTag = '</'


def incrementnumChildrenElems():
    # TODO
    pass


def printVerboseText(text):
    # TODO: Future Functionality planned. If Verbose is set, it will spit out more information Otherwise it wont
    print(text)


def find_obj_by_id(htmlObjectList, idToFind):
    # Returns an Object from the html object list that has a specific tagID
    if debug:
        print('find_obj_by_id()')
    for i in htmlObjectList:
        if i.tagID == idToFind:
            return i
    return False


def find_obj_by_name(htmlObjectList, nameToFind):
    if debug:
        print('find_obj_by_name()')
    for i in htmlObjectList:
        if i.name == nameToFind:
            return i


def updateNestingValuesNew(htmlObjectList):
    if debug:
        print("updateNestingvalues()")
    objListLength = len(htmlObjectList)
    idTally = {}
    for i in range(0, objListLength):
        # Update the number of nested tags, and set the hasNestedContent value of the nested in value to true
        # If there is data. But if will ignore other elements, and not unnecessarily nest things
        thisTag = htmlObjectList[i]
        idToSearchFor = thisTag.parentID  # Store the ID
        if idToSearchFor not in idTally:  # if the id is not in the tally, add it.
            if idToSearchFor == 'none':  # Ignore the HTML as it isn't nested within anything
                pass
            else:
                idTally[idToSearchFor] = 1
        else:
            idTally[idToSearchFor] += 1
    idTallyTuples = list(idTally.items()) # Create a list of tuples, from the idTally dictionary, and use it to
    # distribute the values to the appropriate HTML IDs
    if debug:
        print("idTallyTuples: ", idTallyTuples)
    for i in idTallyTuples:
        thisparentID = i[0]
        # print("\nSearching htmlObjectList for the ID: \'%s\'" % thisparentID)
        thisTag = find_obj_by_id(htmlObjectList, thisparentID)
        if thisTag == False:
            print("ID not Found!")
        else:
            # print("ID found! Updating totals!")
            # print("Before:", thisTag.convertToDict())
            thisTag.numChildrenElems = i[1]  # Update the value
            thisTag.hasNestedContent = True  # Update that it has nested content
            # print("After:", thisTag.convertToDict())


def findAttributes(thisTag):
    ''' This converts single item dictionaries into their key value pairs, and loops through the
    array of dictionaries, to extract the attributes. To add more elements to the attribs,
    you add them as array elements to the 'attr': dictionary entry. This is modeled after
    JSON structure. Where objects with multiple elements will be an array of elements.'''
    thisTagAttribList = thisTag.attr # List of dictionaries containing the tag's attributes
    attribString = ""
    numAttribs = len(thisTagAttribList)
    if numAttribs > 0:
        for i in range(0, numAttribs): # Since 'attr' in this example is a list, search starting from elem 1
            attrib =  list(thisTagAttribList[i].keys())
            attribContent = list(thisTagAttribList[i].values())
            attribString = attribString + " " + str(attrib[0]) + "=\"" + str(attribContent[0]) +"\""
    return attribString


def createStartTag(thisTag, isAnchor=False):
    if thisTag.name == 'html':
        if isAnchor == False:
            return '<!DOCTYPE html'
    if isAnchor:
        startTag = '</'
    else:
        startTag = '\n' + ('\t' * thisTag.tabLevel) + '<' # Realign the opening tag based on its tab level
        # Extra Info:
        # Every opening tag after <!DOCTYPE html> will be on a new line, hence \n at the start.
        # How many tabs that line has is based on its 'tabLevel' property
        # The tabLevel property is calculated in the function call: "updateTabLevel(htmlObjectList, thisTag, parentID)"
        # HTML starts with a tabLevel of 0 as it is the first tag in the html document
        # All other tags will have a tab level equal to their direct parent element's .tabLevel + 1
        # Example #1:
        # <html> has a tabLevel of 0. <head> 's parent element is <html>
        # So <head>.tabLevel = <html>.tabLevel + 1
        # <head>.tabLevel = 0 + 1
        # <head>.tabLevel = 1
        # Example #2:
        # A <meta> tag nested inside of <head> will have <head> as its parent element.
        # <head>.tabLevel = 1 .
        # <meta>.tabLevel = <head>.tabLevel + 1
        # <meta>.tabLevel = 1 + 1
        # <meta>.tabLevel = 2. Etc.
        # Managing the orientation this way will properly tab out everything.
    return startTag + thisTag.name


def parseContent(thisTag, htmlObjectList):
    # Recursion.... Totally dont remember how this works ^^;;;
    # I'm not too sure how I managed to get it to work, TBH but it works flawlessly and recursively...
    # So I don't actually want to touch it, Good luck lol
    # Due to how it works though, it NEEDS the htmlObjectList[] to be listed in the order the tags appear in the markup
    # if debug:
    global currentIndex
    numChildrenElemsLeft = thisTag.numChildrenElems
    finalString = ""
    while numChildrenElemsLeft > 0:
        # print("numChildrenElems", numChildrenElems)
        currentIndex += 1
        numChildrenElemsLeft = numChildrenElemsLeft - 1
        finalString += createTags(htmlObjectList[currentIndex], htmlObjectList)
    return finalString + thisTag.content


def createTags(thisTag, htmlObjectList):
    # Returns the created string.
    if debug:
        print("createTags()")
    anchorAlignment = ''
    if thisTag.hasNestedContent:
        anchorAlignment = '\n' + ('\t' * thisTag.tabLevel) # Used to tab align anchors properly
    openingTag = createStartTag(thisTag) + findAttributes(thisTag) + endTag
    if thisTag.selfClosing == False:
        closingTag = anchorAlignment + createStartTag(thisTag, True) + endTag
        # ParseContent does recursive calls to fill in the data. It's genius work, but I have no idea how it works :^)
        # Find Attributes turns the Attribute Dictionary list into a string for ease of use
        return (openingTag + parseContent(thisTag, htmlObjectList) + closingTag)
    else:
        # SelfClosing tags have no content nor closing tags
        return openingTag

#Suggested Edits for createTags()
'''While your function does not do too many things, I do have some remarks on your code:
* You may want to look at logging to avoid all the if debug: print() in your code. It's easier to do logging.debug() in any case, and only setup logging to print out debug information if debug is true in some logging management function/main function.
* if thisTag.selfClosing == False: should rather be if not thisTag.slefClosing: it's easier to read.
* You have some unnecessary parentheses, in anchorAlignment = '\n' + '\t' * thisTag.tabLevel and in return openingTag +...
* I think your createStartTag function is ill-named, since you use it to create the closingTag as well when the second parameter is True.

How to Log Debug: https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
'''


def parseHtmlDocumentList(htmlObjectList):
    global currentIndex
    currentIndex = 0
    updateNestingValuesNew(htmlObjectList) # UPDATE THE DATA FOR NESTING VALUES FIRST. THEN DO PROCESSING AFTER. THIS IS IMPORTANT !!!!!
    thisTag = htmlObjectList[0] #Send over the first element, and process from there.
    print("Converting to HTML Document... ")
    output = createTags(thisTag, htmlObjectList)
    copyTextToClipboard(output)
    return output
    # displayHTMLDictionaries(htmlObjectList)


def copyTextToClipboard(output):
    pyperclip.copy(output)
    print("HTML Document Pasted to Clipboard!\n")


def insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength):
    if debug:
        print("insert_append_data()")
    if (insertionPoint == tagListLength - 1) or thisTag.parentID == 'body': #Append items nested into the body to the end of the document
        if verbose:
            print("'%s' appended onto a list of length %d" % (thisTag.tagID, tagListLength))
        htmlObjectList.append(thisTag)
        return
    else:
        htmlObjectList.insert(insertionPoint + 1, thisTag)
        if verbose:
            print("'%s' inserted at Index %d" % (thisTag.tagID, insertionPoint + 1))
        return


def convert_parentID_to_name(htmlObjectList, parentID):
    if debug:
        print("convert_parentID_to_name()")
    for i in range(len(htmlObjectList)-1, -1, -1):
        if htmlObjectList[i].tagID == parentID:
            # print("Found the %s tag" %htmlObjectList[i].name )
            # print("Its id is %d" %htmlObjectList[i].tagID)
            return htmlObjectList[i].name
    print("No such tag was found")


# TODO: HAD AN IDEA! TRY TO CHANGE THIS SO THAT IT USES THE 'NUMOFNESTEDTAGS' PROPERTY OF THE PARENT ELEMENT TO
# TODO: 'COUNT DOWN' THE DOM (Starting from the parent's index, if the currently looked at item is a child
# TODO: of the parent element: 'if currentItem.parentID == parent.tagID' then deduct 1 from the number
# TODO: OR Fill a list of elements that are direct children to the parent element until you have a list of
# TODO: elements that make len(listOfElements) == parent.numChildrenElems. Then, you take the last element of the list
# TODO: find its index in the
# TODO: SCRATCH THAT LAST IDEA.
def findLastChildOfParent(htmlObjectList, thisTag):
    # This "Walks down the DOM" Starting at the location of this Tag's Parent
    # It uses the Tab Level Property to verify whether an item is a child or not
    # More tabs, mean its a child as its tabbed more deeply to the side, signifying that its a child
    # The tab level is determined by the parentID property  so it shouldn't be wrong.
    # If the tab value is less or equal to the parent level,
    # then you know it's not a child so you'll break at that
    # point and retun the index
    thisTagParent = find_obj_by_id(htmlObjectList, thisTag.parentID)
    parentIndex = htmlObjectList.index(thisTagParent)
    parentLevel = thisTagParent.tabLevel
    lastChildLevel = thisTagParent.tabLevel
    lastChildIndex = parentIndex + 1
    for i in range(parentIndex+1,len(htmlObjectList),1):
        currentTag = htmlObjectList[i]
        # print("Current Last Child: %s" %currentTag.tagID)
        if currentTag.tabLevel > parentLevel:
            lastChild = currentTag
            lastChildIndex = i
            lastChildLevel = currentTag.tabLevel
            # print("New Last Child Found!")
            # print("New Last Child: %s" % lastChild.tagID)
            # print("New Index: %d" % i)
        elif currentTag.tabLevel <= parentLevel: # Some potential code that can cause problems, but I think it will work
            break
    return lastChildIndex


def add_tag_obj_to_list(htmlObjectList, thisTag):
    if debug:
        print("add_tag_obj_to_list()")
    # Adds a html.Tag Object, to the list given
    tagListLength = len(htmlObjectList)
    if tagListLength <= 1:
        # If this list is empty, you have to fill it with something
        if debug:
            print("List Empty or only has HTML tag, so appending this new tag")
        htmlObjectList.append(thisTag)
        return
    lastItemIndex = tagListLength-1
    lastItem = htmlObjectList[lastItemIndex]  # Declare the last item in the html list
    lastItemParent = find_obj_by_id(htmlObjectList, lastItem.parentID)  # Find the parent element of the last Item in the htmlList
    if lastItemParent.parentID == thisTag.parentID:
        if debug:
            print("Last item parent: %s has the same parentID(%s) as '%s'" % (lastItemParent.tagID, lastItemParent.parentID, thisTag.tagID))
        # If the parent element of the last item on the list, has the same nesting ID as this tag, append this
        # Item to the end of the html list
        insertionPoint = lastItemIndex
        insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)
        return
    for i in range(lastItemIndex, -1, -1):  # Loop backwards to find the last item that matches the criteria
        # print("Loop Backwards")
        currListObject = htmlObjectList[i]
        if currListObject.parentID == thisTag.parentID:  # If you found the location of the tag to be nested in...
            insertionPoint = findLastChildOfParent(htmlObjectList, thisTag)  # Store that location
            insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)  # Add it to the object list
            return
    # If you got here, then the item doesn't have another item it can nest next to, so that would mean this item
    # is the first item to be nested within that tag, so change the behavior:
    if debug:
        print("Fell Through")
    parent = find_obj_by_id(htmlObjectList, thisTag.parentID)
    # print("This %s tag is the first tag to be nested in the %s tag" %
    #       (thisTag.tagID, convert_parentID_to_name(htmlObjectList, thisTag.parentID)))
    if debug:
        print("This %s tag is the first tag to be nested in the %s tag" %(thisTag.tagID, parent.tagID))
    # TODO: Try to find a way to consolidate these two for loops in some kind of way. There's a lot of code repetition
    for i in range(lastItemIndex, -1, -1):
        currListObject = htmlObjectList[i]
        if currListObject.tagID == thisTag.parentID:  # Compare the tag ID's instead if its the first of its type
            insertionPoint = i
            insert_append_data(htmlObjectList, thisTag, insertionPoint, tagListLength)  # Add it to the object list
            return


def is_tagid_unique(tagToCheck):
    # This checks if the tag given is a unique tagID or the name of an HTML element from the HTML spec(vanilla tag name)
    tagList = htmlgentools4.Tag.htmlSpecTagList
    if tagToCheck in tagList: # If the tag is an official tag in the HTML Spec, it's not unique
        return False
    else:
        if debug:
            print("%s is NOT a tag in the HTML Spec. \nSearching as if its a unique ID" %(tagToCheck))
        return True


def convert_tagID_to_parentID(nestingString, htmlObjectList):
    # TODO I still think this is doing too much by searching for the object. try to make a function that searches backwards
    for i in range(len(htmlObjectList)-1,-1,-1):
        if htmlObjectList[i].tagID == nestingString:
            return htmlObjectList[i].tagID
    # If you got here, that nestingString wasnt found
    print("The nesting string \'%s\' was not found in the HTML object list of tagIDs" % nestingString)
    return False


def convert_name_to_parentID(nestingString, htmlObjectList):
    if debug:
        print("convert_name_to_parentID()")
    for i in range(len(htmlObjectList)-1, -1, -1):
        if htmlObjectList[i].name == nestingString:
            found = True
            return htmlObjectList[i].tagID
    # If you got here, that nestingString wasnt found
    print("The parentID \'%s\' was not found in the HTML object list of tag names" % nestingString)
    return False


def showCurrentHTMLStructure(htmlObjectList):
    # Mostly for debugging purposes
    htmlStructureList = ''
    for i in htmlObjectList:
        htmlStructureList += ("<%s> [tagID: %s][nested within: %s]\n" %(i.name, i.tagID, str(i.parentID)))
    print("\nCurrent HTML Structure:\n%s" % htmlStructureList)


def create_table_data(htmlObjectList, tableRowID, attributeList = [], content = ''):
    return create_html_object(htmlObjectList, 'td', tableRowID, attributeList, content)


def create_new_row(htmlObjectList, rowLocationID, attributeList = []):
    return create_html_object(htmlObjectList, 'tr', rowLocationID, attributeList)


def editAttributes(htmlObjectList, idName):
    tagToEdit = find_obj_by_id(htmlObjectList, idName)
    attributes = input("What attributes would you like to add to this element.")


def updateParentNumChildrenElems(htmlObjectList, thisTag):
    thisTagParentObj = thisTag.findParentObj(htmlObjectList)
    thisTagParentObj.numChildrenElems += 1
    # print('%s num of child elems increased to %d' % (thisTagParentObj.tagID, thisTagParentObj.numChildrenElems))

# TODO: STORE tagID:TagObject pair dictionary as global? Gross. As class? Maybe better?
# TODO: For easy lookup of tagObjects: Ex: {'html': (htmlTagObject at x0a08sasdf), 'p_5': (htmlTagObject at xxxx01)}
# TODO: Instead of having to do a for loop to look for each individual tagID, store it in an object like this ^---
# TODO: JSON is looking more and more appealing lol

def updateTabLevel(htmlObjectList, thisTag):
    # TODO: Updated This Recently, Backup located in htmlGen4Backup2.py
    if debug:
        print('updateTabLevel()')
    if thisTag.name == 'html':
        thisTag.tabLevel = 0
        return
    # elif len(htmlObjectList) == 0 or thisTag.parentID == 'none':
    #         thisTag.tabLevel = 0
    #         return
    else:
        nestedTag = find_obj_by_id(htmlObjectList, thisTag.parentID) # returns the parent
        thisTag.tabLevel = nestedTag.tabLevel + 1 # An nested tag, will have a tab level equal to the tag its nested in, + 1
    # print("%s has a Tab Level of %d" % (thisTag.tagID, thisTag.tabLevel))


def create_html_object(htmlObjectList, name, parentID = 'html', attributeList = [], content =''):
    # Creates and HTML Object based on the information given, and adds it to the HTML list
    # This also returns the tagObject thats created
    global busyNotificationShown
    if debug:
        print("create_html_object()")
    if verbose:
        initText = "\nAttempting to make a <%s> tag " % name
        initText += "nested within the tag of ID: '" + str(parentID) + "', attributes: " + str(
            attributeList) + " and content of '" + str(content) + "'"
        # print(initText)
    if busyNotificationShown == False:
        print('Creating HTML Tags... This can take a while!')
        busyNotificationShown = True
    if name in ['html', 'body', 'head']:
        # These three tags, get a free pass, as special conditions are already set for them (especially for html tags)
        # and the default value of 'html' for nesting id works for them perfectly
        pass
    else:
        if (is_tagid_unique(parentID) == False):
            # If this is tag's parentID parameter is a tag name within the HTML spec,
            # you can simply insert it into the most recent occurrence of a tag with the same name
            parentID = convert_name_to_parentID(parentID, htmlObjectList)
        else:
            # If this tag's parentID param is a unique tagID (not in the HTML spec),
            # Then search for the unique tagID
            parentID = convert_tagID_to_parentID(parentID, htmlObjectList)
        if parentID == False:
            # If it couldn't find that parentID in the list, don't create the tag object
            print("Unable to find that parentID. So the Tag object wont be created. Returning...")
            return
    thisTag = htmlgentools4.Tag(name, parentID, attributeList, content, htmlObjectList) # Create the tag object
    updateTabLevel(htmlObjectList, thisTag)  # Update the tag Object's Tab Level
    add_tag_obj_to_html_obj_list(htmlObjectList, thisTag) # Add the tag object to the list of HTML Tag Objects
    if (thisTag.parentObject in htmlObjectList): # The parentTag has to be in the list, to update its numChildren.
        updateParentNumChildrenElems(htmlObjectList, thisTag)
    if debug:
        showCurrentHTMLStructure(htmlObjectList)
        showTagsAndParents(thisTag)
    return thisTag # Return the created Tag Object


def displayHTMLDictionaries(htmlObjectList):
    if debug:
        print("displayHTMLDictionaries()")
    for i in htmlObjectList:
        print()
        dictionary = i.convertToDict()
        for j in dictionary.items():
            print (j)


def new_html_document():
    if debug:
        print("new_html_document()")
    # Object Properties:
    # name, attr, hasNestedContent, numChildrenElems, parentID, content, tagID, selfClosing
    htmlObjectList = []
    create_html_object(htmlObjectList, 'html') # Should always create the HTML Tag first
    create_html_object(htmlObjectList, 'head') # Default value of 0 for parentID will nest things into the html tag by default
    create_html_object(htmlObjectList, 'body')
    return htmlObjectList

def tagTesting():
    # Sample Code you can use from this program
    htmlObjectList = new_html_document()
    create_html_object(htmlObjectList, 'p', 'body', [], "Testing Testing 1, 2, 3")
    create_html_object(htmlObjectList, 'meta', 'head', [{'charset':'utf-8'}])
    create_html_object(htmlObjectList, 'title', 'head', [], "Testing Title")
    find_obj_by_name(htmlObjectList, 'body').appendAttrib([{'id': 'main'}, {'class': 'main'}])
    create_html_object(htmlObjectList, 'p', 'body', [{'class': 'butts'}, {'id':'angrymainyu'}, {'class': 'border'}], 'Fate Stay Night is Da Bess\'' )
    create_html_object(htmlObjectList, 'div', 'body', [{'class': 'box'}])
    create_html_object(htmlObjectList, 'p', 'table') # Testing nesting a tag within a valid element name, that doesnt have an instance yet
    create_html_object(htmlObjectList, 'table', 'body')
    create_html_object(htmlObjectList, 'thead', 'table_1')
    create_html_object(htmlObjectList, 'tbody', 'table_1')
    create_html_object(htmlObjectList, 'tr', 'thead_1')
    create_html_object(htmlObjectList, 'th', 'tr_1')
    create_html_object(htmlObjectList, 'tr', 'tbody_1')
    create_html_object(htmlObjectList, 'td', 'tr_2')
    create_html_object(htmlObjectList, 'br', 'body')
    # create_table(htmlObjectList) # Create Table deprecated. just manually create html objects with for loops instead
    create_html_object(htmlObjectList, 'p', 'div_1')
    # td1 = find_obj_by_id(htmlObjectList, 'td1')
    # td1.appendAttrib([{'colspan': 2}])
    # td1.appendContent('Oranges')
    # print()
    # print(testP.tagCountDict)
    # for i in htmlObjectList:
    #     print()
    #     dictionary = i.convertToDict()
    #     for j in dictionary.items():
    #         print (j)

    # table = makeNewTag('table',body.tagID)
    # showCurrentHTMLStructure(htmlObjectList)
    # parseHtmlDocumentList(htmlObjectList)

def showTagsAndParents(thisTag):
    # print('\nThis Tag: %s [%s]' % (thisTag.tagID, str(thisTag)))
    # print('This Tag Parent: %s [%s] ' % (thisTag.parentID, str(thisTag.parentObject)))
    name = ''
    if type(thisTag.parentObject) == htmlgentools4.Tag:
        name = thisTag.parentObject.name
        print (name)


def findLastDirectChildOfParent(htmlObjectList, thisTag):
    numChildrenToFind = thisTag.parentObject.numChildrenElems
    numChildrenFound = 0
    i = htmlObjectList.index(thisTag.parentObject) + 1
    lastFoundIndex = i
    while (numChildrenFound < numChildrenToFind) and (i < len(htmlObjectList)):
        currentTag = htmlObjectList[i]
        if currentTag.parentObject == thisTag.parentObject:
            numChildrenFound += 1
            lastFoundIndex = i
            if currentTag.numChildrenElems > 0:
                i += currentTag.numChildrenElems # Experimental search speedup function. If problems arise, disable this
        i += 1
    if i > len(htmlObjectList): # DEBUG
        print("Got to the end of the document before enough children were found")
    return htmlObjectList[lastFoundIndex] # Returns the last child found  or the last element in the document


def findLastDescendentOfParentNew(htmlObjectList, thisTag):
    # This "Walks down the DOM" Starting at the location of this Tag's Parent
    # It uses the Tab Level Property to verify whether an item is a child or not
    # More tabs, mean its a child as its tabbed more deeply to the side, signifying that its a child
    # The tab level is determined by the parentID property  so it shouldn't be wrong.
    # If the tab value is less or equal to the parent level,
    # then you know it's not a child so you'll break at that
    # point and retun the index
    lastDirectChildObject = findLastDirectChildOfParent(htmlObjectList, thisTag)
    parentIndex = htmlObjectList.index(lastDirectChildObject)
    parentTabLevel = lastDirectChildObject.parentObject.tabLevel
    lastDescIndex = parentIndex
    for i in range(parentIndex+1,len(htmlObjectList),1):
        currentTag = htmlObjectList[i]
        if currentTag.tabLevel > parentTabLevel:
            lastDescIndex = i
        elif currentTag.tabLevel <= parentTabLevel: # Some potential code that can cause problems, but I think it will work
            break
    return lastDescIndex


def verify_obj_in_list(htmlObjectList, objToFind):
    isInList = False
    if (objToFind in htmlObjectList):
        isInList = True
    return isInList


def findParentIndex (htmlObjectList, thisTag):
    return htmlObjectList.index(thisTag.parentObject)  # Make this into one function?


def find_insertion_point(htmlObjectList, thisTag):
    tagListLength = len(htmlObjectList)
    if thisTag.parentID == 'none':
        # Elements without a parent can be appended right away
        # print("This %s tag's parentID is 'none'. Appending [%s]" % (thisTag.tagID, thisTag.tagID))
        return tagListLength
    if (verify_obj_in_list(htmlObjectList, thisTag.parentObject)):
        # print("%s's Parent: [%s] found in the htmlObjectList" % (thisTag.tagID, thisTag.parentObject.tagID))
        # First make sure the parent is in the list
        if thisTag.parentObject.numChildrenElems == 0:
            # print("%s's Parent: [%s] has no children yet. Appending [%s]" % (thisTag.tagID, thisTag.parentObject.tagID, thisTag.tagID))
            # If this object's parent doesn't have children yet, just insert it directly after the parent
            return (findParentIndex(htmlObjectList, thisTag)) + 1
        else:
            # print("%s's Parent: [%s] already has children. Have to find last descendent of [%s]" % (thisTag.tagID, thisTag.parentObject.tagID, thisTag.parentObject.tagID))
            return (findLastDescendentOfParentNew(htmlObjectList, thisTag)) + 1


def add_tag_obj_to_html_obj_list(htmlObjectList, thisTag):
    insertionPoint = find_insertion_point(htmlObjectList, thisTag)
    htmlObjectList.insert(insertionPoint, thisTag)


def test_document():
    if debug:
        print("new_html_document()")
    # Object Properties:
    # name, attr, hasNestedContent, numChildrenElems, parentID, content, tagID, selfClosing
    htmlObjectList = []
    thisTag = create_html_object(htmlObjectList, 'html') # Should always create the HTML Tag first
    thisTag = create_html_object(htmlObjectList, 'head') # Default value of 0 for parentID will nest things into the html tag by default
    thisTag = create_html_object(htmlObjectList, 'body')
    thisTag = create_html_object(htmlObjectList, 'p', 'body', [], "Testing Testing 1, 2, 3")

# test_document()
# tagTesting()