query_string = 'SELECT * FROM ionosphere'
from_timestamp = request.args.get('from_timestamp', None)
request.args = 10
new_query_string = '%s AND anomaly_timestamp >= %s' % (query_string, from_timestamp)
query_string = new_query_string
stmt = query_string
it = engine.execute(stmt)
