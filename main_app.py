import database

def initialize_database():
    """
    Initializes the database by creating a connection, creating tables,
    and populating the courses. This should only be run once.
    """
    conn = database.create_connection()
    if conn is not None:
        print("Database connection successful. Setting up tables...")
        database.create_tables(conn)
        database.populate_courses(conn)
        conn.close()
        print("Database setup complete.")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    # This block will run when the script is executed directly.
    # It sets up the database.
    initialize_database()
