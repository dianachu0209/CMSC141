"""
CMSC 14100

Winter 2023

"""

# Feel free to add to this import statement
# It is OK if pylint complains about unused items.
import csv
from library import Library, LibraryException
from version import Version, VersionException, version_helper
from version_spec import VersionSpecification, VersionSpecException

class LibraryHubException(Exception):
    """
    A simple exception for described error conditions. You should not
    modify this class.
    """
    pass


class LibraryHub:
    """
    A class for a registry for managing libraries. 
    """
    def __init__(self):
        """
        Create a new LibraryHub instance.
        """
        self.Hub = {}
    

    def register_library(self, lib_name, version_str, registered_by):
        """
        Register a library with the hub

        Inputs

            lib_name(str): The name of the library  

            version_str (str): The semantic version number for the
              library

            registered_by (str): The name of the developer who
              registered the library
        
        Raises:

            LibraryHubException - if the values supplied for the library --
              lib_name, version_str, and registered_by-- do not meet
              the requirements for constructing a Library.

            LibraryHubException - if a library with the same name and version
              already exists

        Returns (Library):

            Returns the registered Library.
        """
        self.lib_name = lib_name
        try:
            self.library = Library(lib_name, version_str, registered_by)
        except LibraryException:
            error_msg = "Input must be valid to construct a Library"
            raise LibraryHubException(error_msg)
        self.version = version_helper(version_str)
        if self.lib_name not in self.Hub:
            libs = []
            libs.append(self.library)
        else:
            for nlib in self.Hub[lib_name]:
                if self.version == nlib.get_version():
                    error_msg = "library with the same name and version already exists."
                    raise LibraryHubException(error_msg)
            libs = self.Hub[lib_name]
            libs.append(self.library)
        self.Hub[lib_name] = libs
        return self.library
    

    def get_library(self, name, vspec_str):
        """
        Get a library with the specified name that matches the
        version specification string.  If more than one library
        matches, returns the latest version.

        Inputs:

            lib_name (str): the library name

            vspec_str (str): a version specification string

        Raises:

            LibraryHubException - if name is not a string

            LibraryHubException - if vspec_str not a valid version specification string


        Returns (Library):

            Returns the library with the latest release number that
            matches the version specification string, if one exists.
            None, if there are no libraries that match the
            specification.

        """
        self.name = name
        if not isinstance(name, str):
            error_msg = "name must be a string"
            raise LibraryHubException(error_msg)
        try:
            self.vspec = VersionSpecification(vspec_str)
        except VersionSpecException:
            error_msg = "vspec_sting must be a valid version specification string."
            raise LibraryHubException(error_msg)
        satislibs = []
        try:
            for lib in self.Hub[name]:
                if Library.satisfies_version_req(lib, self.vspec):
                    satislibs.append(lib)
        except KeyError:
            return None
        if satislibs == []:
            return None
        for lib in satislibs:
            current_max = lib
            if Library.is_later_version(lib, current_max):
                current_max = lib
        return current_max
        
    

    def add_dependency(self, lib_name, lib_ver, dep_name, dep_ver_spec):
        """
        Add a dependency that matches the dependency version
        specification to a library (known below as the
        receiving library).  The library receiving the dependency
        and the library that is identified as the dependency
        are expected to exist in the hub.


        Inputs:

            lib_name (str): the name of the receiving library

            lib_ver (str): the version string for the receiving library

            dep_name (str): the name of the dependency library

            dep_ver_spec (str): a version specification for the
                dependency

        Raises:

            LibraryHubException - if lib_name is not a string
        
            LibraryHubException - if lib_ver is not a valid version string
        
            LibraryHubException - if a library with the name and specified version
              does not exist

            LibraryHubException - if dep_name is not a string

            LibraryHubException - if dep_ver_spec is not a valid version
              specification string.

            LibraryHubException - if no libraries exist that have
              the specified dependency name and match the dependency
              specification.

            LibraryHubException - if the dependency is not valid for the
              receiving library.
        """
        
        if not isinstance(lib_name, str):
            error_msg = "name must be a string"
            raise LibraryHubException(error_msg)
        if not isinstance(dep_name, str):
            error_msg = "dep_name must be a string"
            raise LibraryHubException(error_msg)
        self.lib_name = lib_name
        try:
            self.lib_ver = version_helper(lib_ver)
        except VersionException:
            error_msg = "lib_ver must be a valid version string."
            raise LibraryHubException(error_msg)
        self.dep_name = dep_name
        try:
            self.dep_ver_spec = VersionSpecification(dep_ver_spec)
        except VersionSpecException:
            error_msg = "dep_ver_spec must be a valid version spec string."
            raise LibraryHubException(error_msg)
        if dep_name in self.Hub:
            dep_lib = self.get_library(dep_name, dep_ver_spec)
        else:
            error_msg = "valid dep library does not exist"
            raise LibraryHubException(error_msg)
        try:
            for lib in self.Hub[lib_name]:
                try:
                    if lib.get_version() == self.lib_ver:
                        Library.add_dependency(lib, dep_lib)
                except LibraryException:
                    error_msg = "dependency does not meet requirements."
                    raise LibraryHubException(error_msg)
        except KeyError:
            error_msg = "library with this name does not exist."
            raise LibraryHubException(error_msg)
        
    def remove_dependency(self, lib_name, lib_ver, dep_name, dep_ver):
        """
        Remove the dependency from the library.  Both the library and
        the dependency are expected to exist in the hub.

        Inputs:

            lib_name (str): the name of the library

            lib_ver (str): the version string for the library

            dep_name (str): the name of the dependency to be removed

            dep_ver (str): a version of the dependency to be removed

        Raises:

            LibraryHubException - if lib_name is not a string

            LibraryHubException - if lib_ver is not a valid version string
        
            LibraryHubException - if a library with the name and specified version
              does not exist

            LibraryHubException - if dep_name is not a string
        
            LibraryHubException - if dep_ver is not a valid version string

            LibraryHubException - if a library with the name and version specified
              for the dependency does not exist.
           
            LibraryHubException - if the library is not dependent upon
              the specified version.
        """

        if not isinstance(lib_name, str):
            error_msg = "name must be a string"
            raise LibraryHubException(error_msg)
        if not isinstance(dep_name, str):
            error_msg = "dep_name must be a string"
            raise LibraryHubException(error_msg)
        self.lib_name = lib_name
        try:
            self.lib_ver = version_helper(str(lib_ver))
        except VersionException:
            error_msg = "lib_ver must be a valid version string."
            raise LibraryHubException(error_msg)
        self.dep_name = dep_name
        try:
            self.dep_ver = version_helper(dep_ver)
        except VersionException:
            error_msg = "dep_ver_spec must be a valid version string."
            raise LibraryHubException(error_msg)
        if dep_name in self.Hub:
            dep_lib = self.get_library(dep_name, dep_ver)
        else:
            error_msg = "valid dep library does not exist"
            raise LibraryHubException(error_msg)
        try:
            for lib in self.Hub[lib_name]:
                try: 
                    if lib.get_version() == self.lib_ver:
                        try:
                            Library.remove_dependency(lib, dep_lib)
                        except LibraryException:
                            error_msg = "dep is not dependent on lib"
                            raise LibraryHubException(error_msg)
                except VersionException:
                    error_msg = "dep must exist to be compared"
                    raise LibraryHubException(error_msg)
        except KeyError:
            error_msg = "library with this name does not exist."
            raise LibraryHubException(error_msg)
    

    def get_contacts(self, lib_name, lib_ver, level=None):
        """
        Optional method: required only to earn an E.
        
        Get the set of contacts for all the libraries that the
        specified library requires up to the specified level
        in the dependency graph.

        Inputs:

            lib_name (str): the name of the library

            lib_ver (str): the version string for the library

            level (int or None): level of dependencies to traverse when
              collecting contacts.  (default is None, which means traverse
              all the levels).

        Raises:

            LibraryHubException - if lib_name is not a string

            LibraryHubException - if lib_ver is not a valid version string

            LibraryHubException - if a library with the name and specified version
              does not exist

            LibraryHubException - if level is something other than None or an
              integer that is greater than or equal to zero.

        Returns (set(str)):

            Returns a set of the names of the people who registered
            the libraries that the specified library requires.
        """
        raise NotImplementedError("TODO project 3") ### TODO        


def create_hub_from_file(filename):
    """
    This function is provided for you to use
    while you are testing your code.

    Load information about a set of libraries from
    a file into a hub.  Each line in the file
    describes one library: name, version string, the name
    of the person who registered the library.

    Inputs:

        filename (str): a file containing library
            registration information.

    Returns (LibraryHub):

        Returns a hub filled with the libraries
        described in the file.
    """
    lib_hub = LibraryHub()
    try:
        f = open(filename)
    except IOError as e:
        print(f"Could not open file: {filename}.")
        return None

    for i, row in enumerate(csv.reader(f)):
        if len(row) != 3:
            print(f"Skipping row {i}: row")
            continue
        lib_name, lib_ver, reg_by = row 
        try:
            lib = lib_hub.register_library(lib_name.strip(), lib_ver.strip(), reg_by.strip())
        except LibraryHubException:
            print(f"Was not able to register {lib_name} {lib_ver} {reg_by}")

    # close the file, we are done.
    f.close()
    
    return lib_hub
