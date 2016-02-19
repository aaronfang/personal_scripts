# ----------------------------------------------------------------------
# DreamWorks Animation LLC Confidential Information.
# TM and (c) 2015-16 DreamWorks Animation LLC. All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
# ----------------------------------------------------------------------
"""
sort.py

All the different sort classes.

The simplest way to use alpha numeric sorting is to use or pass this function:

alphaNumericSort

... as your favorite sort method. Otherwise, to access any of the methods in
this module, you'll need a class object. Since there are multiple classes in
this module, you'll need to be sure you create the correct object to access the
methods you want.

For example:

    comparatorObject = dwacore.utils.sort.Comparator()

        Now, you can access all of the Comparator class methods.

        comparatorObject.__init__()
        comparatorObject.getCompareFunction()
        comparatorObject.compare(myObject1, myObject2)
        comparatorObject.getSorter('mode_ids')
        comparatorObject.getSorter('mode_series')
        comparatorObject.isAlpha('a')
        comparatorObject.isDash('-')
        comparatorObject.isDot('.')
        comparatorObject.isNumber('234')
        comparatorObject.maxLength('firstString', 'secondString')

    alphaObject = dwacore.utils.sort.AlphaNumericComparator()

        Now, you can access all of the AlphaNumericComparator class methods.

        alphaObject.__init__()

    untokStringCompObject = dwacore.utils.sort.UntokenizedStringComparator()

        Now, you can access all of the UntokenizedStringComparator class 
        methods.

        untokStringCompObject.__init__()
        untokStringCompObject.getTokenizedStringComparatorFunction()
        untokStringCompObject.decompose("my5string6to7tokenize")
        untokStringCompObject.combineCharToToken(['my', '5', 'string', '6', 
                                                 'to', '7', 'tokenize'], 'a')
        untokStringCompObject.recompose([['my', '5', 'string', '6', 'to', 
                                                         '7', 'tokenize'])
        untokStringCompObject.compare(myObject1, myObject2)
"""
from __future__ import division

# $Source: /rel/cvsroot/mod/python/studio/utils/sort.py,v $



class Comparator(object):
    """
    This is the "interface" for all classes that can be returned
    by the static sort.getSorter(mode) function.
    All instances of subclasses of this class will have a function
    called compare(self, object1, object2) which allows the python sort 
    function to sort two objects accordingly.
    """
    def __init__(self):
        """
        Initalize the comparator.  Currently does nothing.

        Arguments:
            self - A reference to the Comparator object.

        Returns:
            None
        """
        pass

    def getCompareFunction(self):
        """
        Returns the compare attribute.
        
        Arguments:
            self - A reference to the Comparator object.
        
        Returns:
            The compare attribute.
        """
        return getattr(self, "compare")

    def compare(self, object1, object2):
        """
        This forces subclassse to implement this function which compares two
        objects and returns an integer indicating whether they are equal, 
        less than, or greater than.

        Arguments:
            self - A reference to the Comparator object.
            object1 - The first object to compare.
            object2 - The second object to compare.

        Returns:
            Raises a NotImplementedError()
        """
        raise NotImplementedError()

    def getSorter(mode):
        """
        This function is a static function which will return a class having 
        a comparator function that can be passed to python's sort function
        mode: the type of sort needed.

        Arguments:
            mode - A string indicating the mode of the comparator function
                   you want.  Currently, 'mode_ids' for the 
                   DecimalAsISUntokenizedStringComparator and 'mode_series'
                   for the DecimalAsSequenceUntokenizedStringComparator.

        Returns:
            A reference to the specified function.
        """
        if (mode == AlphaNumericComparator.MODE_IDS):
            return DecimalAsIDUntokenizedStringComparator()
        elif (mode == AlphaNumericComparator.MODE_SERIES):
            return DecimalAsSequenceUntokenizedStringComparator()
    getSorter = staticmethod(getSorter)

    def isAlpha(char):
        """
        Lets you know if a character is alphabetic or not.

        Arguments:
            char - A character.

        Returns:
            True - The character is alphabetic.
            False - The character is not alphabetic.
        """
        return char.isalpha()
    isAlpha = staticmethod(isAlpha)
    
    def isDash(char):
        """
        Lets you know if a character is a dash.
        
        Arguments:
            char - The character to be checked for "dashness".

        Returns:
            True - The character is a dash. 
            False - The character is not a dash.
        """
        return char == "-"
    isDash = staticmethod(isDash)

    def isDot(char):
        """
        Lets you know if a character is a period.
                                                                               
        Arguments:
            char - The character to be checked.
                                                                               
        Returns:
            True - The character is a period.
            False - The character is not a period.
        """
        return char == "."
    isDot = staticmethod(isDot)

    def isNumber(string):
        """
        Lets you know if a string contains ANY (not necessarily all) digits.           Assumes that the decompose/recompose processing has already 
        separated alpha, number, and other tokens. 
        
        Arguments:
            string - The string to be checked for "numberness".
        
        Returns:
            True - The string contains a number.
            False - There are no numbers in the string.
        """
        #return string.isdigit()
        for char in string:
            if (char.isdigit()):
                return True
        return False
    isNumber = staticmethod(isNumber)

    def maxLength(string1, string2):
        """
        Gives the maximum length of the two strings input.
        
        Arguments:
            string1 - The first string to compare.
            string2 - The second string to compare.

        Returns:
            An integer representing max length.
        """
        return max(len(string1), len(string2))
    maxLength = staticmethod(maxLength)

