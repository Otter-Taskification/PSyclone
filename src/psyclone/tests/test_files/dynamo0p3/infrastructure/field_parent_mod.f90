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
!> @details All concrete field types are part of the same family of fields. This
!>          module contains the abstract type that will be the parent to all
!>          of them

module field_parent_mod

  use constants_mod,               only: i_def, l_def, str_def, r_def
  use function_space_mod,          only: function_space_type
  use pure_abstract_field_mod,     only: pure_abstract_field_type
  use mesh_mod,                    only: mesh_type

  implicit none

  private

!______field_parent_type______________________________________________________

  !> Abstract field type that is the parent of any field type in the field
  !> object hierarchy
  type, extends(pure_abstract_field_type), public, abstract :: field_parent_type
    !> A pointer to the function space on which the field lives
    type( function_space_type ), pointer :: vspace => null()
    !> Flag that holds whether each depth of halo is clean or dirty (dirty=1)
    integer(kind=i_def), allocatable :: halo_dirty(:)
    !> Flag that determines whether the field should be advected.
    !! false by default.
    logical(kind=l_def) :: advected = .false.
    !> Name of the field. Note the name is immutable once defined via
    !! the initialiser.
    character(str_def) :: name = 'unset'
    !> Flag describes order of data. False=layer first, true=multi-data first
    logical :: ndata_first
  contains
    !> Initialise public pointers that belong to the field_parent_type.
    !> @param [inout] field_proxy The field proxy object being initialised.
    procedure, public :: field_parent_proxy_initialiser
    !> Returns the enumerated integer for the functions_space on which
    !! the field lives
    !> @return fs The enumerated integer for the functions_space
    procedure, public :: which_function_space
    !> Returns a pointer to the function space on which the field lives
    !> @return vspace A pointer to the function space on which the field lives.
    procedure, public :: get_function_space
    !> Returns the mesh used by this field
    !> @return mesh The mesh object associated with the field
    procedure, public :: get_mesh
    !> Return the id of the mesh used by this field
    !> @return mesh_id The id of the mesh object associated with the field
    procedure, public :: get_mesh_id
    !> Returns the order of the FEM elements
    !> @return elem Element order of this field
    procedure, public :: get_element_order
    !> Returns the name of the field
    !> @return field name
    procedure, public :: get_name
    !> Returns whether the field is advected
    procedure, public :: is_advected
  end type field_parent_type

!______field_parent_proxy_type________________________________________________

  !> Abstract field proxy type that is the parent of any field proxy
  type, public, abstract :: field_parent_proxy_type
    !> An unused allocatable integer that prevents an internal compiler error
    !> with the Gnu Fortran compiler. Adding an allocatable forces the compiler
    !> to accept that the object has a finaliser. It gets confused without it.
    !> This is a workaround for GCC bug id 61767 - when this bug is fixed, the
    !> integer can be removed.
    integer(kind=i_def), allocatable :: dummy_for_gnu
    !> A pointer to the function space on which the field lives
    type( function_space_type ), pointer, public :: vspace => null()
    !> A pointer to the array that holds halo dirtiness
    integer(kind=i_def), public, pointer :: halo_dirty(:) => null()
    !> Flag describes order of data. False=layer first, true=multi-data first
    logical, public, pointer :: ndata_first
  contains
    !> Return the maximum halo depth on this field
    !> @return The maximum halo depth on this field
    procedure, public :: max_halo_depth
    !> Returns whether the halos at the given depth are dirty or clean
    !! @param[in] depth The depth at which to check the halos
    !! @return True if the halos are dirty or false if they are clean
    procedure, public :: is_dirty
    !> Flags all halos as being dirty
    procedure, public :: set_dirty
    !> Flags all the halos up the given depth as clean
    !! @param[in] depth The depth up to which to set the halo to clean
    procedure, public :: set_clean
    !> Returns if the ordering of data is multi-data quickest
    !> @return True if the data is ordered multi-data quickest
    procedure, public :: is_ndata_first
  end type field_parent_proxy_type

!______end of type declarations_______________________________________________

contains

!______field_parent_type procedures___________________________________________

  ! Initialise public pointers that belong to the field_parent_type.
  subroutine field_parent_proxy_initialiser(self, field_proxy)

   implicit none

   class(field_parent_type), target, intent(in)  :: self
   class(field_parent_proxy_type), intent(inout) :: field_proxy

   field_proxy%vspace       => self%vspace
   field_proxy%halo_dirty   => self%halo_dirty
   field_proxy%ndata_first  => self%ndata_first

  end subroutine field_parent_proxy_initialiser

  ! Function to return the integer id of the function space from the field
  function which_function_space(self) result(fs)
    implicit none
    class(field_parent_type), intent(in) :: self
    integer(i_def) :: fs

    fs = 0
    return
  end function which_function_space

  ! Function to get pointer to function space from the field.
  function get_function_space(self) result(vspace)
    implicit none

    class (field_parent_type), target :: self
    type(function_space_type), pointer :: vspace

    vspace => null()

    return
  end function get_function_space

  ! Function to get mesh information from the field.
  function get_mesh(self) result(mesh)

    implicit none

    class(field_parent_type), intent(in) :: self
    type(mesh_type), pointer :: mesh

    mesh => null()

  end function get_mesh

  ! Function to get mesh id from the field.
  function get_mesh_id(self) result(mesh_id)
    implicit none

    class (field_parent_type) :: self
    integer(i_def) :: mesh_id

    mesh_id = 0

    return
  end function get_mesh_id

  ! Function to get element order from the field.
  function get_element_order(self) result(elem)
    implicit none

    class (field_parent_type) :: self
    integer(i_def) :: elem

    elem = 0

    return
  end function get_element_order

  !> Returns the name of the field
  function get_name(self) result(name)

    implicit none

    class(field_parent_type), intent(in) :: self
    character(str_def) :: name

    name = 'unset'

  end function get_name

  !> Returns whether the field is advected
  !>
  !> @return field advected
  function is_advected(self) result(flag)

    implicit none

    class(field_parent_type), intent(in) :: self
    logical :: flag

    flag = .false.

  end function is_advected

!______field_parent_proxy_type procedures_____________________________________

  ! Returns the max halo depth of the field.
  function max_halo_depth(self) result(max_depth)

    implicit none

    class(field_parent_proxy_type), intent(in) :: self
    integer(i_def) :: max_depth

    max_depth = 0

  end function max_halo_depth

  ! Returns true if a halo depth is dirty
  function is_dirty(self, depth) result(dirtiness)

    implicit none

    class(field_parent_proxy_type), intent(in) :: self
    integer(i_def), intent(in) :: depth
    logical(l_def) :: dirtiness

    dirtiness = .false.

  end function is_dirty

  ! Sets a halo depth to be flagged as dirty
  subroutine set_dirty( self )

    implicit none

    class(field_parent_proxy_type), intent(inout) :: self

    self%halo_dirty(:) = 1

  end subroutine set_dirty

  ! Sets the halos up to depth to be flagged as clean
  subroutine set_clean(self, depth)

    implicit none

    class(field_parent_proxy_type), intent(inout) :: self
    integer(i_def), intent(in) :: depth

    self%halo_dirty(1:depth) = 0

  end subroutine set_clean

  !> Returns whether the field data is ordered multi-data first
  !>
  !> @return Flag for if field data order is multi-data first
  function is_ndata_first(self) result(flag)

    implicit none

    class(field_parent_proxy_type), intent(in) :: self
    logical(l_def) :: flag

    flag = .false.

  end function is_ndata_first

end module field_parent_mod
