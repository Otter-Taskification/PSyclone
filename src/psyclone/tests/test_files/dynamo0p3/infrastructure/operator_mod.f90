! -----------------------------------------------------------------------------
! BSD 3-Clause License
!
! Copyright (c) 2017, Science and Technology Facilities Council
! However, it has been created with the help of the GungHo Consortium,
! whose members are identified at https://puma.nerc.ac.uk/trac/GungHo/wiki
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
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
! "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
! LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
! FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
! COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
! INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
! BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
! LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
! LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
! ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
! -----------------------------------------------------------------------------
! Author R. Ford and A. R. Porter, STFC Daresbury Lab
! Modified I. Kavcic Met Office

module operator_mod
  use constants_mod,            only : r_def, i_def
  use function_space_mod,       only : function_space_type
  use mesh_mod

  ! Base operator type on which operator type and columnwise assembled
  ! operator type are built (LMA and CMA operators)
  type, public :: base_operator_type

     integer(i_def) :: a
     type( function_space_type ), pointer :: fs_from => null( )
     type( function_space_type ), pointer :: fs_to => null( )

   contains

     procedure, public :: get_mesh

  end type base_operator_type

  ! Locally (element-wise) assembled operator type
  type, extends(base_operator_type) :: operator_type

     real(kind=r_def), allocatable :: local_stencil( :, :, : )
     integer(i_def) :: ncell_3d

   contains

     procedure, public :: get_proxy => get_proxy_op

  end type operator_type

  ! Locally (element-wise) assembled operator proxy type
  type, extends(base_operator_type) :: operator_proxy_type

     real(kind=r_def), allocatable :: local_stencil( :, :, : )
     integer(i_def) :: ncell_3d

  end type operator_proxy_type

  ! Columnwise assembled operator type
  type, extends(base_operator_type) :: columnwise_operator_type

    private

    integer(i_def) :: alpha
    integer(i_def) :: beta
    integer(i_def) :: gamma_m, gamma_p
    integer(i_def) :: bandwidth
    integer(i_def) :: nrow
    integer(i_def) :: ncol
    integer(i_def) :: ndof_face_to, ndof_face_from
    integer(i_def) :: ndof_interior_to, ndof_interior_from 
    integer(i_def) :: ndof_cell_to, ndof_cell_from
    real(kind=r_def), allocatable :: columnwise_matrix( :, :, : )
    integer(i_def) :: ncell_2d 
    integer(kind=i_def), allocatable :: column_dofmap_to( :, : )
    integer(kind=i_def), allocatable :: column_dofmap_from( :, : )
    integer(kind=i_def), allocatable :: column_banded_dofmap_to( :, : )
    integer(kind=i_def), allocatable :: column_banded_dofmap_from( :, : )
    integer(kind=i_def), allocatable :: indirection_dofmap_to( : )
    integer(kind=i_def), allocatable :: indirection_dofmap_from( : )

  contains

    procedure, public :: get_proxy => get_proxy_columnwise

  end type columnwise_operator_type

  ! Columnwise assembled operator proxy type
  type, extends( base_operator_type ) :: columnwise_operator_proxy_type 
    private
    integer(i_def), public :: alpha
    integer(i_def), public :: beta
    integer(i_def), public :: gamma_m, gamma_p
    integer(i_def), public :: bandwidth
    integer(i_def), public :: nrow
    integer(i_def), public :: ncol
    real(kind=r_def), public, pointer :: columnwise_matrix( :, :, : )
    integer(i_def), public :: ncell_2d
    integer(kind=i_def), public, pointer :: column_banded_dofmap_to( :, : )
    integer(kind=i_def), public, pointer :: column_banded_dofmap_from( :, : ) 
    integer(kind=i_def), public, pointer :: indirection_dofmap_to( : ) 
    integer(kind=i_def), public, pointer :: indirection_dofmap_from( : )

 end type columnwise_operator_proxy_type

contains

  ! Function to create a proxy with access to the data in the
  ! operator_type
  type( operator_proxy_type ) function get_proxy_op(self)

    implicit none

    class(operator_type), target, intent(in)  :: self

    get_proxy_op % fs_from => null()
    get_proxy_op % fs_to   => null()

  end function get_proxy_op

  ! Function to create a proxy with access to the data in the
  ! columnwise_operator_type
  type( columnwise_operator_proxy_type ) function get_proxy_columnwise(self)

    implicit none

    class(columnwise_operator_type), target, intent(in)  :: self
    get_proxy_columnwise % fs_from                 => self % fs_from
    get_proxy_columnwise % fs_to                   => self % fs_to
    get_proxy_columnwise % alpha                   =  self % alpha
    get_proxy_columnwise % beta                    =  self % beta
    get_proxy_columnwise % gamma_m                 =  self % gamma_m
    get_proxy_columnwise % gamma_p                 =  self % gamma_p
    get_proxy_columnwise % bandwidth               =  self % bandwidth
    get_proxy_columnwise % nrow                    =  self % nrow
    get_proxy_columnwise % ncol                    =  self % ncol
    get_proxy_columnwise % columnwise_matrix       => self % columnwise_matrix
    get_proxy_columnwise % ncell_2d                =  self % ncell_2d
    get_proxy_columnwise % column_banded_dofmap_to => self % column_banded_dofmap_to
    get_proxy_columnwise % column_banded_dofmap_from => self % column_banded_dofmap_from
    get_proxy_columnwise % indirection_dofmap_to   => self % indirection_dofmap_to
    get_proxy_columnwise % indirection_dofmap_from => self % indirection_dofmap_from

  end function get_proxy_columnwise
  
  ! Function to get the mesh the operator lives on
  function get_mesh(self) result(mesh)

    implicit none

    class (base_operator_type), intent(in) :: self
    type(mesh_type), pointer :: mesh

    mesh => null()

  end function get_mesh

end module operator_mod
