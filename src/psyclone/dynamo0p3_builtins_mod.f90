!-------------------------------------------------------------------------------
! (c) The copyright relating to this work is owned jointly by the Crown,
! Met Office and NERC 2015.
! However, it has been created with the help of the GungHo Consortium,
! whose members are identified at https://puma.nerc.ac.uk/trac/GungHo/wiki
!-------------------------------------------------------------------------------
! Modified I. Kavcic Met Office
!
!>@brief Meta-data for the Dynamo 0.3 built-in operations.
!>@details This meta-data is purely to provide psyclone with a
!!         specification of each operation. This specification is used
!!         for correctness checking as well as to enable optimisations
!!         of invokes containing calls to built-in operations.
!!         The actual implementation of these built-ins is
!!         generated by psyclone (hence the empty ..._code routines in
!!         this file).
module dynamo0p3_builtins_mod
!---------------------------------------------------------------------!
!=============== Adding (scaled) fields ==============================!
!---------------------------------------------------------------------!
  !> field3 = field1 + field2
  type, public, extends(kernel_type) :: X_plus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_plus_Y_code
  end type X_plus_Y

  !> field1 = field1 + field2
  type, public, extends(kernel_type) :: inc_X_plus_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_plus_Y_code
  end type inc_X_plus_Y

  !> field3 = a*field1 + field2
  type, public, extends(kernel_type) :: aX_plus_Y
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_plus_Y_code
  end type aX_plus_Y

  !> field1 = a*field1 + field2
  type, public, extends(kernel_type) :: inc_aX_plus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_plus_Y_code
  end type inc_aX_plus_Y

  !> field1 = field1 + b*field2
  type, public, extends(kernel_type) :: inc_X_plus_bY
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_plus_bY_code
  end type inc_X_plus_bY

  !> field3 = a*field1 + b*field2
  type, public, extends(kernel_type) :: aX_plus_bY
     private
     type(arg_type) :: meta_args(5) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_plus_bY_code
  end type aX_plus_bY

  !> field1 = a*field1 + b*field2
  type, public, extends(kernel_type) :: inc_aX_plus_bY
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_plus_bY_code
  end type inc_aX_plus_bY
!---------------------------------------------------------------------!
!=============== Subtracting (scaled) fields =========================!
!---------------------------------------------------------------------!
  !> field3 = field1 - field2
  type, public, extends(kernel_type) :: X_minus_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_minus_Y_code
  end type X_minus_Y

  !> field3 = a*field1 - field2
  type, public, extends(kernel_type) :: aX_minus_Y
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: aX_minus_Y_code
  end type aX_minus_Y

  !> field3 = field1 - b*field2
  type, public, extends(kernel_type) :: X_minus_bY
     private
     type(arg_type) :: meta_args(4) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_minus_bY_code
  end type X_minus_bY

  !> field1 = field1 - b*field2
  type, public, extends(kernel_type) :: inc_X_minus_bY
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_minus_bY_code
  end type inc_X_minus_bY
!---------------------------------------------------------------------!
!=============== Multiplying (scaled) fields =========================!
!---------------------------------------------------------------------!
  !> field3(:) = field1(:) * field2(:)
  type, public, extends(kernel_type) :: X_times_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_times_Y_code
  end type X_times_Y

  !> field1 = field1 * field2
  type, public, extends(kernel_type) :: inc_X_times_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_times_Y_code
  end type inc_X_times_Y

  !> field1 = a*field1*field2
  type, public, extends(kernel_type) :: inc_aX_times_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_READ             ),                   &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_aX_times_Y_code
  end type inc_aX_times_Y
!---------------------------------------------------------------------!
!=============== Scaling fields ======================================!
!---------------------------------------------------------------------!
  !> field2 = a*field1
  type, public, extends(kernel_type) :: a_times_X
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              ),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: a_times_X_code
  end type a_times_X

  !> field1 = ascalar * field1
  type, public, extends(kernel_type) :: inc_a_times_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_READ            ),                    &
          arg_type(GH_FIELD, GH_INC, ANY_SPACE_1)                     &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_a_times_X_code
  end type inc_a_times_X
!---------------------------------------------------------------------!
!=============== Dividing (scaled) fields ============================!
!---------------------------------------------------------------------!
  !> field3 = field1 / field2
  type, public, extends(kernel_type) :: X_divideby_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_divideby_Y_code
  end type X_divideby_Y

  !> field1 = field1 / field2
  type, public, extends(kernel_type) :: inc_X_divideby_Y
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC,  ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_divideby_Y_code
  end type inc_X_divideby_Y