class AggregrateComparator(Comparator):
    """
    upon calling the getCompareFunction of this class,
    returns a (curried) compare function
    which will compare two rows based upon a list of (columnIdx, cmpFunction) pairs
    example: each row has type (date,number,id)
    to sort using (descendingDate, ascendingID)
    this class should be created with the argument
    compareInfoList = [(0,descendingDateCmp),(2,ascendingStringCmp)]
    """    
    def __init__(self, compareInfoList):
        self.__compareInfoList = compareInfoList
        

    def compare(self, x, y):
        """
        iterates through the elements of compareInfoList,
        each of which is a tuple- (columnIdx, columnCmpFunction)
        will sort x,y (assumed to be rows of a table)
        according to the values at the columnIdx
        using the corresponding columnCmpFunction
        """
        for compareInfo in self.__compareInfoList:
            columnIdx, function = compareInfo
            cmpValue = function(x[columnIdx], y[columnIdx])
            if (cmpValue != 0):
                return cmpValue
            pass
        return 0

    
class AlphaNumericComparator(Comparator):
    """
    This will act as the parent class to the two alphanumeric comparators 
    we have.

    Sorts lexically on alphabetic elements of strings and numerically on 
    numeric elements of strings.

    There are two ways that decimal numbers can be handled:

    In "IDS" mode, decimal numbers are sorted as actual numbers. This is the 
    mode to use when sorting sequence and shot names. For example, sq1.25 
    should sort between sq1.2 and sq1.3. IDS would sort: -3, -2, -1.2, -1.15, 
    -0.5, 0.5, 1.15, 1.2, 2, 3. IDS would sort .001 less than .01 (first is 
    considered 1, second is considered 10)
    
    In "SERIES" mode, decimal numbers are sorted assuming that the decimal 
    is actually a field separator. This is the mode to use when sorting file 
    names. For example, frame.25 (that is, twenty five) should sort after 
    frame.3 (that is, frame 3). SERIES would sort: -3, -2, -1.15, -1.2, -0.5, 
    0.5, 1.2, 1.15, 2, 3. SERIES would sort .001 equal to .01 (both are 
    considered 1 with different padding).
    
    Unfortunately, there is no way to sort full file specs if they include 
    strings of both types (e.g., /prod/sq1.25/s1/frame.25). You have to pick 
    one or the other mode, or you have to tokenize the path names and sort 
    individual directory contexts in their appropriate modes.
    """

    MODE_IDS = "mode_ids"
    MODE_SERIES = "mode_series"

    
    def __init__(self):
        """
        Initalizes the AlphaNumericComparator.

        Arguments:
            self - A reference to the AlphaNumericComparator object.

        Returns:
            None
        """
        Comparator.__init__(self)


