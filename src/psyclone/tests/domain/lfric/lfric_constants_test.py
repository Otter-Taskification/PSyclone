# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2022, Science and Technology Facilities Council.
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

'''
Module containing tests for the LFRic (Dynamo0.3) constants class.
'''

import pytest
from psyclone.domain.lfric import LFRicConstants
from psyclone.errors import InternalError


def test_specific_function_space():
    ''' Check that the lookup of a specific function space for a valid
    wildcard name works as expected.

    '''
    name = LFRicConstants().specific_function_space("ANY_W2")
    assert name == "w2"
    name = LFRicConstants().specific_function_space("ANY_space_3")
    assert name == "w0"
    name = LFRicConstants().specific_function_space(
        "ANY_disCONTINUOUS_space_3")
    assert name == "w3"
    name = LFRicConstants().specific_function_space("wtheta")
    assert name == "wtheta"


def test_specific_function_space_invalid(monkeypatch):
    ''' Check that the specific_function_space() method rejects an invalid
    function-space name. '''
    with pytest.raises(ValueError) as err:
        LFRicConstants().specific_function_space("wrong")
    assert ("'wrong' is not a recognised LFRic function space (one of"
            in str(err.value))


def test_specific_function_space_internal_error(monkeypatch):
    ''' Check that the lookup of a specific function space raises the expected
    internal error if an unhandled case is found.
    '''
    const = LFRicConstants()
    # We have to monkeypatch the list of valid FS names to get to the bit
    # of code we want to test.
    monkeypatch.setattr(LFRicConstants,
                        "VALID_FUNCTION_SPACE_NAMES", ["any_wrong"])
    with pytest.raises(InternalError) as err:
        const.specific_function_space("any_wrong")
    assert ("Error mapping from meta-data function space to actual space: "
            "cannot handle 'any_wrong'" in str(err.value))
