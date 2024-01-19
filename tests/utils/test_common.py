from sirocco.utils.common import uuid


def test_uuid():
    new_uuid = uuid()
    assert isinstance(new_uuid, str)
    assert len(new_uuid) == 36
