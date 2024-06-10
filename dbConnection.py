import oracledb


def create_connection(username, password, wallet_location, config_dir, dsn):
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn,
        config_dir=config_dir,
        wallet_location=wallet_location,
        wallet_password=password
    )
    return connection
