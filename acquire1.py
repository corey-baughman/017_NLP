def get_google_sheet(url_as_string):
    csv_export_url = url_as_string.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(csv_export_url)
    return


def get_titanic_data():
    '''
    must import env
    '''
    url = env.get_db_url('titanic_db')
    query = '''select * from passengers;'''
    return pd.read_sql(query, url)

def get_iris_data():
    '''
    must import env
    '''
    url = env.get_db_url('iris_db')
    query = '''select * from species
	right join measurements
		using(species_id);'''
    return pd.read_sql(query, url)
        
def get_telco_data():
    '''
    must import env
    '''
    url = env.get_db_url('telco_churn')
    query = '''select * from customers
	left join contract_types
		using(contract_type_id)
	left join internet_service_types
		using(internet_service_type_id)
	left join payment_types
		using(payment_type_id)'''
    return pd.read_sql(query, url)