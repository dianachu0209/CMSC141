"""
CMSC 14100
Winter 2023
"""
from version import Version, VersionException, version_helper
from version_spec import VersionSpecification, VersionSpecException


class LibraryException(Exception):
    """
    A simple exception for described error conditions. You should not
    modify this Class at all.
    """
    pass


class Library:
    """
    A class to represent a published library. This class will have public
    attributes for:

        - A name
        - A version, and
        - The name of the person who registered the library

    Library should support the ``str`` functionality by implementing the
    appropriate dunder method.
    """

    def __init__(self,
                 name,
                 version_str,
                 registered_by,
                 ):
        """
        Create a new library.

        Inputs:

            name(str): The name of the library

            version_str (str): The semantic version number

            registered_by (str): The name of the developer who
              registered the library

        Raises:

            LibraryException - if the supplied version string is not a
              valid version string.

        """
        
        self.name = name
        if not isinstance(name, str):
            error_msg = "name must be a string."
            raise LibraryException(error_msg)
        self.version_str = version_str
        if not isinstance(version_str, str):
            error_msg = "version_str must be a string."
            raise LibraryException(error_msg)
        if version_helper(version_str) is None:
            error_msg = "version_str must be an instance of the Version class."
            raise LibraryException(error_msg)
        self.registered_by = registered_by
        if not isinstance(registered_by, str):
            error_msg = "registered_by must be a string."
            raise LibraryException(error_msg)
        self.__dependencies = {}
    
    def get_name(self):
        """
        ** New in Part 3 **

        Return (str): the library's name
        """
        return self.name

    def get_version(self):
        """
        ** New in Part 3 **

        Return (Version): the library's version
        """
        ver = version_helper(self.version_str)
        return ver
    
    def get_registered_by(self):
        """
        ** New in Part 3 **

        Return (str): the information about who registered the library
        """
        return self.registered_by


    def is_stable(self):
        """
        Is this library stable, that is, does it have a stable version number.

        Returns (bool):

            True if the library has a stable version number, False otherwise.
        """
        return int(self.version_str[0]) != 0


    def satisfies_version_req(self, version_spec):
        """
        Checks if this Library satisfies the version specification

        Inputs:

            version_spec (VersionSpecification): the version specification
              that is of interest

        Raises:

            LibraryException - if version_spec is not an instance of the
              VersionSpecification class

        Returns (bool):

            Returns True if the library's version satisfies the provided
            version specification and False, otherwise.
        """
        if not isinstance(version_spec, VersionSpecification):
            error_msg = "version_spec must be an instance of VersionSpecification."
            raise LibraryException(error_msg)
        interest = version_helper(self.version_str)
        x = VersionSpecification.satisfies_specification(version_spec, interest)
        return x


    def is_later_version(self, other):
        """
        Does this library's version come after the other library's
        version in the semantic version ordering?

        Inputs:

            other (Library): the library to check

        Raises:

            LibraryException - if other is not an instance of the Library class

            LibraryException - if other does not have the same library name as
              this library

        Returns (bool):

            Returns True if this library's version comes later in the
              semantic version ordering than other's.  False, otherwise.
        """
        if not isinstance(other, Library):
            error_msg = "other must be an instance of Library"
            raise LibraryException(error_msg)
        if self.name != other.name:
            error_msg = "libraries must have the same names"
            raise LibraryException(error_msg)
        this_library = version_helper(self.version_str)
        other_library = version_helper(other.version_str)
        return this_library > other_library

    def check_lib(self, dep):
        """
        Checks if a dependent library is dependent on the library of interest.

        Inputs:
            dep (Library): the library being checked

        Returns (bool): True if the library is dependent on itself.
        """
        if dep.name == self.name:
            return True
        else:
            for dependent in dep.__dependencies:
                return self.check_lib(dep.__dependencies[dependent])
            return False

    def add_dependency(self, dep):
        """
        Add dep as a library that this one depends upon.

        Inputs:

            dep (Library): the library to add as a dependency

        Raises:

            LibraryException - if dep is not an instance of the Library class

            LibraryException - if this library is stable and dep is not a stable
              library.

            LibraryException - if this library already depends on a library with
              the same name as dep.

            LibraryException - if dep has the same name as this library or requires
              a library with the same name as this library.  ** New in Part 3 **
        """
        if not isinstance(dep, Library):
            error_msg = "dep must be an instance of the Library class."
            raise LibraryException(error_msg)
        if self.is_stable() and (dep.is_stable() == False):
            error_msg = "dep can only be unstable if existing library is unstable."
            raise LibraryException(error_msg)
        if dep.name in self.__dependencies:
            error_msg = "other version of dep already exists in library."
            raise LibraryException(error_msg)
        if self.check_lib(dep):
            error_msg = "library cannot depend on a library with the same name."
            raise LibraryException(error_msg)
        self.__dependencies[dep.name] = dep


    def remove_dependency(self, dep):
        """
        Remove dep from dependencies for this library

        Inputs:

            dep (Library): the library that to remove as a dependency


        Raises:

            LibraryException - if dep is not an instance of the Library class

            LibraryException - if this library is not dependent on the
              library dep.
        """
        if not isinstance(dep, Library):
            error_msg = "dep must be an instance of the Library class."
            raise LibraryException(error_msg)
        if dep.name not in self.__dependencies:
            error_msg = "library is not dependent on dep."
            raise LibraryException(error_msg)
        elif dep.name in self.__dependencies:
            dep_lib = self.__dependencies[dep.name] 
            if dep_lib.get_version() != dep.get_version():
                error_msg = "library is not dependent on dep."
                raise LibraryException(error_msg)
        del self.__dependencies[dep.name]
            

    def __str__(self):
        """
        Construct a string:
        """
        library_info = f"{self.name} {self.version_str} {self.registered_by}"
        return f"Library: {library_info} Dependencies: {self.__dependencies}"
