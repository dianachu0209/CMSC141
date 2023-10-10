"""
CMSC 14100 Project
Winter 2023
"""

class VersionException(Exception):
    """
    A simple exception for Version error conditions. You should not
    modify this Class and you will not use until Part 2 of the project.
    """
    pass


class Version:
    """
    A class to represent an exact semantic version that includes:

        - a major release number
        - a minor release number
        - a patch release number

    All three parts are required.

    Version should support the following functionality by implementing the
    appropriate dunder methods:

    - str(v) - constructs a version string major.minor.patch

    - v1 == v2 - version v1 and version v2 represent the same semantic version

    - v1 != v2 - version v1 and version v2 do not represent the
         same semantic version

    - v1 < v2 - version v1 comes earlier in the semantic version
         ordering than v2

    - v1 <= v2 - version v1 comes earlier in the semantic version
         ordering than v2 or v1 and v2 represent the same semantic version

    - v1 > v2 - version v1 comes later in the semantic version ordering
         than v2

    - v1 >= v2 - version v1 comes later in the semantic version ordering
         than v2 or v1 and v2 represent the same semantic version
    """
    def __init__(self, major, minor, patch):
        """
        Create a new Version instance from the specified release numbers.

        Inputs:

            major (int): the major release number
            minor (int): the minor release number
            patch (int): the patch release number
        """
        
        if not isinstance(major, int):
            error_msg = "All release numbers in the Version constructor must be integers."
            raise VersionException(error_msg)
        if not isinstance(minor, int):
            error_msg = "All release numbers in the Version constructor must be integers."
            raise VersionException(error_msg)
        if not isinstance(patch, int):
            error_msg = "All release numbers in the Version constructor must be integers."
            raise VersionException(error_msg)
        if major < 0 or minor < 0 or patch < 0:
            error_msg = "All release numbers in the Version constructor must be greater than or equal to zero."
            raise VersionException(error_msg)

        self.__major = major
        self.__minor = minor
        self.__patch = patch


    def get_major(self):
        """ Return the major release number from the version"""
        return self.__major


    def get_minor(self):
        """ Return the minor release number from the version"""
        return self.__minor


    def get_patch(self):
        """ Return the patch release number from the version"""
        return self.__patch


    def is_stable(self):
        """
        Is this version stable?
        """
        return self.__major != 0


    def __str__(self):
        """
        Constructs a string representation of the version with
        the components separated by periods.

        Sample use: str(Version(3, 2, 1)) yields "3.2.1"
        """
        return f"{self.__major}.{self.__minor}.{self.__patch}"


    def __eq__(self, other):
        """
        Does this version (self) represent the same semantic version as other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        return str(self) == str(other)


    def __ne__(self, other):
        """
        Does this version (self) represent a different semantic version
        than other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        return not self == other


    def __gt__(self, other):
        """
        Does this version (self) come later in the semantic version
        ordering than other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if str(self) == str(other):
            return False
        if self.get_major() < other.get_major():
            return False
        elif self.get_major() == other.get_major():
            if self.get_minor() < other.get_minor():
                return False
            elif self.get_minor() == other.get_minor():
                if self.get_patch() < other.get_patch():
                    return False
        return True


    def __ge__(self, other):
        """
        Does this version (self) come later in the semantic version
        ordering than other or, alternatively, does it represent the
        same semantic version as other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        return self == other or self > other


    def __lt__(self, other):
        """
        Does this version (self) come earlier in the semantic version
        ordering than other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if str(self) == str(other):
            return False
        if self.get_major() > other.get_major():
            return False
        elif self.get_major() == other.get_major():
            if self.get_minor() > other.get_minor():
                return False
            elif self.get_minor() == other.get_minor():
                if self.get_patch() > other.get_patch():
                    return False
        return True
    
    def __le__(self, other):
        """
        Does this version (self) come earlier in the semantic version
        ordering than other or, alternatively, does it represent the
        same semantic version as other?
        """
        if not isinstance(self, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        if not isinstance(other, Version):
            error_msg = "Version must exist to be compared"
            raise VersionException(error_msg)
        return self == other or self < other

def version_helper(spec_str):
    """
    Make a string into an instance of the verion class

    Inputs:
    spec_str [str]: a version string, optionally augmented
        with a prefix of "~", "^" or "+"
    
    Returns an instance of Version if string is valid, None otherwise
    """
    mod_list = ["~","^","+"]
    if spec_str[0] in mod_list:
        sslist = spec_str[1:].split(".")
        try:
            i, j, k = sslist
            version = Version(int(i),int(j),int(k))
        except ValueError:
            return None
        except VersionException:
            return None
        return version
    if spec_str[0] not in mod_list and spec_str[0].isdigit():
        sslist = spec_str.split(".")
        try:
            i, j, k = sslist
            version = Version(int(i),int(j),int(k))
        except ValueError:
            return None
        except VersionException:
            return None
        return version
    else:
        return None