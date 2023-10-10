"""
CMSC 14100 Project
Winter 2023
"""

from version import Version, VersionException

class VersionSpecException(Exception):
    """
    A simple exception for Version error conditions. You should not
    modify this Class and you will not use until Part 2 of the project.
    """
    pass

class VersionSpecification:
    """
    A class to represent a semantic version specification that includes:

        - an optional specifier (~, ^, or +)
        - a version string (major.minor.patch)

    VersionSpec should support the ``str`` functionality by implementing the
    appropriate dunder method.
    """

    def __init__(self, spec_str):
        """
        Construct an instance of the VersionSpec class.

        Inputs:

            spec_str [str]: a version string, optionally augmented
              with a prefix of "~", "^" or "+"
        """
        fst_idx = ["~","^","+","1","2","3","4","5","6","7","8","9","0"]
        self.spec_str = spec_str
        if not isinstance(spec_str, str):
            error_msg = "Input in the VersionSpec constructor must be a string."
            raise VersionSpecException(error_msg)
        if spec_str == "":
            error_msg = "Input in the VersionSpec constructor cannot be an empty string."
            raise VersionSpecException(error_msg)
        if spec_str[0] not in fst_idx:
            error_msg = "Input in the VersionSpec constructor have a prefix or a digit."
            raise VersionSpecException(error_msg)
                
        mod_list = ["~","^","+"]
        if spec_str[0] in mod_list:
            self.mod = spec_str[0]
            sslist = spec_str[1:].split(".")
            try:
                i, j, k = sslist
                self.version = Version(int(i),int(j),int(k))
            except ValueError:
                error_msg = "Input must be an instance of the Version class."
                raise VersionSpecException(error_msg) 
            except VersionException:
                error_msg = "Input must be an instance of the Version class."
                raise VersionSpecException(error_msg)
            
        else:
            self.mod = None
            sslist = spec_str.split(".")
            try:
                i, j, k = sslist
                self.version = Version(int(i),int(j),int(k))
            except ValueError:
                error_msg = "Input must be an instance of the Version class."
                raise VersionSpecException(error_msg) 
            except VersionException:
                error_msg = "Input must be an instance of the Version class."
                raise VersionSpecException(error_msg)

    def satisfies_specification(self, ver):
        """
        Determine whether a given version meets the specification.

        Inputs:

            ver [Version]: the version to check

        Returns [bool]: True if the specified version meets the specification,
          and False otherwise.
        """
        if not isinstance(ver, Version):
            error_msg = "Input must be an instance of the Version class."
            raise VersionSpecException(error_msg)
        if self.mod == "~":
            match = (self.version.get_major() == ver.get_major() and
                    self.version.get_minor() == ver.get_minor())
            up = self.version <= ver
            return match and up
        elif self.mod == "^":
            match = self.version.get_major() == ver.get_major()
            up = self.version <= ver
            return match and up
        elif self.mod == "+":
            return self.version <= ver
        elif self.mod == None:
            return self.version == ver



    def __str__(self):
        """ Yields the augmented semantic version string """
        return f"{self.spec_str}"
