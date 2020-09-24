!-----------------------------------------------------------------------------
! (C) Crown copyright 2019 Met Office. All rights reserved.
! The file LICENCE, distributed with this code, contains details of the terms
! under which the code may be used.
!-----------------------------------------------------------------------------
! LICENCE is available from the Met Office Science Repository Service:
! https://code.metoffice.gov.uk/trac/lfric/browser/LFRic/trunk/LICENCE
! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Modifications copyright (c) 2020, Science and Technology Facilities
! Council
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! * Redistributions of source code must retain the above copyright notice, this
!   list of conditions and the following disclaimer.
!
! * Redistributions in binary form must reproduce the above copyright notice,
!   this list of conditions and the following disclaimer in the documentation
!   and/or other materials provided with the distribution.
!
! * Neither the name of the copyright holder nor the names of its
!   contributors may be used to endorse or promote products derived from
!   this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
! DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
! FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
! DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
! SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
! OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
! OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
!
!> @brief A module containing the abstract type that is the parent to all
!>        child field types.
!>
!> @details All field types (and pointer field types) are part of the same
!>          family. This module contains the pure abstract type that will be
!>          the parent to all of them

module pure_abstract_field_mod
  use linked_list_data_mod,        only: linked_list_data_type
  implicit none

  private

  !> Pure abstract field type that is the parent of any field type or field
  !> pointer type in the field object hierarchy
  type, extends(linked_list_data_type), public, abstract :: &
                                                 pure_abstract_field_type
  contains
  end type pure_abstract_field_type

contains

end module pure_abstract_field_mod