class UntokenizedStringComparator(AlphaNumericComparator):
    """
    A specialized subclass of AlphaNumericComparator.
    """
    def __init__(self):
        """
        Initalizes the UntokenizedStringComparator.
        
        Arguments:
            self - A reference to the UntokenizedStringComparator object.

        Returns:
            None
        """
        AlphaNumericComparator.__init__(self)

    def getTokenizedStringComparatorFunction(self):
        """
        Gives a reference to the comparator function attribute.

        Arguments:
            self - A reference to the UntokenizedStringComparator object.
    
        Returns:
            Raises a NotImplementedError.
        """
        raise NotImplementedError
    
    def decompose(self, string):
        """
        Decomposes a string into its digit, alpha, and misc parts.

        Arguments:
            self - A reference to the UntokenizedStringComparator object.
            string - The string to decompose.

        Returns:
            tokenList - A list of the string's tokens.
        """
        tokenList = []
        try:
            tokenList = reduce(self.combineCharToToken, [[string[0]]]+[x \
                        for x in string[1:]])
        except IndexError:
            #this means that string was empty
            pass
            
        return tokenList

    def combineCharToToken(self, tokenList, char):
        """
        Adds a character to a given token list.

        Arguments:
            self - A reference to the UntokenizedStringComparator object.
            tokenList - A list of tokens.
            char - A character.

        Returns:
            tokenList - The new list of tokens.
        """
        lastToken = tokenList[-1]
        combinedWithLastFragment = False
        for function in [self.isAlpha, self.isNumber]:            
            if function(char) and function(lastToken):
                tokenList[-1] = lastToken+char
                combinedWithLastFragment = True
                break

        if not combinedWithLastFragment:
            tokenList.append(char)

        return tokenList


    def recompose(self, tokenList):
        """
        Recompses a list of tokens back into a string.

        Arguments:
            self - A reference to the UntokenizedStringComparator object.
            tokenList - A list of tokens.

        Returns:
            combinedList - The recombined string.
        """
        combinedList = []

        i=0
        #for i in range(0,len(tokenList)):
        while (i<len(tokenList)):
            token = tokenList[i]

            if (self.isNumber(token) or self.isDash(token) or self.isDot\
                                                                (token)):
                nextTokens = tokenList[i+1:i+4]
                
                if (self.isDash(token) and len(nextTokens) >= 3):
                    #check if is a negative number with a fractional component
                    #eg -0.3 or -1.7
                    dashNumDotNumFormat = self.isNumber(nextTokens[0]) and \
                                          self.isDot(nextTokens[1]) and \
                                          self.isNumber(nextTokens[2])
                    if (dashNumDotNumFormat):
                        combinedList.append("".join([token]+nextTokens))
                        i+=4
                        continue

                if ((not self.isDot(token)) and len(nextTokens) >= 2):
                    #check if is a negative number between 0 and -1
                    #eg -.3
                    dashDotNumFormat = self.isDash(token) and \
                                       self.isDot(nextTokens[0]) and \
                                       self.isNumber(nextTokens[1])

                    #check if is a negative integer ending with a period <= -1
                    dashNumDotFormat = self.isDash(token) and \
                                       self.isNumber(nextTokens[0]) and \
                                       self.isDot(nextTokens[1])

                    #check if is a positive number with a fractional component
                    numDotNumFormat = self.isNumber(token) and \
                                      self.isDot(nextTokens[0]) and \
                                      self.isNumber(nextTokens[1])

                    if (dashDotNumFormat or \
                        dashNumDotFormat or \
                        numDotNumFormat):
                        i+=3
                        combinedList.append("".join([token]+nextTokens[0:2]))
                        continue

                if (len(nextTokens) >= 1):
                    #check if is a negative integer <= -1 (no ending period)
                    dashNumFormat = self.isDash(token) and \
                                    self.isNumber(nextTokens[0])
                    #check if is a positive number between 0 and 1
                    dotNumFormat = self.isDot(token) and \
                                   self.isNumber(nextTokens[0])
                    #check if is an integer with a ending period, >= 0
                    numDotFormat = self.isNumber(token) and \
                                   self.isDot(nextTokens[0])

                    if (dashNumFormat or dotNumFormat or numDotFormat):
                        i+=2
                        combinedList.append("".join([token]+nextTokens[0:1]))
                        continue
                
            #No other ways to legally combine dots, dashes, and digits
            #exist, so accept token on its own.
            i+=1
            combinedList.append(token)


        return combinedList
    

    def compare(self, object1, object2):
        """
        Compares two objects and returns an integer depecting whether the
        objects were equal, greater than or less than. Does not assume that 
        the strings have to contain a character of only one of 
        (alpha|number|misc).

        Arguments:
            self - A reference to the UntokenizedStringComparator object.
            object1 - The first object to compare.
            object2 - The second object to compare.

        Returns:
            0 - The objects are equal.
            0 > - The first object is less than the second.
            0 < - The first object is greater than the second.
        """
        if not (isinstance(object1, basestring) and
                isinstance(object2, basestring)):
            
            raise ValueError("Cannot compare non-strings")

        #Split string A into alphabetic, numeric, and other tokens.
        #Split string B into alphabetic, numeric, and other tokens.
        original = [object1, object2]
        decomposed = [self.decompose(x) for x in original]
        recomposed = [self.recompose(x) for x in decomposed]

        #Compare strings by comparing each successive token.
        f = self.getTokenizedStringComparatorFunction()
        for i in range(0, min([len(x) for x in recomposed])):
            token1 = recomposed[0][i]
            token2 = recomposed[1][i]
            #compare the two tokens
            #if they are not the same, then we are done, and can return the 
            #value - otherwise, continue
            cmpValue = f(token1, token2)
            if cmpValue != 0:
                return cmpValue
        
        #All tokens up to the end of one or both strings compared
        #equal. At this point, how they compare depends on which has less 
        #tokens
        len1 = len(recomposed[0])
        len2 = len(recomposed[1])

        return len1 - len2

