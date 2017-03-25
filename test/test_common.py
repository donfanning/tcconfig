# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from tcconfig._common import (
    is_anywhere_network,
    get_anywhere_network,
    sanitize_network,
)


class Test_is_anywhere_network:

    @pytest.mark.parametrize(["network", "ip_version", "expected"], [
        ["0.0.0.0/0", 4, True],
        ["192.168.0.0/0", 4, False],
        ["::0/0", 6, True],
        ["2001:db00::0/24", 6, False],
    ])
    def test_normal(self, network, ip_version, expected):
        assert is_anywhere_network(network, ip_version) == expected

    @pytest.mark.parametrize(["network", "ip_version",  "expected"], [
        [None, 4, ValueError],
        ["0.0.0.0/0", None, ValueError],
    ])
    def test_exception(self, network, ip_version, expected):
        with pytest.raises(expected):
            is_anywhere_network(network, ip_version)


class Test_get_anywhere_network:

    @pytest.mark.parametrize(["value", "expected"], [
        [4, "0.0.0.0/0"],
        ["4", "0.0.0.0/0"],
        [6, "::0/0"],
        ["6", "::0/0"],
    ])
    def test_normal(self, value, expected):
        assert get_anywhere_network(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ValueError],
        ["test", ValueError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            get_anywhere_network(value)


class Test_sanitize_network:

    @pytest.mark.parametrize(["value", "expected"], [
        ["192.168.0.1", "192.168.0.1/32"],
        ["192.168.0.1/32", "192.168.0.1/32"],
        ["192.168.0.0/24", "192.168.0.0/24"],
        ["192.168.0.0/23", "192.168.0.0/23"],
        ["anywhere", "0.0.0.0/0"],
        ["ANYWHERE", "0.0.0.0/0"],
        ["", ""],
        [None, ""],
    ])
    def test_normal(self, value, expected):
        assert sanitize_network(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["192.168.0.1111", ValueError],
        ["192.168.0.", ValueError],
        [".168.0.1", ValueError],
        ["192.168.1.0/23", ValueError],
        ["192.168.0.0/33", ValueError],
        ["test", ValueError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            sanitize_network(value)
