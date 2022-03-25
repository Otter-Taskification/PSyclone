# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2020-2022, Science and Technology Facilities Council.
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
# Author: A. R. Porter, STFC Daresbury Lab
# Modified by: R. W. Ford, STFC Daresbury Lab
# Modified by J. Henrichs, Bureau of Meteorology
# -----------------------------------------------------------------------------

''' This module contains the implementation of the Member node.'''

from __future__ import absolute_import

from psyclone.core import Signature
from psyclone.psyir.nodes.node import Node


class Member(Node):
    '''
    Node representing a membership expression of a structure.
    As such it is a leaf in the PSyIR tree.

    :param str member_name: the name of the member of the structure that is \
                            being referenced.
    :param parent: the parent of this node in the PSyIR tree.
    :type parent: :py:class:`psyclone.psyir.nodes.StructureReference` or \
                  :py:class:`psyclone.psyir.nodes.Member`

    :raises TypeError: if the supplied parent is of the wrong type.

    '''
    # Textual description of the node.
    _children_valid_format = "<LeafNode>"
    _text_name = "Member"
    _colour = "yellow"

    def __init__(self, member_name, parent=None):
        # Avoid circular dependency
        # pylint: disable=import-outside-toplevel
        from psyclone.psyir.nodes.structure_reference import StructureReference
        from psyclone.psyir.nodes.structure_member import StructureMember

        # Since this node represents a membership expression of a structure,
        # its parent (if supplied) *must* subclass StructureReference or
        # StructureMember.
        if (parent and
                not isinstance(parent, (StructureReference, StructureMember))):
            raise TypeError(
                f"The parent of a {type(self).__name__} must be either a "
                f"(ArrayOf)Structure(s)Reference or (ArrayOf)Structure(s)"
                f"Member but found '{type(parent).__name__}'.")

        super(Member, self).__init__(parent=parent)
        # Store the name of the component that this member represents
        self._component_name = member_name

    @property
    def name(self):
        '''
        :returns: the name of this member.
        :rtype: str
        '''
        return self._component_name

    def node_str(self, colour=True):
        ''' Create a text description of this node in the schedule, optionally
        including control codes for colour.

        :param bool colour: whether or not to include colour control codes.

        :return: text description of this node.
        :rtype: str
        '''
        return self.coloured_name(colour) + "[name:'" + self.name + "']"

    def __str__(self):
        return self.node_str(False)

    @property
    def is_array(self):
        ''':returns: if this member is an array.
        :rtype: bool

        '''
        # pylint: disable=no-self-use
        return False

    def get_signature_and_indices(self):
        ''':returns: the Signature of this member access, and a list \
        of list of the indices used for each component, which is empty \
        in this case since it is not an array access.
        :rtype: tuple(:py:class:`psyclone.core.Signature`, list of \
            lists of indices)
        '''
        return (Signature(self.name), [[]])

    def rank_of_subsection(self):
        '''Check that the supplied candidate array reference uses supported
        array notation syntax and return the rank of the sub-section
        of the array that uses array notation. e.g. for a reference
        "a(:, 2, :)" the rank of the sub-section is 2.

        :param node: the reference to check.
        :type node: :py:class:`psyclone.psyir.nodes.ArrayReference` or \
            :py:class:`psyclone.psyir.nodes.ArrayMember` or \
            :py:class:`psyclone.psyir.nodes.StructureReference`

        :returns: rank of the sub-section of the array.
        :rtype: int

        :raises InternalError: if no ArrayMixin node with at least one \
                               Range in its indices is found.
        :raises InternalError: if two or more part references in a \
                               structure reference contain ranges.
        :raises NotImplementedError: if the supplied node is not of a \
                                     supported type.
        :raises NotImplementedError: if any ranges are encountered that are \
                                     not for the full extent of the dimension.
        '''
        from psyclone.psyir.nodes.array_mixin import ArrayMixin
        ranks = 0
        if isinstance(self, ArrayMixin):
            ranks += self.rank_of_subsection
        if hasattr(self, "member"):
            ranks += self.member.rank_of_subsection()
        return ranks


# For Sphinx AutoAPI documentation generation
__all__ = ['Member']
