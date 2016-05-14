#! ../env/bin/python
# -*- coding: utf-8 -*-
from insynsregistret.client import Session


def test_placeholder():
    i = Session()
    i.get(from_date='2016-05-08', to_date='2016-05-11')
    assert True

