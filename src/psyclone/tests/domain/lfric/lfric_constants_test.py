# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021, Science and Technology Facilities Council.
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
# Author: R. W. Ford, STFC Daresbury Lab

'''This module tests the contents of the lfric_constants.py file.'''

from psyclone.domain.lfric import LFRicConstants


def test_quadrature_type_map():
    '''Check that QUADRATURE_TYPE_MAP contains the expected structure.'''

    quadrature_types = [
        "gh_quadrature_xyoz", "gh_quadrature_face", "gh_quadrature_edge"]
    quadrature_properties = [
        "module", "type", "proxy_type", "intrinsic", "kind"]

    assert len(LFRicConstants.QUADRATURE_TYPE_MAP) == len(quadrature_types)
    for quadrature_type in quadrature_types:
        assert quadrature_type in LFRicConstants.QUADRATURE_TYPE_MAP
        info = LFRicConstants.QUADRATURE_TYPE_MAP[quadrature_type]
        assert len(info) == len(quadrature_properties)
        for item in info:
            assert item in quadrature_properties


def test_data_type_map():
    '''Check that DATA_TYPE_MAP contains the expected structure.'''

    data_types = [
        "reduction", "field", "r_solver_field", "integer_field", "operator",
        "columnwise_operator", "r_solver_operator",
        "r_solver_columnwise_operator"]
    data_type_properties = [
        "module", "type", "proxy_type", "intrinsic", "kind"]

    assert len(LFRicConstants.DATA_TYPE_MAP) == len(data_types)
    for data_type in data_types:
        assert data_type in LFRicConstants.DATA_TYPE_MAP
        info = LFRicConstants.DATA_TYPE_MAP[data_type]
        assert len(info) == len(data_type_properties)
        for item in info:
            assert item in data_type_properties
