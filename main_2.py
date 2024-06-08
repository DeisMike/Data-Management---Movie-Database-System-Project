import pymysql
import tkinter as tk
from decimal import Decimal
from PIL import ImageTk, Image

def run_query():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='12345',
        database='Movies',
        cursorclass=pymysql.cursors.DictCursor  # This line specifies that you want a dictionary cursor
    )

    try:
        with connection.cursor() as cursor:
            # SQL query example (replace with your SQL query)
            sql_query = "SELECT * from Movie"

            # Execute the SQL query
            cursor.execute(sql_query)

            # Fetch all rows from the result set
            result = cursor.fetchall()

            # Display the results
            for row in result:
                print(row)

    finally:
        # Close the connection
        connection.close()
# Function to execute MySQL queries


def execute_query():
    selected_query = dropdown.get()

    # Define your MySQL connection details
    connection = pymysql.connect(host='localhost', user='root', password='12345', database='Movies')
    cursor = connection.cursor()

    # Execute a query based on the selected option in the dropdown
    if selected_query == 'Directed by Joe Johnston':
        #query = "SELECT * FROM Movie"
        query = '''SELECT Movie.MovieName 
        FROM Movie
        JOIN Director ON Movie.MovieID = Director.Movie_ID
        where Director.DirectorName = 'Joe Johnston'
        '''
    elif selected_query == 'Produced by Terrence Malick and distributed by Distributor Warner Bros.':
        #query = "SELECT * FROM Actors"
        query = '''
        SELECT Movie.MovieName
        FROM Movie
        JOIN Producer ON Movie.MovieID = Producer.Movie_ID
        JOIN Distributors ON Movie.MovieID = Distributors.Movie_ID
        WHERE Producer.ProducerName = 'Terrence Malick' AND Distributors.DistributorName = 'Warner Bros.'
        '''
    elif selected_query == 'Warner Bros Artists':
        query = '''
        select actors.actorname
        from actors
        join distributors on actors.movie_id=distributors.movie_id
        where distributors.distributorname = 'Warner Bros.'
        '''
    elif selected_query == 'Distributors who have distributed more than 1 film':
        query = '''
        SELECT Distributors.DistributorName, COUNT(Distributors.Movie_ID) AS MovieCount
        FROM Distributors
        GROUP BY Distributors.DistributorName
        HAVING MovieCount > 1;
        '''
    elif selected_query == 'Producers who have distributed a movie for Sony Pictures artists':
        query = '''
        select distinct producer.producername
        from producer
        join actors on actors.movie_id=producer.movie_id
        where actors.actorname in
        (
        select actors.actorname
        from actors
        join distributors on actors.movie_id=distributors.movie_id
        where distributors.distributorname = 'Sony Pictures'
        )
        '''
    elif selected_query == 'Distributed more than 1 film and has worked with Morgan Lily or Will smith':
        query = '''
        Select Distributors.DistributorName, COUNT(Distributors.Movie_ID) AS MovieCount
        FROM Distributors
        GROUP BY Distributors.DistributorName
        HAVING MovieCount > 1 and Distributors.DistributorName in 
        (
        Select Distributors.DistributorName 
        from distributors 
        inner join Actors on Distributors.Movie_ID=Actors.Movie_ID
        where Actors.ActorName like '%Morgan Lily%' or Actors.ActorName like '%Will%');
        '''
    elif selected_query == 'Average age of actors in movies released after 2000':
        query = '''
        SELECT AVG(Actors.Age) AS AvgAge
        FROM Actors
        JOIN Movie ON Actors.Movie_ID = Movie.MovieID
        WHERE Movie.ReleaseDate > '2000-01-01';
        '''
    elif selected_query == 'Actors with age more than the average age of actors in movies released after 2000':
        query = '''
        select Actors.actorname
        from actors 
        where actors.age>
        (SELECT AVG(Actors.Age) AS AvgAge
        FROM Actors
        JOIN Movie ON Actors.Movie_ID = Movie.MovieID
        WHERE Movie.ReleaseDate > '2000-01-01');'''
    elif selected_query == 'Both Actors and Directors have won awards':
        query = '''
        SELECT DISTINCT M.MovieName
            FROM Movie M, Actors A, Director D
            WHERE M.MovieID = A.Movie_ID
            AND M.MovieID = D.Movie_ID
            AND A.Award IS NOT NULL
            AND D.Award IS NOT NULL;'''
    elif selected_query == 'More than 2 Producers':
        query = '''
        SELECT M.MovieName, count(P.Producername) as Producers
            FROM Movie  M, Producer P
            WHERE M.MovieID = P.Movie_ID
            group by M.MovieName
            Having count(P.Producername)>2;
           '''
    elif selected_query == 'Have directors that have won academy awards':
        query = '''
        SELECT Movie.MovieName, Director.DirectorName, Director.Award
            FROM Movie, Director
            WHERE Movie.MovieID = Director.Movie_ID
            AND Director.Award LIKE '%Academy Award%';
        '''
    elif selected_query == 'Distributors with highest number of PG films':
        query = '''
        select Distributorname,count(Rating)
        from ( 
        select Distributors.Distributorname,Movie.Rating
        from Distributors
        inner join Movie on Movie.MovieID=Distributors.Movie_ID
        where Movie.Rating = 'PG'
        ) as S
        group by Distributorname
        order by count(Rating) desc
        limit 1; 
        '''
    elif selected_query == 'Distributors with least number of PG films':
        query = '''
        select Distributorname,count(Rating)
        from ( 
        select Distributors.Distributorname,Movie.Rating
        from Distributors
        inner join Movie on Movie.MovieID=Distributors.Movie_ID
        where Movie.Rating = 'PG'
        ) as S
        group by Distributorname
        having count(Rating)=
        (
        select F_rating from
        (select Distributorname,count(Rating) as F_rating
        from ( 
        select Distributors.Distributorname,Movie.Rating
        from Distributors
        inner join Movie on Movie.MovieID=Distributors.Movie_ID
        where Movie.Rating = 'PG'
        ) as S
        group by Distributorname
        order by count(Rating) asc
        limit 1) as R)
        ;
        '''
    elif selected_query== 'Distributors with PG films higher than Distributors with least number of PG films':
        query = '''
        select Distributorname,count(Rating)
        from ( 
        select Distributors.Distributorname,Movie.Rating
        from Distributors
        inner join Movie on Movie.MovieID=Distributors.Movie_ID
        where Movie.Rating = 'PG'
        ) as S
        group by Distributorname
        having count(Rating)>
        (
        select F_rating from
        (select Distributorname,count(Rating) as F_rating
        from ( 
        select Distributors.Distributorname,Movie.Rating
        from Distributors
        inner join Movie on Movie.MovieID=Distributors.Movie_ID
        where Movie.Rating = 'PG'
        ) as S
        group by Distributorname
        order by count(Rating) asc
        limit 1) as R)
        ;
        '''
    elif selected_query == 'oldest actor to receive an award in movies released in the 20th century':
        query = '''
        Select Actors.Actorname, Actors.Age
        from Actors where Actors.Age =
        (SELECT max(Actors.Age)
            FROM Actors
            join Movie on Actors.Movie_ID = Movie.MovieID
            WHERE Movie.ReleaseDate > '2000-01-01'
            AND Actors.Award IS NOT NULL);

        '''

    cursor.execute(query)
    result = cursor.fetchall()

    # Display the query result in the Text widget
    output_text.delete(1.0, tk.END)  # Clear previous content

    # Display the query result (modify as needed)
    '''
    for row in result:
        print(row)
    '''
    '''
    for row in result:
        output_text.insert(tk.END, str(row) + '\n')
    '''
    for row in result:
        # Convert Decimal objects to standard Python types
        row = [str(item) if isinstance(item, Decimal) else item for item in row]
        output_text.insert(tk.END, str(row) + '\n')  # Insert each row into the Text widget
    cursor.close()
    connection.close()