!---------------------------------------------------------------------!
!=============== Raising field to a scalar ===========================!
!---------------------------------------------------------------------!
  !> field1 =  field1 ** ascalar (real ascalar)
  type, public, extends(kernel_type) :: inc_X_powreal_a
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_INC, ANY_SPACE_1),                    &
          arg_type(GH_REAL,  GH_READ            )                     &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: inc_X_powreal_a_code
  end type inc_X_powreal_a
!---------------------------------------------------------------------!
!=============== Setting field elements to a value  ==================!
!---------------------------------------------------------------------!
  !> field1 = ascalar
  type, public, extends(kernel_type) :: setval_c
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_REAL,  GH_READ              )                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: setval_c_code
  end type setval_c

  !> field2 = field1
  type, public, extends(kernel_type) :: setval_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_FIELD, GH_WRITE, ANY_SPACE_1),                  &
          arg_type(GH_FIELD, GH_READ,  ANY_SPACE_1)                   &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: setval_X_code
  end type setval_X
!---------------------------------------------------------------------!
!=============== Inner product of fields =============================!
!---------------------------------------------------------------------!
  !> sum = sum + field1(i,j,..) * field2(i,j,...)
  type, public, extends(kernel_type) :: X_innerproduct_Y
     private
     type(arg_type) :: meta_args(3) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_innerproduct_Y_code
  end type X_innerproduct_Y

  !> sum = sum + field1(i,j,..) * field1(i,j,...)
  type, public, extends(kernel_type) :: X_innerproduct_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: X_innerproduct_X_code
  end type X_innerproduct_X
!---------------------------------------------------------------------!
!=============== Sum field elements ==================================!
!---------------------------------------------------------------------!
  !> scalar = SUM(field1(:,:,...))
  type, public, extends(kernel_type) :: sum_X
     private
     type(arg_type) :: meta_args(2) = (/                              &
          arg_type(GH_REAL,  GH_SUM              ),                   &
          arg_type(GH_FIELD, GH_READ, ANY_SPACE_1)                    &
          /)
     integer :: iterates_over = DOFS
   contains
     procedure, nopass :: sum_X_code
  end type sum_X

contains
  ! Adding (scaled) fields
  subroutine X_plus_Y_code()
  end subroutine X_plus_Y_code

  subroutine inc_X_plus_Y_code()
  end subroutine inc_X_plus_Y_code

  subroutine aX_plus_Y_code()
  end subroutine aX_plus_Y_code

  subroutine inc_aX_plus_Y_code()
  end subroutine inc_aX_plus_Y_code

  subroutine inc_X_plus_bY_code()
  end subroutine inc_X_plus_bY_code

  subroutine aX_plus_bY_code()
  end subroutine aX_plus_bY_code

  subroutine inc_aX_plus_bY_code()
  end subroutine inc_aX_plus_bY_code
  ! Subtracting (scaled) fields
  subroutine X_minus_Y_code()
  end subroutine X_minus_Y_code

  subroutine aX_minus_Y_code()
  end subroutine aX_minus_Y_code

  subroutine X_minus_bY_code()
  end subroutine X_minus_bY_code

  subroutine inc_X_minus_bY_code()
  end subroutine inc_X_minus_bY_code
  ! Multiplying (scaled) fields
  subroutine X_times_Y_code()
  end subroutine X_times_Y_code

  subroutine inc_X_times_Y_code()
  end subroutine inc_X_times_Y_code

  subroutine inc_aX_times_Y_code()
  end subroutine inc_aX_times_Y_code
  ! Multiplying fields by a scalar (scaling fields)
  subroutine a_times_X_code()
  end subroutine a_times_X_code

  subroutine inc_a_times_X_code()
  end subroutine inc_a_times_X_code
  ! Dividing (scaled) fields
  subroutine X_divideby_Y_code()
  end subroutine X_divideby_Y_code

  subroutine inc_X_divideby_Y_code()
  end subroutine inc_X_divideby_Y_code
  ! Raising field to a scalar
  subroutine inc_X_powreal_a_code()
  end subroutine inc_X_powreal_a_code
  ! Setting field elements to scalar or other field's values
  subroutine setval_c_code()
  end subroutine setval_c_code

  subroutine setval_X_code()
  end subroutine setval_X_code
  ! Inner product of fields
  subroutine X_innerproduct_Y_code()
  end subroutine X_innerproduct_Y_code

  subroutine X_innerproduct_X_code()
  end subroutine X_innerproduct_X_code
  ! Sum values of a field
  subroutine sum_X_code()
  end subroutine sum_X_code

end module dynamo0p3_builtins_mod
