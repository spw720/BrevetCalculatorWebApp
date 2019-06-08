import acp_times

"""
open_time(control_dist_km, brevet_dist_km, brevet_start_time)
close_time(control_dist_km, brevet_dist_km, brevet_start_time)

Args:
   control_dist_km:  number, the control distance in kilometers

   brevet_dist_km: number, the nominal distance of the brevet
	   in kilometers, which must be one of 200, 300, 400, 600,
	   or 1000 (the only official ACP brevet distances)

   brevet_start_time:  An ISO 8601 format date-time string indicating
	   the official start time of the brevet
"""

start = '2017-01-01T00:00:00.000Z'

def test_open0():
	assert acp_times.open_time(0, 200, start) == '2017-01-01T00:00:00+00:00'
def test_open1():
	assert acp_times.open_time(100, 300, start) == '2017-01-01T02:56:28.235294+00:00'
def test_open2():
	assert acp_times.open_time(400, 400, start) == '2017-01-01T12:07:56.470588+00:00'
def test_open3():
	assert acp_times.open_time(400, 600, start) == '2017-01-01T12:07:56.470588+00:00'
def test_open4():
	assert acp_times.open_time(1111, 1000, start) == '2017-01-02T09:05:05.042017+00:00'

def test_close0():
	assert acp_times.close_time(0, 200, start) == '2017-01-01T01:00:00+00:00'
def test_close1():
	assert acp_times.close_time(100, 300, start) == '2017-01-01T06:40:00+00:00'
def test_close2():
	assert acp_times.close_time(400, 400, start) == '2017-01-02T03:00:00+00:00'
def test_close3():
	assert acp_times.close_time(400, 600, start) == '2017-01-02T02:40:00+00:00'
def test_close4():
	assert acp_times.close_time(1111, 1000, start) == '2017-01-04T03:00:00+00:00'
