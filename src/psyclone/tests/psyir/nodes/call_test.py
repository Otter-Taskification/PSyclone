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
# Author R. W. Ford STFC Daresbury Lab
# -----------------------------------------------------------------------------

''' Performs py.test tests on the Call PSyIR node. '''

from __future__ import absolute_import
import pytest
from psyclone.psyir.nodes import (
    Call, Reference, ArrayReference, Schedule, Literal)
from psyclone.psyir.nodes.node import colored
from psyclone.psyir.symbols import ArrayType, INTEGER_TYPE, DataSymbol, \
    RoutineSymbol, NoType, REAL_TYPE
from psyclone.errors import GenerationError


class SpecialCall(Call):
    '''Test Class specialising the Call class'''


def test_call_init():
    '''Test that a Call can be created as expected. Also test the routine
    property.

    '''
    # routine argument
    routine = RoutineSymbol("jo", NoType())
    call = Call(routine)
    assert call._routine is routine
    assert call.routine is call._routine
    assert call.parent is None
    assert call.children == []

    # optional parent argument
    parent = Schedule()
    call = Call(routine, parent=parent)
    assert call.routine is routine
    assert call.parent is parent
    assert call.children == []


def test_call_equality():
    '''Test the __eq__ method of the Call class. '''
    # routine arguments
    routine = RoutineSymbol("j", NoType())
    routine2 = RoutineSymbol("k", NoType())
    call1 = Call(routine)
    call2 = Call(routine)
    assert call1 == call2

    call3 = Call(routine2)
    assert call1 != call3

    # Check with argument names
    call4 = Call.create(routine, [("name", Literal("1.0", REAL_TYPE))])
    call5 = Call.create(routine, [("name", Literal("1.0", REAL_TYPE))])
    assert call4 == call5

    # Check with argument name and no argument name
    call6 = Call.create(routine, [Literal("1.0", REAL_TYPE)])
    assert call4 != call6

    # Check with different argument names
    call7 = Call.create(routine, [("new_name", Literal("1.0", REAL_TYPE))])
    assert call4 != call7


def test_call_init_error():
    '''Test that the appropriate exception is raised if the routine
    argument is not a RoutineSymbol.

    '''
    with pytest.raises(TypeError) as info:
        _ = Call(None)
    assert ("Call routine argument should be a RoutineSymbol but found "
            "'NoneType'." in str(info.value))


@pytest.mark.parametrize("cls", [Call, SpecialCall])
def test_call_create(cls):
    '''Test that the create method creates a valid call with arguments,
    some of which are named. Also checks the routine and argument_names
    properties.

    '''
    routine = RoutineSymbol("ellie", INTEGER_TYPE)
    array_type = ArrayType(INTEGER_TYPE, shape=[10, 20])
    arguments = [Reference(DataSymbol("arg1", INTEGER_TYPE)),
                 ArrayReference(DataSymbol("arg2", array_type))]
    call = cls.create(routine, [arguments[0], ("name", arguments[1])])
    # pylint: disable=unidiomatic-typecheck
    assert type(call) is cls
    assert call.routine is routine
    assert call.argument_names == [None, "name"]
    for idx, child, in enumerate(call.children):
        assert child is arguments[idx]
        assert child.parent is call


def test_call_create_error1():
    '''Test that the appropriate exception is raised if the routine
    argument to the create method is not a RoutineSymbol.

    '''
    with pytest.raises(GenerationError) as info:
        _ = Call.create(None, [])
    assert ("Call create routine argument should be a RoutineSymbol but "
            "found 'NoneType'." in str(info.value))


def test_call_create_error2():
    '''Test that the appropriate exception is raised if the arguments
    argument to the create method is not a list'''
    routine = RoutineSymbol("isaac", NoType())
    with pytest.raises(GenerationError) as info:
        _ = Call.create(routine, None)
    assert ("Call create arguments argument should be a list but found "
            "'NoneType'." in str(info.value))


