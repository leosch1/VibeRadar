from math import sqrt
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import text
import timeit
import random
import time

Base = declarative_base()

class City(Base):
    """
    ORM model representing a city record in the cities table.
    """
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=True)
    region_code = Column(String, nullable=True)
    playlist_id = Column(String, nullable=True)
    country_name = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    geom = Column(String, nullable=True)
    active = Column(Boolean, default=False, nullable=True)
    video_id = Column(String, nullable=True)

class Connection(Base):
    """
    ORM model representing a connection record in the connections table.
    """
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_lat = Column(Float, nullable=True)
    start_lon = Column(Float, nullable=True)
    end_lat = Column(Float, nullable=True)
    end_lon = Column(Float, nullable=True)

class DatabaseOperations:
    """
    Encapsulates operations for database interaction using SQLAlchemy.
    
    Attributes:
        engine (Engine): The SQLAlchemy engine.
        session (Session): The current SQLAlchemy session.
    """

    def __init__(self, db_url: str = "postgresql://postgres:postgres@localhost/postgres"):
        """
        Initialize the database connection, creating tables if they don't exist.
        
        Args:
            db_url (str): A database connection URL. Default is for local PostgreSQL.
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        self.session: Session = SessionLocal()
        self.connections_dict = {}

    def insert_record(self, record: dict) -> None:
        """
        Insert a new record into the cities table.
        
        Args:
            record (dict): A dictionary containing the record details.
                Expected keys: 'city', 'region_code', 'playlist_id', 'country', 'lat', 'lon'
        """
        try:
            new_city = City(
                city_name=record["city"],
                region_code=record["region_code"],
                playlist_id=record["playlist_id"],
                country_name=record["country"],
                lat=record["lat"],
                lon=record["lon"]
            )
            self.session.add(new_city)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Failed to insert record for {record.get('city')} - {record.get('region_code')}: {e}")

    def get_last_id(self) -> int:
        """
        Retrieve the highest city ID from the cities table.
        
        Returns:
            int: The maximum ID present in the table, or 0 if the table is empty.
        """
        last_id = self.session.query(func.max(City.id)).scalar()
        return last_id if last_id is not None else 0

    def get_nearest_playlist(self, location: tuple) -> City:
        """
        Get the nearest city record to the provided location.
        
        This method uses a basic Euclidean distance calculation as an approximation.
        For more accurate geospatial queries, consider using a geospatial database extension.
        
        Args:
            location (tuple): A tuple representing (latitude, longitude).
        
        Returns:
            City: The nearest city record, or None if no records exist.
        """
        lat, lon = location
        cities = self.session.query(City).all()

        if not cities:
            return None

        # Find the city with the minimum Euclidean distance to the specified location.
        nearest_city = min(
            cities,
            key=lambda city: float('inf') if city.lat is None or city.lon is None else sqrt((city.lat - lat) ** 2 + (city.lon - lon) ** 2)
        )
        return nearest_city
    
    def get_nearest_playlist2(self, location: tuple) -> dict:
        """
        Get the nearest city record (playlist) using a geospatial SQL query with PostGIS functions.

        This method executes a raw SQL query that leverages PostGIS's ST_Distance to compute the
        distance in meters from the provided location to each city (using the geom field). It orders
        the results by this distance and limits to the nearest record.

        Args:
            location (tuple): A tuple representing (latitude, longitude). Note: ST_MakePoint expects
                            longitude first, so we pass parameters accordingly.

        Returns:
            dict: A dictionary containing the keys 'city_name', 'country_name', 'playlist_id', 'lat',
                'lon', and 'distance_m'. Returns None if no record is found.
        """
        lat, lon = location
        query = text("""
            SELECT city_name, country_name, playlist_id, video_id, lat, lon,
                ST_Distance(geom, ST_MakePoint(:lon, :lat)::geography) AS distance_m
            FROM cities
            WHERE lat IS NOT NULL 
                AND lon IS NOT NULL
                AND geom IS NOT NULL
                AND active
            ORDER BY distance_m ASC
            LIMIT 1;
        """)
        result = self.session.execute(query, {"lon": lon, "lat": lat}).fetchone()
        if result is None:
            return None

        return {
            "city_name": result.city_name,
            "country_name": result.country_name,
            "playlist_id": result.playlist_id,
            "video_id": result.video_id,
            "lat": result.lat,
            "lon": result.lon,
            "distance_m": result.distance_m
        }
    
    def insert_connection(self, session, connection) -> None:
        """
        Insert a new connection record into the connections table.
        
        Args:
            session (str): The session ID for the connection.
            connection (dict): A Class object containing the connection details.
        """
        self.connections_dict[session] = {
            "start": { 
                        "lat": connection.start.lat, 
                        "lng": connection.start.lng 
                    },
            "end": { 
                        "lat": connection.end.lat,
                        "lng": connection.end.lng 
                    },
            "expiration": time.time() + 45 # make entry expire after 45 seconds
        }

    def get_additional_connections(self, connections) -> list:
        """
        Generate additional connections to ensure a minimum of 5 connections.

        Args:
            connections (list): A list of existing connection records.
        
        Returns:
            list: A list of additional Connection objects.

        """
        missing = 5 - len(connections)
        cities = self.session.query(City).all()
        # Randomly select cities to create connections
        for _ in range(missing):
            start_city = random.choice(cities)
            end_city = random.choice(cities)

            # reroll if start or end city has no lat/lon
            while start_city.lat is None or start_city.lon is None:
                start_city = random.choice(cities)
            while end_city.lat is None or end_city.lon is None:
                end_city = random.choice(cities)

            # reroll if start and end city are too close to each other
            # while abs(start_city.lat - end_city.lat) < 10 and abs(start_city.lon - end_city.lon) < 10:
            #     end_city = random.choice(cities)

            connections.append({
                                "start": { 
                                    "lat": start_city.lat, 
                                    "lng": start_city.lon 
                                    },
                                "end": { 
                                        "lat": end_city.lat,
                                        "lng": end_city.lon 
                                        }
                                })

        return connections
    
    def get_other_connections(self, my_conn) -> list:
        """
        Retrieve all connection records from the connections table.
        
        Returns:
            list: A list of Connection objects.
        """
        session = my_conn.sessionId
        connection = my_conn.myConnection

        if my_conn.myConnection is not None:
            self.insert_connection(session=session, connection=connection)

        # drop expired connections
        for session, conn in list(self.connections_dict.items()):
            if conn["expiration"] < time.time():
                del self.connections_dict[session]

        # create list with all connections except the one that was just added
        connections = [conn for conn in self.connections_dict.values() if conn != self.connections_dict[session]]
        
        # get random connections from the database if there are less than 5 connections in the dictionary
        if len(connections) < 5:
            connections = self.get_additional_connections(connections)

        return connections

    def close(self) -> None:
        """
        Close the database session and dispose of the engine.
        """
        self.session.close()
        self.engine.dispose()

    def check_db_health(self) -> bool:
        """
        Check the health of the database connection.
        
        Returns:
            bool: True if the connection is healthy, False otherwise.
        """
        try:
            self.session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False



if __name__ == "__main__":
    db_ops = DatabaseOperations()

    # Example nearest playlist lookup
    location = (40.730610, -73.935242)  # Example coordinates near New York City

    # Use timeit to check how long get_nearest_playlist runs.
    num_runs = 10
    repeat = 5
    times = timeit.repeat(lambda: db_ops.get_nearest_playlist(location), repeat=repeat, number=num_runs)
    avg_time = sum(times) / repeat
    print(f"Total time for {num_runs} runs (repeated {repeat} times): {times}")
    print(f"Average time per {num_runs} runs: {avg_time:.6f} seconds")
    print(f"Average time per single run: {avg_time / num_runs:.6f} seconds\n")

    # Now get the nearest playlist as usual and print its details.
    nearest_city = db_ops.get_nearest_playlist(location)
    if nearest_city:
        print("Nearest City Info:")
        print(f"City Name: {nearest_city.city_name}")
        print(f"Region Code: {nearest_city.region_code}")
        print(f"Playlist ID: {nearest_city.playlist_id}")
        print(f"Country Name: {nearest_city.country_name}")
        print(f"Latitude: {nearest_city.lat}")
        print(f"Longitude: {nearest_city.lon}")
    else:
        print("No nearest city found.")

    db_ops.close()
