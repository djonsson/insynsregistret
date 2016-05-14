#! ../env/bin/python
# -*- coding: utf-8 -*-
from insynsregistret.client import Session
from nose.tools import assert_is_none, assert_is_not_none


def test_valid_date_should_not_return_none():
    assert_is_not_none(Session().get(from_date='2001-12-18', to_date='2001-12-18'))


def test_invalid_date_in_the_1900s_should_return_none():
    assert_is_none(Session().get(from_date='1901-05-12', to_date='1901-05-15'))