def test_call_create_error3():
    '''Test that the appropriate exception is raised if an entry in the
    arguments argument to the create method is is a tuple that does
    not have two elements.'''
    routine = RoutineSymbol("isaac", NoType())
    with pytest.raises(GenerationError) as info:
        _ = Call.create(routine, [(1, 2, 3)])
    assert ("If a child of the children argument in create method of Call "
            "class is a tuple, it's length should be 2, but found 3."
            in str(info.value))


def test_call_create_error4():
    '''Test that the appropriate exception is raised if an entry in the
    arguments argument to the create method is is a tuple with two
    elements and the first element is not a string.'''
    routine = RoutineSymbol("isaac", NoType())
    with pytest.raises(GenerationError) as info:
        _ = Call.create(routine, [(1, 2)])
    assert ("If a child of the children argument in create method of Call "
            "class is a tuple, its first argument should be a str, but "
            "found int." in str(info.value))


def test_call_create_error5():
    '''Test that the appropriate exception is raised if one or more of the
    argument names is not valid.'''
    routine = RoutineSymbol("roo", INTEGER_TYPE)
    with pytest.raises(ValueError) as info:
        _ = Call.create(
            routine, [Reference(DataSymbol(
                "arg1", INTEGER_TYPE)), (" a", None)])
    assert "Invalid name ' a' found." in str(info.value)


def test_call_create_error6():
    '''Test that the appropriate exception is raised if one or more of the
    arguments argument list entries to the create method is not a
    DataNode.

    '''
    routine = RoutineSymbol("roo", INTEGER_TYPE)
    with pytest.raises(GenerationError) as info:
        _ = Call.create(
            routine, [Reference(DataSymbol(
                "arg1", INTEGER_TYPE)), ("name", None)])
    assert ("Item 'NoneType' can't be child 1 of 'Call'. The valid format "
            "is: '[DataNode]*'." in str(info.value))


def test_call_appendnamedarg():
    '''Test the append_named_arg method in the Call class. Check
    it raises the expected exceptions if arguments are invalid and
    that it works as expected when the input is valid.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("2", INTEGER_TYPE)
    op3 = Literal("3", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("hello"), [])
    # name arg wrong type
    with pytest.raises(TypeError) as info:
        call.append_named_arg(1, op1)
    assert ("A name should be a string or None, but found int."
            in str(info.value))
    # invalid name
    with pytest.raises(ValueError) as info:
        call.append_named_arg("_", op1)
    assert "Invalid name '_' found." in str(info.value)
    # name arg already used
    call.append_named_arg("name1", op1)
    with pytest.raises(ValueError) as info:
        call.append_named_arg("name1", op2)
    assert ("The value of the name argument (name1) in 'append_named_arg' in "
            "the 'Call' node is already used for a named argument."
            in str(info.value))
    # ok
    call.append_named_arg("name2", op2)
    call.append_named_arg(None, op3)
    assert call.children == [op1, op2, op3]
    assert call.argument_names == ["name1", "name2", None]


def test_call_insertnamedarg():
    '''Test the insert_named_arg method in the Call class. Check
    it raises the expected exceptions if arguments are invalid and
    that it works as expected when the input is valid.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("2", INTEGER_TYPE)
    op3 = Literal("3", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("hello"), [])
    # name arg wrong type
    with pytest.raises(TypeError) as info:
        call.insert_named_arg(1, op1, 0)
    assert ("A name should be a string or None, but found int."
            in str(info.value))
    # invalid name
    with pytest.raises(ValueError) as info:
        call.insert_named_arg("1", op1, 0)
    assert "Invalid name '1' found." in str(info.value)
    # name arg already used
    call.insert_named_arg("name1", op1, 0)
    with pytest.raises(ValueError) as info:
        call.insert_named_arg("name1", op2, 0)
    assert ("The value of the name argument (name1) in 'insert_named_arg' in "
            "the 'Call' node is already used for a named argument."
            in str(info.value))
    # invalid index type
    with pytest.raises(TypeError) as info:
        call.insert_named_arg("name2", op2, "hello")
    assert ("The 'index' argument in 'insert_named_arg' in the 'Call' node "
            "should be an int but found str." in str(info.value))
    # ok
    assert call.children == [op1]
    assert call.argument_names == ["name1"]
    call.insert_named_arg("name2", op2, 0)
    assert call.children == [op2, op1]
    assert call.argument_names == ["name2", "name1"]
    call.insert_named_arg(None, op3, 0)
    assert call.children == [op3, op2, op1]
    assert call.argument_names == [None, "name2", "name1"]


