use cmccb2b
db.Cmccb2bItem.count()
db.Cmccb2bItem.aggregate([ 
	{'$project': {'day': {'$substr': ['$crawled_time', 0,10]}}}, 
	{'$group':{'_id': '$day', 'number': {'$sum': 1} }}, 
	{'$sort': {'_id':-1}}
])
