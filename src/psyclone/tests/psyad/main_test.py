# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021-2022, Science and Technology Facilities Council.
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
# Authors: R. W. Ford and A. R. Porter, STFC Daresbury Lab

'''A module to perform pytest tests on the code in the main.py file
within the psyad directory.

'''
from __future__ import print_function, absolute_import
import logging
import six
import pytest
from psyclone.psyad import main


TEST_PROG = (
    "program test\n"
    "real :: a\n"
    "a = 0.0\n"
    "end program test\n")

TEST_MOD = (
    "module my_mod\n"
    "  contains\n"
    "  subroutine kern(field)\n"
    "    real, intent(inout) :: field\n"
    "    field = 0.0\n"
    "  end subroutine kern\n"
    "end module my_mod\n"
)

EXPECTED_HARNESS_CODE = ('''program adj_test
  use my_mod, only : kern
  use my_mod_adj, only : kern_adj
  integer, parameter :: array_extent = 20
  real, parameter :: overall_tolerance = 1500.0
  real :: inner1
  real :: inner2
  real :: field
  real :: field_input
  real :: MachineTol
  real :: relative_diff

  ! Initialise the kernel arguments and keep copies of them
  CALL random_number(field)
  field_input = field
  ! Call the tangent-linear kernel
  call kern(field)
  ! Compute the inner product of the results of the tangent-linear kernel
  inner1 = 0.0
  inner1 = inner1 + field * field
  ! Call the adjoint of the kernel
  call kern_adj(field)
  ! Compute inner product of results of adjoint kernel with the original \
inputs to the tangent-linear kernel
  inner2 = 0.0
  inner2 = inner2 + field * field_input
  ! Test the inner-product values for equality, allowing for the precision \
of the active variables
  MachineTol = SPACING(MAX(ABS(inner1), ABS(inner2)))
  relative_diff = ABS(inner1 - inner2) / MachineTol
  if (relative_diff < overall_tolerance) then
    WRITE(*, *) 'Test of adjoint of ''kern'' PASSED: ', inner1, inner2, \
relative_diff
  else
    WRITE(*, *) 'Test of adjoint of ''kern'' FAILED: ', inner1, inner2, \
relative_diff
  end if

end program adj_test''')

# main function


# -h description
def test_main_h_option(capsys):
    '''Test that the -h script option works as expected'''

    with pytest.raises(SystemExit) as info:
        main(["-h", "filename"])
    assert str(info.value) == "0"
    output, error = capsys.readouterr()
    assert error == ""
    # The name of the executable is replaced with either pytest or -c
    # when using pytest, therefore we split this test into sections.
    assert "usage: " in output
    expected2 = (
        "[-h] [-oad OAD] [-v] [-t] [-otest TEST_FILENAME] "
        "-a ACTIVE [ACTIVE ...] -- filename\n\n"
        "Run the PSyclone adjoint code generator on an LFRic tangent-linear "
        "kernel file\n\n"
        "positional arguments:\n"
        "  filename              LFRic tangent-linear kernel source\n\n")
    assert expected2 in output
    expected3 = (
        "  -h, --help            show this help message and exit\n"
        "  -a ACTIVE [ACTIVE ...], --active ACTIVE [ACTIVE ...]\n"
        "                        names of active variables\n"
        "  -v, --verbose         increase the verbosity of the output\n"
        "  -t, --gen-test        generate a standalone unit test for the "
        "adjoint code\n"
        "  -otest TEST_FILENAME  filename for the unit test (implies -t)\n"
        "  -oad OAD              filename for the transformed code\n")
    assert expected3 in output


# no args
def test_main_no_args(capsys):
    '''Test that the main() function raises an exception if the required
    arguments are not supplied.

    '''
    with pytest.raises(SystemExit) as info:
        main([])
    assert str(info.value) == "2"
    output, error = capsys.readouterr()
    assert output == ""
    # Python2 returns a different message to Python3. Also, the name
    # of the executable is replaced with either pytest or -c when
    # using pytest, therefore we split the test into sections.
    expected1 = "usage: "
    expected2 = ("[-h] [-oad OAD] [-v] [-t] [-otest TEST_FILENAME] "
                 "-a ACTIVE [ACTIVE ...] -- filename")
    if six.PY2:
        expected3 = "error: too few arguments\n"
    else:
        expected3 = ("error: the following arguments are required: "
                     "-a/--active, filename\n")
    assert expected1 in error
    assert expected2 in error
    assert expected3 in error


# no -a
def test_main_no_a_arg(capsys):
    '''Test that the main() function raises an exception if the -a
    argument is not supplied.
    '''
    with pytest.raises(SystemExit) as info:
        main(["file"])
    assert str(info.value) == "2"
    output, error = capsys.readouterr()
    assert output == ""
    expected = ("error: the following arguments are required: "
                "-a/--active")
    if six.PY2:
        expected = "argument -a/--active is required"
    assert expected in error