class DecimalAsIDUntokenizedStringComparator(UntokenizedStringComparator):
    """
    In "IDS" mode, decimal numbers are sorted as actual numbers. This
    is the mode to use when sorting sequence and shot names. For
    example, sq1.25 should sort between sq1.2 and sq1.3.
    IDS would sort: -3, -2, -1.2, -1.15, -0.5, 0.5, 1.15, 1.2, 2, 3
    IDS would sort .001 less than .01 (first is considered 1, second is
    considered 10)
    """
    def getTokenizedStringComparatorFunction(self):
        """
        Returns the compare function being used.

        Arguments:
            self - A reference to the DecimalAsIDUntokenizedStringComparator
                   object.

        Returns:
            The compare function being used.
        """
        return DecimalAsIDTokenizedStringComparator().getCompareFunction()

class DecimalAsSequenceUntokenizedStringComparator(UntokenizedStringComparator):
    """
    In "SERIES" mode, decimal numbers are sorted assuming that the
    decimal is actually a field separator. This is the mode to use when
    sorting file names. For example, frame.25 (that is, twenty five)
    should sort after frame.3 (that is, frame 3).
    SERIES would sort: -3, -2, -1.15, -1.2, -0.5, 0.5, 1.2, 1.15, 2, 3
    SERIES would sort .001 equal to .01 (both are considered 1 with
    different padding).
    """
    
    def getTokenizedStringComparatorFunction(self):
        """
        Returns the compare function being used.
                                                                               
        Arguments:
            self - A reference to the DecimalAsSequenceUntokenizedString-
                   Comparator object.
                                                                               
        Returns:
            The compare function being used.
        """

        return DecimalAsSequenceTokenizedStringComparator().\
                                       getCompareFunction()