if __name__ == '__main__':
    #run_query()
    root = tk.Tk()
    root.title("MySQL Query Executor")

    # Set the window size
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)

    root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    # Load the background image
    bg_image = Image.open("R.jpg")  # Replace "background_image.jpg" with your image file
    bg_image = bg_image.resize((window_width, window_height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to set the background image
    background_label = tk.Label(root, image=bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    options = ['Directed by Joe Johnston', \
               'Produced by Terrence Malick and distributed by Distributor Warner Bros.', \
               'Warner Bros Artists',\
               'Distributors who have distributed more than 1 film',\
               'Producers who have distributed a movie for Sony Pictures artists',\
               'Distributed more than 1 film and has worked with Morgan Lily or Will smith',\
               'Average age of actors in movies released after 2000',\
               'Actors with age more than the average age of actors in movies released after 2000',\
               'Both Actors and Directors have won awards', \
               'More than 2 Producers',\
               'Have directors that have won academy awards',\
               'Distributors with highest number of PG films',\
               'Distributors with least number of PG films',\
               'Distributors with PG films higher than Distributors with least number of PG films',\
               'oldest actor to receive an award in movies released in the 20th century']  # Add more query options as needed
    dropdown = tk.StringVar(root)
    dropdown.set(options[0])  # Set default value for dropdown

    dropdown_menu = tk.OptionMenu(root, dropdown, *options)
    dropdown_menu.pack(pady=20)

    # Button to execute the selected query
    execute_button = tk.Button(root, text="Execute Query", command=execute_query)
    execute_button.pack(pady=40)

    # Text widget to display query results
    output_text = tk.Text(root, height=30, width=80, wrap=tk.NONE, bg='white', fg='black', font=('Arial', 10))
    output_text.place(relx=0.5, rely=0.5, anchor='center')  # Position the Text widget in the center

    output_text_2 = tk.Text(root, height=3, width=30, wrap=tk.NONE, bg='red', fg='black', font=('Arial', 20))
    output_text_2.place(x=20, y=150, anchor='sw')  # Position the Text widget in the center

    # Display text in the Text widget
    output_text_2.insert(tk.END, "Movie DataBase ...........\nPick an option from the dropdown\n")

    root.mainloop()