# no -a arg arg
def test_main_no_a_arg_arg(capsys):
    '''Test that the main() function raises an exception if an argument to
    the -a argument is not supplied.
    '''
    with pytest.raises(SystemExit) as info:
        main(["file", "-a"])
    assert str(info.value) == "2"
    output, error = capsys.readouterr()
    assert output == ""
    expected = ("error: argument -a/--active: expected at least one "
                "argument")
    assert expected in error


# no filename
def test_main_no_filename(capsys):
    '''Test that the main() function raises an exception if no filename is
    supplied.
    '''
    with pytest.raises(SystemExit) as info:
        main(["-a", "var"])
    assert str(info.value) == "2"
    output, error = capsys.readouterr()
    assert output == ""
    expected = "error: the following arguments are required: filename\n"
    if six.PY2:
        expected = "error: too few arguments\n"
    assert expected in error


# no --
def test_main_no_separator(capsys):
    '''Test that the main() function raises an exception if the -- is not
    provided between the argument and the filename.

    '''
    with pytest.raises(SystemExit) as info:
        main(["-a", "var", "filename"])
    assert str(info.value) == "2"
    output, error = capsys.readouterr()
    assert output == ""
    expected = "error: the following arguments are required: filename\n"
    if six.PY2:
        expected = "error: too few arguments\n"
    assert expected in error


# invalid filename
@pytest.mark.xfail(reason="issue #1235: caplog returns an empty string in "
                   "github actions.", strict=False)
def test_main_invalid_filename(capsys, caplog):
    '''Test that the the main() function raises an exception if the
    file specified by filename does not exist.

    '''
    with pytest.raises(SystemExit) as info:
        main(["-a", "var", "--", "does_not_exist.f90"])
    assert str(info.value) == "1"
    output, error = capsys.readouterr()
    assert output == ""
    assert error == ""
    assert "file 'does_not_exist.f90', not found." in caplog.text


# Exceptions in adjoint generation (TangentLinearError, TypeError,
# KeyError, NotImplementedError)

def test_main_tangentlinearerror(tmpdir, capsys):
    '''Test that a TangentLinearError exception is picked up when
    generating an adjoint and appropriate information output to
    stdout. This can be triggered by providing active variables that
    mean that the supplied code is not tangent linear. For example,
    for the assignment `a=b`, if `b` were specified as being active
    but `a` was not, the code would not be a valid tangent linear
    code.

    '''
    test_prog = (
        "program test\n"
        "real :: a, b\n"
        "a = b\n"
        "end program test\n")
    filename = six.text_type(tmpdir.join("tl.f90"))
    with open(filename, "w", encoding='utf-8') as my_file:
        my_file.write(test_prog)
    with pytest.raises(SystemExit) as info:
        main(["-a", "b", "--", filename])
    assert str(info.value) == "1"
    output, error = capsys.readouterr()
    assert error == ""
    assert ("Assignment node 'a = b\n' has the following active variables "
            "on its RHS '['b']' but its LHS 'a' is not an active variable."
            in output)


def test_main_keyerror(tmpdir, capsys):
    '''Test that a KeyError exception is picked up when generating an
    adjoint and appropriate information output to stdout. This can be
    triggered by providing a variable name that does not exist in the
    code.

    '''
    filename = six.text_type(tmpdir.join("tl.f90"))
    with open(filename, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_PROG)
    with pytest.raises(SystemExit) as info:
        main(["-a", "doesnotexist", "--", filename])
    assert str(info.value) == "1"
    output, error = capsys.readouterr()
    assert error == ""
    assert "Could not find 'doesnotexist' in the Symbol Table." in output


def test_main_not_implemented_error(tmpdir, capsys):
    ''' Test that a NotImplementedError is caught when generating an adjoint
    test harness and that appropriate information is output to stdout. This
    can be triggered when the set of active variables are not all of the
    same type or precision. '''
    test_prog = (
        "module my_mod\n"
        "contains\n"
        "subroutine test\n"
        "real :: a\n"
        "integer :: b\n"
        "a = b\n"
        "end subroutine test\n"
        "end module my_mod\n")
    filename = six.text_type(tmpdir.join("tl.f90"))
    with open(filename, "w", encoding='utf-8') as my_file:
        my_file.write(test_prog)
    with pytest.raises(SystemExit) as info:
        main(["-a", "a", "b", "-t", "--", filename])
    assert str(info.value) == "1"
    output, error = capsys.readouterr()
    assert error == ""
    assert "'a' is of intrinsic type 'Intrinsic.REAL'" in output
    assert "This is not currently supported" in output


def test_main_new_var(tmpdir):
    '''Test that the main() function works when -a specifies a variable
    name that does not exist in the original code but gets created as
    part of the internal support for transformations.

    '''
    code = (
        "program test\n"
        "real :: a, b(10), c(10)\n"
        "a = dot_product(b(:), c(:))\n"
        "end program test\n")
    filename = str(tmpdir.join("tl.f90"))
    with open(filename, "w", encoding='utf-8') as my_file:
        my_file.write(code)
    main(["-a", "a", "b", "res_dot_product", "--", filename])


