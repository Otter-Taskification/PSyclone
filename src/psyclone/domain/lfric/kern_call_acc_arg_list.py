# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2017-2020, Science and Technology Facilities Council.
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
# Authors R. W. Ford, A. R. Porter and S. Siso, STFC Daresbury Lab
# Modified I. Kavcic, Met Office
# Modified J. Henrichs, Bureau of Meteorology

'''This module implements a class that manages the argument for a kernel
call using OpenACC. It especially adds all implicitly required parameters.
'''

from psyclone.core.access_type import AccessType
from psyclone.domain.lfric import KernCallArgList


class KernCallAccArgList(KernCallArgList):
    '''Kernel call arguments that need to be declared by OpenACC
    directives. KernCallArgList only needs to be specialised
    where modified, or additional, arguments are required.
    Scalars are apparently not required but it is valid in
    OpenACC to include them and requires less specialisation
    to keep them in.

    '''
    def field_vector(self, argvect, var_accesses=None):
        '''Add the field vector associated with the argument 'argvect' to the
        argument list. OpenACC requires the field and the
        dereferenced data to be specified. If supplied it also stores
        this access in var_accesses.

        :param argvect: the field vector to add.
        :type argvect: :py:class:`psyclone.dynamo0p3.DynKernelArgument`
        :param var_accesses: optional VariablesAccessInfo instance to store \
            the information about variable accesses.
        :type var_accesses: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`

        '''
        # First provide the derived class
        for idx in range(1, argvect.vector_size+1):
            self.append(argvect.proxy_name + "(" + str(idx) + ")")
        # Then provide the actual fields that are in the derived class
        super(KernCallAccArgList, self).field_vector(argvect, var_accesses)

    def field(self, arg, var_accesses=None):
        '''Add the field array associated with the argument 'arg' to the
        argument list. OpenACC requires the field and the
        dereferenced data to be specified. If supplied it also
        stores this access in var_accesses.

        :param arg: the field to be added.
        :type arg: :py:class:`psyclone.dynamo0p3.DynKernelArgument`
        :param var_accesses: optional VariablesAccessInfo instance to store \
            the information about variable accesses.
        :type var_accesses: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`

        '''
        text1 = arg.proxy_name
        self.append(text1)
        # This will add the field%data argument, and add the field
        # to the variable access list.
        super(KernCallAccArgList, self).field(arg, var_accesses)

    def stencil(self, arg, var_accesses=None):
        '''Add general stencil information associated with the argument 'arg'
        to the argument list. OpenACC requires the full dofmap to be
        specified. If supplied it also stores this access in var_accesses.

        :param arg: the meta-data description of the kernel \
            argument with which the stencil is associated.
        :type arg: :py:class:`psyclone.dynamo0p3.DynKernelArgument`
        :param var_accesses: optional VariablesAccessInfo instance to store \
            the information about variable accesses.
        :type var_accesses: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`

        '''
        from psyclone.dynamo0p3 import DynStencils
        var_name = DynStencils.dofmap_name(self._kern.root.symbol_table, arg)
        self.append(var_name)
        if var_accesses is not None:
            var_accesses.add_access(var_name, AccessType.READ,
                                    self._kern, [1])

    def operator(self, arg, var_accesses=None):
        '''Add the operator arguments to the argument list if
        they have not already been added. OpenACC requires the
        derived type and the dereferenced data to be
        specified. If supplied it also stores this access in
        var_accesses.

        :param arg: the meta-data description of the operator.
        :type arg: :py:class:`psyclone.dynamo0p3.DynKernelArgument`
        :param var_accesses: optional VariablesAccessInfo instance to store \
            the information about variable accesses.
        :type var_accesses: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`

        '''
        # In case of OpenACC we do not want to transfer the same
        # data to GPU twice.
        if arg.proxy_name_indexed not in self.arglist:
            self.append(arg.proxy_name_indexed)
            if var_accesses is not None:
                var_accesses.add_access(arg.proxy_name_indexed,
                                        AccessType.READ, self._kern)
            # This adds ncell_3d and local_stencil after the derived type:
            super(KernCallAccArgList, self).operator(arg, var_accesses)

    def fs_compulsory_field(self, function_space, var_accesses=None):
        '''Add compulsory arguments associated with this function space to
        the list. OpenACC requires the full function-space map
        to be specified. If supplied it also stores this access in
        var_accesses.

        :param function_space: the function space for which the compulsory \
            arguments are added.
        :type function_space: :py:class:`psyclone.domain.lfric.FunctionSpace`
        :param var_accesses: optional VariablesAccessInfo instance to store \
            the information about variable accesses.
        :type var_accesses: \
            :py:class:`psyclone.core.access_info.VariablesAccessInfo`

        '''
        undf_name = function_space.undf_name
        self.append(undf_name)
        # The base class only adds one dimension tothe list, while OpenACC
        # needs the whole field, so we cannot call the base class
        map_name = function_space.map_name
        self.append(map_name)
        if var_accesses is not None:
            var_accesses.add_access(undf_name, AccessType.READ,
                                    self._kern)
            var_accesses.add_access(map_name, AccessType.READ,
                                    self._kern)
