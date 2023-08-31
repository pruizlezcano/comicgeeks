from datetime import datetime
def compare_timestamp(local_timestamp,utc_timestamp):
	"""Compare the local timestamp to the server timestamp (UTC).

	Args:
		local_timestamp (int): Local timestamp
		utc_timestamp (int): UTC timestamp
	"""
	utc_time = datetime.utcfromtimestamp(utc_timestamp)
	local_time = datetime.fromtimestamp(local_timestamp)

	return utc_time==local_time
