# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2019-2021, Science and Technology Facilities Council.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
# Author J. Henrichs, Bureau of Meteorology
# Modified by: S. Siso, STFC Daresbury Laboratory
#              A. R. Porter, STFC Daresbury Laboratory
# -----------------------------------------------------------------------------

'''This module provides management of variable access information.'''

from __future__ import print_function, absolute_import

from psyclone.core.access_type import AccessType
from psyclone.core.signature import Signature
from psyclone.errors import InternalError


class AccessInfo(object):
    '''This class stores information about a single access
    pattern of one variable (e.g. variable is read at a certain location).
    A location is a number which can be used to compare different accesses
    (i.e. if one access happens before another). Each consecutive
    location will have an increasing location number, but read and write
    accesses in the same statement will have the same location number.
    If the variable accessed is an array, this class will also store
    the indices used in the access.
    Note that the name of the variable is not stored in this class.
    It is a helper class used in the `SingleVariableAccessInfo` class,
    which stores all `AccessInfo` objects for a variable, and it stores
    the name of the variable.

    :param access: the access type.
    :type access_type: :py:class:`psyclone.core.access_type.AccessType`
    :param int location: a number used in ordering the accesses.
    :param indices_groups: indices used in the access, defaults to None
    :type indices_groups: list of list of
        :py:class:`psyclone.psyir.nodes.Node` (e.g. Reference, ...)
    :param node: Node in PSyIR in which the access happens, defaults to None.
    :type node: :py:class:`psyclone.psyir.nodes.Node`

    '''
    def __init__(self, access_type, location, node, indices_groups=None):
        self._location = location
        self._access_type = access_type
        self._node = node
        self.indices_groups = indices_groups

    def __str__(self):
        '''Returns a string representating showing the access mode
        and location, e.g.: WRITE(5).'''
        return "{0}({1})".format(self._access_type, self._location)

    def change_read_to_write(self):
        '''This changes the access mode from READ to WRITE.
        This is used for processing assignment statements,
        where the LHS is first considered to be READ,
        and which is then changed to be WRITE.

        :raises InternalError: if the variable originally does not have\
            READ access.

        '''
        if self._access_type != AccessType.READ:
            raise InternalError("Trying to change variable to 'WRITE' "
                                "which does not have 'READ' access.")
        self._access_type = AccessType.WRITE

    @property
    def indices_groups(self):
        '''
        This function returns the list of accesses used for each component,
        e.g. `a(i)%b(j,k)%c` will return `[ [i], [j, k], [] ]`. Especially
        in case of a simple scalar variable `a` this function will still
        return `[ [] ]`. Each entry in this list of lists will be a PSyIR
        node of the index expression used.
        :returns: the indices used in this access for each component.
        :rtype: list of list of :py:class:`psyclone.psyir.nodes.Node`
        '''
        return self._indices_groups

    @indices_groups.setter
    def indices_groups(self, indices_groups):
        '''Sets the indices for this AccessInfo instance.

        :param indices_groups: list of indices used in the access.
        :type indices_groups: list of list of \
            py:class:`psyclone.psyir.nodes.Node`

        :raises InternalError: if the indices_groups is not a list of lists.

        '''
        if indices_groups:
            if not isinstance(indices_groups, list):
                raise InternalError("Indices_groups in add_access must be a "
                                    "list or None, got '{0}'".
                                    format(indices_groups))
            for indices in indices_groups:
                if not isinstance(indices, list):
                    raise InternalError("Indices_groups in add_access must be "
                                        "a list of lists, or None, got '{0}'".
                                        format(indices_groups))
            self._indices_groups = indices_groups[:]
        else:
            self._indices_groups = [[]]

    def is_array(self):
        '''Test if any of the components has an index. E.g. an access like
        a(i)%b would still be considered an array.

        :returns: if any of the variable components uses an index, i.e.\
            the variable is an array.
        :rtype: bool
        '''
        for list_of_indices in self._indices_groups:
            if list_of_indices != []:
                return True
        return False

    @property
    def access_type(self):
        ''':returns: the access type.
        :rtype: :py:class:`psyclone.core.access_type.AccessType`'''
        return self._access_type

    @property
    def location(self):
        ''':returns: the location information for this access.\
        Please see the Developers' Guide for more information.
        :rtype: int
        '''
        return self._location

    @property
    def node(self):
        ''':returns: the PSyIR node at which this access happens.
        :rtype: :py:class:`psyclone.psyir.nodes.Node` '''
        return self._node