def test_call_replacenamedarg():
    '''Test the replace_named_arg method in the Call class. Check
    it raises the expected exceptions if arguments are invalid and
    that it works as expected when the input is valid.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("2", INTEGER_TYPE)
    op3 = Literal("3", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("hello"),
                       [("name1", op1), ("name2", op2)])

    # name arg wrong type
    with pytest.raises(TypeError) as info:
        call.replace_named_arg(1, op3)
    assert ("The 'name' argument in 'replace_named_arg' in the 'Call' "
            "node should be a string, but found int." in str(info.value))
    # name arg is not found
    with pytest.raises(ValueError) as info:
        call.replace_named_arg("new_name", op3)
    assert ("The value of the existing_name argument (new_name) in "
            "'insert_named_arg' in the 'Call' node was not found in the "
            "existing arguments." in str(info.value))
    # ok
    assert call.children == [op1, op2]
    assert call.argument_names == ["name1", "name2"]
    assert call._argument_names[0][0] == id(op1)
    assert call._argument_names[1][0] == id(op2)
    call.replace_named_arg("name1", op3)
    assert call.children == [op3, op2]
    assert call.argument_names == ["name1", "name2"]
    assert call._argument_names[0][0] == id(op3)
    assert call._argument_names[1][0] == id(op2)


def test_validate_name_type():
    '''Test that the _validate_name utility raise an error if the wrong
    type is provided and returns successfully if the expected type is
    provided.

    '''
    call = Call(RoutineSymbol("x"))
    # invalid type
    with pytest.raises(TypeError) as info:
        call._validate_name(2)
    assert ("A name should be a string or None, but found int."
            in str(info.value))
    # ok
    call._validate_name(None)
    # ok
    call._validate_name("hello")


@pytest.mark.parametrize("name", ["", "0", "_", " a", "a ", "a*"])
def test_validate_name_invalid(name):
    '''Test the _validate_name utility raises the expected exception when
    the supplied name is invalid.'''
    call = Call(RoutineSymbol("x"))
    with pytest.raises(ValueError) as info:
        call._validate_name(name)
    assert f"Invalid name '{name}' found." in str(info.value)


@pytest.mark.parametrize("name", ["a", "A", "aA", "a1", "a_", "a3B_"])
def test_validate_name_valid(name):
    '''Test the _validate_name utility accepts valid names.'''
    call = Call(RoutineSymbol("x"))
    call._validate_name(name)


def test_call_argumentnames_after_removearg():
    '''Test the argument_names property makes things consistent if a child
    argument is removed. This is used transparently by the class to
    keep things consistent.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("1", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    assert call.argument_names == ["name1", "name2"]
    call.children.pop(0)
    assert len(call.children) == 1
    assert len(call._argument_names) == 2
    # argument_names property makes _argument_names list consistent.
    assert call.argument_names == ["name2"]
    assert len(call._argument_names) == 1


def test_call_argumentnames_after_addarg():
    '''Test the argument_names property makes things consistent if a child
    argument is added. This is used transparently by the class to
    keep things consistent.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("1", INTEGER_TYPE)
    op3 = Literal("1", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    assert call.argument_names == ["name1", "name2"]
    call.children.append(op3)
    assert len(call.children) == 3
    assert len(call._argument_names) == 2
    # argument_names property makes _argument_names list consistent.
    assert call.argument_names == ["name1", "name2", None]
    assert len(call._argument_names) == 3


def test_call_argumentnames_after_replacearg():
    '''Test the argument_names property makes things consistent if a child
    argument is replaced. This is used transparently by the class to
    keep things consistent.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("1", INTEGER_TYPE)
    op3 = Literal("1", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    assert call.argument_names == ["name1", "name2"]
    call.children[0] = op3
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    # argument_names property makes _argument_names list consistent.
    assert call._argument_names[0][0] != id(call.children[0])
    assert call.argument_names == [None, "name2"]
    assert len(call._argument_names) == 2
    assert call._argument_names[0][0] == id(call.children[0])


def test_call_argumentnames_after_reorderarg():
    '''Test the argument_names property makes things consistent if a child
    argument is replaced. This is used transparently by the class to
    keep things consistent.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("1", INTEGER_TYPE)
    op3 = Literal("1", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    assert call.argument_names == ["name1", "name2"]
    call.children[0] = op3
    assert len(call.children) == 2
    assert len(call._argument_names) == 2
    # argument_names property makes _argument_names list consistent.
    assert call.argument_names == [None, "name2"]
    assert len(call._argument_names) == 2


def test_call_node_reconcile_add():
    '''Test that the reconcile method behaves as expected. Use an example
    where we add a new arg.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("1", INTEGER_TYPE)
    op3 = Literal("1", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    # consistent
    assert len(call._argument_names) == 2
    assert call._argument_names[0] == (id(call.children[0]), "name1")
    assert call._argument_names[1] == (id(call.children[1]), "name2")
    call.children.append(op3)
    # inconsistent
    assert len(call._argument_names) == 2
    assert call._argument_names[0] == (id(call.children[0]), "name1")
    assert call._argument_names[1] == (id(call.children[1]), "name2")
    call._reconcile()
    # consistent
    assert len(call._argument_names) == 3
    assert call._argument_names[0] == (id(call.children[0]), "name1")
    assert call._argument_names[1] == (id(call.children[1]), "name2")
    assert call._argument_names[2] == (id(call.children[2]), None)


def test_call_node_reconcile_reorder():
    '''Test that the reconcile method behaves as expected. Use an example
    where we reorder the arguments.

    '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("2", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    # consistent
    assert len(call._argument_names) == 2
    assert call._argument_names[0] == (id(call.children[0]), "name1")
    assert call._argument_names[1] == (id(call.children[1]), "name2")
    call.children = [op2.detach(), op1.detach()]
    # inconsistent
    assert len(call._argument_names) == 2
    assert call._argument_names[0] != (id(call.children[0]), "name1")
    assert call._argument_names[1] != (id(call.children[1]), "name2")
    call._reconcile()
    # consistent
    assert len(call._argument_names) == 2
    assert call._argument_names[0] == (id(call.children[0]), "name2")
    assert call._argument_names[1] == (id(call.children[1]), "name1")


def test_call_node_str():
    ''' Test that the node_str method behaves as expected '''
    routine = RoutineSymbol("isaac", NoType())
    call = Call(routine)
    colouredtext = colored("Call", Call._colour)
    assert call.node_str() == colouredtext+"[name='isaac']"


def test_call_str():
    ''' Test that the str method behaves as expected '''
    routine = RoutineSymbol("roo", NoType())
    call = Call(routine)
    assert str(call) == "Call[name='roo']"


def test_copy():
    ''' Test that the copy() method behaves as expected. '''
    op1 = Literal("1", INTEGER_TYPE)
    op2 = Literal("2", INTEGER_TYPE)
    call = Call.create(RoutineSymbol("name"), [("name1", op1), ("name2", op2)])
    # consistent call
    call_copy = call.copy()
    assert call._argument_names[0] == (id(call.children[0]), "name1")
    assert call._argument_names[1] == (id(call.children[1]), "name2")
    assert call_copy._argument_names[0] == (id(call_copy.children[0]), "name1")
    assert call_copy._argument_names[1] == (id(call_copy.children[1]), "name2")
    assert call._argument_names != call_copy._argument_names

    call.children = [op2.detach(), op1.detach()]
    assert call._argument_names[0] != (id(call.children[0]), "name2")
    assert call._argument_names[1] != (id(call.children[1]), "name1")
    # inconsistent call
    call_copy = call.copy()
    assert call._argument_names[0] == (id(call.children[0]), "name2")
    assert call._argument_names[1] == (id(call.children[1]), "name1")
    assert call_copy._argument_names[0] == (id(call_copy.children[0]), "name2")
    assert call_copy._argument_names[1] == (id(call_copy.children[1]), "name1")
    assert call._argument_names != call_copy._argument_names
