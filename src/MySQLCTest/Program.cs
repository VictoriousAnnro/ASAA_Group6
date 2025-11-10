// in terminal
// dotnet new console -n MySQLCTest

/* You must install
- MySQL
- MySQL .NET Connector
*/
using MySql.Data.MySqlClient;

/*
Web service needs to query existing cars,
query options for components,
save the order to db
*/

class Program
{
    static void Main()
    {
        string connectionString = "";
        MySqlConnection connection = new MySqlConnection(connectionString);

        try
        {
            connection.Open();
            Console.WriteLine("Connected to database");
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error with database: {e.Message}");
        }
    }
}

Console.WriteLine("Hello, World!");
