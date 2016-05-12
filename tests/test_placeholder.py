#! ../env/bin/python
# -*- coding: utf-8 -*-
from insynsregistret.client import Session


def test_placeholder():
    i = Session()
    i.get()
    assert True

