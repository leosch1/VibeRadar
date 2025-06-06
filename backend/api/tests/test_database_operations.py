# tests/test_database_operations.py

import pytest
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.database_operations import DatabaseOperations, City

class DummyPoint:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

@pytest.fixture
def db_ops():
    # use in-memory SQLite to avoid needing a real Postgres instance
    ops = DatabaseOperations(db_url="sqlite:///:memory:")
    yield ops
    ops.close()

def test_get_last_id_empty(db_ops):
    assert db_ops.get_last_id() == 0

def test_get_nearest_playlist_empty(db_ops):
    assert db_ops.get_nearest_playlist((0, 0)) is None

def test_get_nearest_playlist2_no_result(db_ops, monkeypatch):
    # simulate no rows returned by raw SQL
    def fake_execute(query, params):
        class R:
            def fetchone(self): return None
        return R()
    monkeypatch.setattr(db_ops.session, "execute", fake_execute)
    assert db_ops.get_nearest_playlist2((0.0, 0.0)) is None

def test_get_nearest_playlist2_success(db_ops, monkeypatch):
    # simulate a single row returned by raw SQL
    class FakeRow:
        city_name = "A"
        country_name = "C"
        playlist_id = "P"
        lat = 1.1
        lon = 2.2
        distance_m = 123.45
    class R:
        def fetchone(self): return FakeRow()
    monkeypatch.setattr(db_ops.session, "execute", lambda q, p: R())
    res = db_ops.get_nearest_playlist2((0.0, 0.0))
    assert res == {
        "city_name": "A",
        "country_name": "C",
        "playlist_id": "P",
        "lat": 1.1,
        "lon": 2.2,
        "distance_m": 123.45
    }
def test_get_additional_connections(db_ops):
    # Insert just two cities (with a dummy POINT geom) so get_additional_connections can sample.
    coords_list = [(0.0, 0.0), (10.0, 10.0)]
    for lat, lon in coords_list:
        city = City(
            city_name="X",
            region_code="R",
            playlist_id="P",
            country_name="C",
            lat=lat,
            lon=lon,
            geom=f"POINT({lon} {lat})"  # dummy WKT
        )
        db_ops.session.add(city)
    db_ops.session.commit()

    extra = db_ops.get_additional_connections([])
    assert len(extra) == 5
    for conn in extra:
        assert isinstance(conn, dict)
        assert "start" in conn and "end" in conn
        assert "lat" in conn["start"] and "lng" in conn["start"]
        assert "lat" in conn["end"] and "lng" in conn["end"]

def test_get_other_connections(db_ops, monkeypatch):
    # Insert one city (with geom) so get_other_connections can generate extras.
    city = City(
        city_name="Y",
        region_code="R",
        playlist_id="P",
        country_name="C",
        lat=0.0,
        lon=0.0,
        geom="POINT(0.0 0.0)"
    )
    db_ops.session.add(city)
    db_ops.session.commit()

    # Freeze time so expiration logic is predictable
    fixed = 2000.0
    monkeypatch.setattr(time, "time", lambda: fixed)

    # Dummy incoming connection
    start = DummyPoint(5.0, 6.0)
    end   = DummyPoint(7.0, 8.0)
    inner = type("I", (), {})()
    inner.start = start
    inner.end   = end
    dummy = type("D", (), {"sessionId": "s2", "myConnection": inner})()

    conns = db_ops.get_other_connections(dummy)
    assert isinstance(conns, list)
    assert len(conns) == 5

def test_close_does_not_raise(db_ops):
    # just ensure calling close twice doesn't crash
    db_ops.close()
    db_ops.close()