# =============================================================================
class SingleVariableAccessInfo(object):
    '''This class stores a list with all accesses to one variable.

    :param signature: signature of the variable.
    :type signature: :py:class:`psyclone.core.signature`

    '''
    def __init__(self, signature):
        self._signature = signature
        # This is the list of AccessInfo instances for this variable.

        self._accesses = []

    def __str__(self):
        '''Returns a string representation of this object with the format:
        var_name:WRITE(2),WRITE(3),READ(5) where the numbers indicate
        the 'location' of the corresponding access. The location is an
        integer number that enumerates each statement in a program unit,
        and can be used to compare if an access is earlier, later or in
        the same statement as another access.

        '''
        return "{0}:{1}".format(self._signature,
                                ",".join([str(access)
                                          for access in self._accesses]))

    @property
    def var_name(self):
        ''':returns: the name of the variable whose access info is managed.
        :rtype: str
        '''
        return str(self._signature)

    def get_all_accesses_of_type(self, access_type):
        '''Returns all access in var_info of the given type.

        :param access_type: the type of access (READ, WRITE, ....)
        :type access_type: \
            :py:class:`psyclone.core.access_type.AccessType`

        '''
        return [access for access in self.all_accesses
                if access.access_type is access_type]

    def is_written(self):
        ''':returns: True if this variable is written (at least once).
        :rtype: bool
        '''
        return any(access_info.access_type in
                   AccessType.all_write_accesses()
                   for access_info in self._accesses)

    def is_read_only(self):
        '''Checks if this variable is always read, and never
        written.

        :returns: True if this variable is read only.
        :rtype: bool
        '''
        return all(access_info.access_type == AccessType.READ
                   for access_info in self._accesses)

    def is_read(self):
        ''':returns: True if this variable is read (at least once).
        :rtype: bool
        '''
        return any(access_info.access_type in AccessType.all_read_accesses()
                   for access_info in self._accesses)

    def has_read_write(self):
        '''Checks if this variable has at least one READWRITE access.

        :returns: True if this variable is read (at least once).
        :rtype: bool
        '''
        return any(access_info.access_type == AccessType.READWRITE
                   for access_info in self._accesses)

    def __getitem__(self, index):
        ''':return: the access information for the specified index.
        :rtype: py:class:`psyclone.core.access_info.AccessInfo`

        :raises IndexError: If there is no access with the specified index.
        '''
        return self._accesses[index]

    @property
    def all_accesses(self):
        ''':returns: a list with all AccessInfo data for this variable.
        :rtype: List of :py:class:`psyclone.core.access_info.AccessInfo`
        '''
        return self._accesses

    def add_access_with_location(self, access_type, location, node,
                                 indices_groups=None):
        '''Adds access information to this variable.

        :param access_type: the type of access (READ, WRITE, ....)
        :type access_type: \
            :py:class:`psyclone.core.access_type.AccessType`
        :param location: location information
        :type location: int
        :param indicies_groups: indices used in the access (None if the \
            variable is not an array). Defaults to None
        :type indices_groups: list of :py:class:`psyclone.psyir.nodes.Node`
        :param node: Node in PSyIR in which the access happens.
        :type node: :py:class:`psyclone.psyir.nodes.Node`
        '''
        self._accesses.append(AccessInfo(access_type, location, node,
                                         indices_groups))

    def change_read_to_write(self):
        '''This function is only used when analysing an assignment statement.
        The LHS has first all variables identified, which will be READ.
        This function is then called to change the assigned-to variable
        on the LHS to from READ to WRITE. Since the LHS is stored in a separate
        SingleVariableAccessInfo class, it is guaranteed that there is only
        one entry for the variable.
        '''
        if len(self._accesses) != 1:
            raise InternalError("Variable '{0}' had {1} accesses listed, "
                                "not one in change_read_to_write.".
                                format(self._signature,
                                       len(self._accesses)))

        if self._accesses[0].access_type != AccessType.READ:
            raise InternalError("Trying to change variable '{0}' to 'WRITE' "
                                "which does not have 'READ' access."
                                .format(self._signature))

        self._accesses[0].change_read_to_write()

    def is_array(self, index_variable=None):
        '''Checks if the variable is used as an array, i.e. if it has
        an index expression. If the optional `index_variable` is specified,
        this variable must be used in (at least one) index access in order
        for this variable to be considered as an array.

        :returns: true if there is at least one access to this variable \
            that uses an index.
        :rtype: bool

        '''
        is_array = any(access_info.is_array() for
                       access_info in self._accesses)

        # If there is no access information using an index, or there is no
        # index variable specified, return the current result:
        if not is_array or index_variable is None:
            return is_array

        # Now test if the loop variable is used when accessing this array:
        for access_info in self._accesses:
            indices_list = access_info.indices_groups
            for index_group in indices_list:
                for index_expression in index_group:
                    accesses = VariablesAccessInfo()
                    index_expression.reference_accesses(accesses)
                    if Signature(index_variable) in accesses:
                        return True

        # The index variable is not used in any index in any access:
        return False