# writing to stdout
def test_main_stdout(tmpdir, capsys):
    '''Test that the the main() function returns its output to stdout by
    default.

    '''
    expected = (
        "program test_adj\n"
        "  real :: a\n\n"
        "  a = 0.0\n"
        "  a = 0.0\n\n"
        "end program test_adj\n")
    filename = six.text_type(tmpdir.join("tl.f90"))
    with open(filename, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_PROG)
    main(["-a", "a", "--", filename])
    output, error = capsys.readouterr()
    assert error == ""
    assert expected in output


# using -oad
def test_main_fileout(tmpdir, capsys):
    '''Test that the the main() function returns its output to a file if
    specified.

    '''
    expected = (
        "program test_adj\n"
        "  real :: a\n\n"
        "  a = 0.0\n"
        "  a = 0.0\n\n"
        "end program test_adj\n")
    filename_in = str(tmpdir.join("tl.f90"))
    filename_out = str(tmpdir.join("ad.f90"))
    with open(filename_in, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_PROG)
    main([filename_in, "-oad", filename_out, "-a", "a"])
    output, error = capsys.readouterr()
    assert error == ""
    assert output == ""
    with open(filename_out, 'r', encoding='utf-8') as my_file:
        data = my_file.read()
    assert expected in data


def test_main_t_option(tmpdir, capsys):
    ''' Test that the -t option causes the test harness to be generated. '''
    filename_in = str(tmpdir.join("tl.f90"))
    filename_out = str(tmpdir.join("ad.f90"))
    with open(filename_in, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_MOD)
    main([filename_in, "-oad", filename_out, "-t", "-a", "field"])
    output, error = capsys.readouterr()
    assert error == ""
    assert EXPECTED_HARNESS_CODE in output


@pytest.mark.parametrize("extra_args", [[], ["-t"]])
def test_main_otest_option(tmpdir, capsys, extra_args):
    ''' Test that the -otest option switches on test-harness generation and
    causes the result to be written to file. We check with and without the
    (superfluous) '-t' flag. '''
    filename_in = str(tmpdir.join("tl.f90"))
    filename_out = str(tmpdir.join("ad.f90"))
    harness_out = str(tmpdir.join("harness.f90"))
    with open(filename_in, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_MOD)
    main([filename_in, "-a", "field", "-oad", filename_out,
          "-otest", harness_out] + extra_args)
    output, error = capsys.readouterr()
    assert error == ""
    assert output == ""
    with open(harness_out, 'r', encoding='utf-8') as my_file:
        data = my_file.read()
    assert EXPECTED_HARNESS_CODE in data


# -v output
@pytest.mark.xfail(reason="issue #1235: caplog returns an empty string in "
                   "github actions.", strict=False)
def test_main_verbose(tmpdir, capsys, caplog):
    '''Test that the the main() function outputs additional information if
    the -v flag is set. Actually -v seems to have no effect here as
    pytest takes control of the logging and we have to set it to the
    required level manually.

    '''
    tl_code = (
        "program test\n"
        "real :: a\n"
        "a = 0.0\n"
        "end program test\n")
    filename_in = str(tmpdir.join("tl.f90"))
    filename_out = str(tmpdir.join("ad.f90"))
    with open(filename_in, "w", encoding='utf-8') as my_file:
        my_file.write(tl_code)
    with caplog.at_level(logging.DEBUG):
        main([filename_in, "-v", "-a", "a", "-oad", filename_out])

    output, error = capsys.readouterr()
    assert error == ""
    assert output == ""
    assert "Reading kernel file" in caplog.text
    assert "/tl.f90" in caplog.text
    assert "Writing adjoint of kernel to file /" in caplog.text
    assert "/ad.f90" in caplog.text


@pytest.mark.xfail(reason="issue #1235: caplog returns an empty string in "
                   "github actions.", strict=False)
def test_main_otest_verbose(tmpdir, caplog):
    ''' Test that the -otest option combined with -v generates the expected
    logging output. '''
    filename_in = str(tmpdir.join("tl.f90"))
    filename_out = str(tmpdir.join("ad.f90"))
    harness_out = str(tmpdir.join("harness.f90"))
    with open(filename_in, "w", encoding='utf-8') as my_file:
        my_file.write(TEST_MOD)
    with caplog.at_level(logging.DEBUG):
        main([filename_in, "-v", "-oad", filename_out, "-otest", harness_out])
    assert ("Creating test harness for TL kernel 'kern' and AD kernel "
            "'kern_adj'" in caplog.text)
    assert "Created test-harness program named 'adj_test'" in caplog.text
    assert "end program adj_test" in caplog.text
    assert "Writing test harness for adjoint kernel to file" in caplog.text
    assert "/harness.f90" in caplog.text