class TokenizedStringComparator(AlphaNumericComparator):
    """
    A specialized subclass of AlphaNumericComparator.
    """
    def __init__(self):
        """
        Initalizes the TokenizedStringComparator.

        Arguments:
            self - A reference to the TokenizedStringComparator object.

        Returns:
            None
        """
        AlphaNumericComparator.__init__(self)

    def formatFractionalStringComponents(self, fractionList):
        """
        Raises a NotImplementedError.
        """
        raise NotImplementedError
    
    def compare(self, object1, object2):
        """
        Compares two objects and returns an integer indicating whether they
        are equal, greater than or less than.

        Arguments:
            self - A reference to the TokenizedStringComparator object.
            object1 - The first object to compare.
            object2 - The second object to compare.

        Returns:
            0 - The objects are equal.
            0 > - The first object is less than the second.
            0 < - The first object is greater than the second.
        """
        if not (isinstance(object1, basestring) and
                isinstance(object2, basestring)):
            raise ValueError("Cannot compare non-strings")

        obj1IsNum = self.isNumber(object1)
        obj2IsNum = self.isNumber(object2)

        if (obj1IsNum and obj2IsNum):
            #because both are numbers, that means they have at least one 
            #char each
            obj1IsNegative = self.isDash(object1[0])
            obj2IsNegative = self.isDash(object2[0])

            if (obj1IsNegative and (not obj2IsNegative)):
                return -1
            elif ((not obj1IsNegative) and obj2IsNegative):
                return 1

            #if obj1 is negative, both are negative
            if (obj1IsNegative):
                #since both are negative, swap their values
                objectTmp = object1[1:]
                object1 = object2[1:]
                object2 = objectTmp

            parts1 = object1.split(".")
            parts2 = object2.split(".")

            exponent1 = int(parts1[0] or "0")
            exponent2 = int(parts2[0] or "0")

            cmpValue = cmp(exponent1, exponent2)
            #if the exponents are not the same, just return their comparison
            if cmpValue != 0:
                return cmpValue

            #handle the case where there was no fractional component
            if (len(parts1) < 2):
                parts1.append("0")
            if (len(parts2) < 2):
                parts2.append("0")

            #handle the case where "3." was split into ["3", ""]
            parts1[1] = parts1[1] or "0"
            parts2[1] = parts2[1] or "0"

            object1,object2 = self.formatFractionalStringComponents(\
                                             [parts1[1], parts2[1]])

            return cmp(object1, object2)
            
        else:
            #just compare lexically
            #need to do this to ignore case unless
            return cmp(object1.lower(), object2.lower()) or cmp(object1, \
                                                                object2)

        return 0


class DecimalAsIDTokenizedStringComparator(TokenizedStringComparator):
    """
    * In "IDS" mode, decimal numbers are sorted as actual numbers. This
    * is the mode to use when sorting sequence and shot names. For
    * example, sq1.25 should sort between sq1.2 and sq1.3.
    * IDS would sort: -3, -2, -1.2, -1.15, -0.5, 0.5, 1.15, 1.2, 2, 3
    * IDS would sort .001 less than .01 (first is considered 1, second is
    * considered 10)
    """

    def formatFractionalStringComponents(self, stringList):
        length = reduce(self.maxLength, stringList)
        return [string+("0"*(length-len(string))) for string in stringList]


class DecimalAsSequenceTokenizedStringComparator(TokenizedStringComparator):
    """
    * In "SERIES" mode, decimal numbers are sorted assuming that the
    * decimal is actually a field separator. This is the mode to use when
    * sorting file names. For example, frame.25 (that is, twenty five)
    * should sort after frame.3 (that is, frame 3).
    * SERIES would sort: -3, -2, -1.15, -1.2, -0.5, 0.5, 1.2, 1.15, 2, 3
    * SERIES would sort .001 equal to .01 (both are considered 1 with
    * different padding).
    """

    def formatFractionalStringComponents(self, stringList):
        return [int(x or "0") for x in stringList]


# Simple shortcut to sort function
alphaNumericSort = \
    AlphaNumericComparator.getSorter(
        AlphaNumericComparator.MODE_SERIES).getCompareFunction()
        

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# TM and (c) 2015-16 DreamWorks Animation LLC. All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
# DreamWorks Animation LLC Confidential Information.
# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.

#import dwacore.utils.sort
#import odwmaya

def mod_surfSortList(items):
    """Sort the given list of objects and reorder them in the maya scene.
    """
    # make a shallow copy of items
    # 
    items = [i for i in items]

    # Sort items
    # 
    items.sort(cmp=alphaNumericSort)
    
    for item in items:
        cmds.reorder(item, back=True)

    for item in items:
        children = cmds.listRelatives(item, f=1)
        if children:
            mod_surfSortList(children)
        
def mod_surfSort():
    """Sort the selected items according to name.
    """
    selected = cmds.ls(sl=True, l=True)
    mod_surfSortList(selected)
    
mod_surfSort()


# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