# =============================================================================
class VariablesAccessInfo(dict):
    '''This class stores all `SingleVariableAccessInfo` instances for all
    variables in the corresponding code section. It maintains 'location'
    information, which is an integer number that is increased for each new
    statement. It can be used to easily determine if one access is before
    another.

    :param nodes: optional, a single PSyIR node or list of nodes from \
                  which to initialise this object.
    :type nodes: None, :py:class:`psyclone.psyir.nodes.Node` or a list of \
                 :py:class:`psyclone.psyir.nodes.Node`

    '''
    def __init__(self, nodes=None):
        # This dictionary stores the mapping of signatures to the
        # corresponding SingleVariableAccessInfo instance.
        dict.__init__(self)

        # Stores the current location information
        self._location = 0
        if nodes:
            # Import here to avoid circular dependency
            # pylint: disable=import-outside-toplevel
            from psyclone.psyir.nodes import Node
            if isinstance(nodes, list):
                for node in nodes:
                    if not isinstance(node, Node):
                        raise InternalError("Error in VariablesAccessInfo. "
                                            "One element in the node list is "
                                            "not a Node, but of type {0}"
                                            .format(type(node)))

                    node.reference_accesses(self)
            elif isinstance(nodes, Node):
                nodes.reference_accesses(self)
            else:
                arg_type = str(type(nodes))
                raise InternalError("Error in VariablesAccessInfo. "
                                    "Argument must be a single Node in a "
                                    "schedule or a list of Nodes in a "
                                    "schedule but have been passed an "
                                    "object of type: {0}".
                                    format(arg_type))

    def __str__(self):
        '''Gives a shortened visual representation of all variables
        and their access mode. The output is one of: READ, WRITE, READ+WRITE,
        or READWRITE for each variable accessed.
        READ+WRITE is used if the statement (or set of statements)
        contain individual read and write accesses, e.g. 'a=a+1'. In this
        case two accesses to `a` will be recorded, but the summary displayed
        using this function will be 'READ+WRITE'. Same applies if this object
        stores variable access information about more than one statement, e.g.
        'a=b; b=1'. There would be two different accesses to 'b' with two
        different locations, but the string representation would show this as
        READ+WRITE. If a variable is is passed to a kernel for which no
        individual variable information is available, and the metadata for
        this kernel indicates a READWRITE access, this is marked as READWRITE
        in the string output.'''

        all_signatures = self.all_signatures
        output_list = []
        for signature in all_signatures:
            mode = ""
            if self.has_read_write(signature):
                mode = "READWRITE"
            else:
                if self.is_read(signature):
                    if self.is_written(signature):
                        mode = "READ+WRITE"
                    else:
                        mode = "READ"
                elif self.is_written(signature):
                    mode = "WRITE"
            output_list.append("{0}: {1}".format(str(signature), mode))
        return ", ".join(output_list)

    @property
    def location(self):
        '''Returns the current location of this instance, which is
        the location at which the next accesses will be stored.
        See the Developers' Guide for more information.

        :returns: the current location of this object.
        :rtype: int'''
        return self._location

    def next_location(self):
        '''Increases the location number.'''
        self._location = self._location + 1

    def add_access(self, signature, access_type, node, indices_list=None):
        '''Adds access information for the variable with the given signature.

        :param signature: the signature of the variable.
        :type signature: :py:class:`psyclone.core.Signature`
        :param access_type: the type of access (READ, WRITE, ...)
        :type access_type: :py:class:`psyclone.core.access_type.AccessType`
        :param node: Node in PSyIR in which the access happens.
        :type node: :py:class:`psyclone.psyir.nodes.Node` instance
        :param indices_list: list of list of indices used in the access, one \
            list for each component. None if the variable is not an array. \
            Defaults to None, which is then converted to [[]].
        :type indices_list: list of list of \
            :py:class:`psyclone.psyir.nodes.Node`

        '''
        if not isinstance(signature, Signature):
            raise InternalError("Got '{0}' of type '{1}' but expected it to "
                                "be of type psyclone.core.Signature."
                                .format(signature, type(signature).__name__))

        if indices_list is None:
            indices_list = [[]]

        if signature in self:
            self[signature].add_access_with_location(access_type,
                                                     self._location, node,
                                                     indices_list)
        else:
            var_info = SingleVariableAccessInfo(signature)
            var_info.add_access_with_location(access_type, self._location,
                                              node, indices_list)
            self[signature] = var_info

    @property
    def all_signatures(self):
        ''':returns: all signatures contained in this instance, sorted (in \
                     order to make test results reproducible).
        :rtype: list of :py:class:`psyclone.core.signature`
        '''
        list_of_vars = list(self.keys())
        list_of_vars.sort()
        return list_of_vars

    def merge(self, other_access_info):
        '''Merges data from a VariablesAccessInfo instance to the
        information in this instance.

        :param other_access_info: the other VariablesAccessInfo instance.
        :type other_access_info: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`
        '''

        # For each variable add all accesses. After merging the new data,
        # we need to increase the location so that all further added data
        # will have a location number that is larger.
        max_new_location = 0
        for signature in other_access_info.all_signatures:
            var_info = other_access_info[signature]
            for access_info in var_info.all_accesses:
                # Keep track of how much we need to update the next location
                # in this object:
                if access_info.location > max_new_location:
                    max_new_location = access_info.location
                new_location = access_info.location + self._location
                if signature in self:
                    var_info = self[signature]
                else:
                    var_info = SingleVariableAccessInfo(signature)
                    self[signature] = var_info

                var_info.add_access_with_location(access_info.access_type,
                                                  new_location,
                                                  access_info.node,
                                                  access_info.indices_groups)
        # Increase the current location of this instance by the amount of
        # locations just merged in
        self._location = self._location + max_new_location

    def is_written(self, signature):
        '''Checks if the specified variable signature is at least
        written once.

        :param signature: signature of the variable.
        :type signature: :py:class:`psyclone.core.Signature`

        :returns: True if the specified variable is written (at least \
            once).
        :rtype: bool

        :raises: KeyError if the signature name cannot be found.

        '''
        var_access_info = self[signature]
        return var_access_info.is_written()

    def is_read(self, signature):
        '''Checks if the specified variable signature is at least read once.

        :param signature: signature of the variable
        :type signature: :py:class:`psyclone.core.Signature`

        :returns: True if the specified variable name is read (at least \
            once).
        :rtype: bool

        :raises: KeyError if the signature cannot be found.'''

        var_access_info = self[signature]
        return var_access_info.is_read()

    def has_read_write(self, signature):
        '''Checks if the specified variable signature has at least one
        READWRITE access (which is typically only used in a function call).

        :param signature: signature of the variable
        :type signature: :py:class:`psyclone.core.Signature`

        :returns: True if the specified variable name has (at least one) \
            READWRITE access.
        :rtype: bool

        :raises: KeyError if the signature cannot be found.'''

        var_access_info = self[signature]
        return var_access_info.has_read_write()


# ---------- Documentation utils -------------------------------------------- #
# The list of module members that we wish AutoAPI to generate
# documentation for. (See https://psyclone-ref.readthedocs.io)
__all__ = ["AccessInfo",
           "SingleVariableAccessInfo",
           "VariablesAccessInfo"]
