using System;
using System.Data.SqlClient;
using System.Threading;

namespace Deadlock
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var connectionString =
                "Data Source=DESKTOP-L25SHPO\\SQLEXPRESS;Initial Catalog=Spotify;Integrated Security=True";
            var retryCount = 0;
            var success = false;

            while (!success && retryCount < 5)
            {
                Console.WriteLine("Retry count: " + retryCount);
                var thread1 = new Thread(() =>
                {
                    using (var connection = new SqlConnection(connectionString))
                    {
                        connection.Open();

                        // using (var setDeadlockPriority = connection.CreateCommand())
                        // {
                        //     setDeadlockPriority.CommandText = "SET DEADLOCK_PRIORITY HIGH";
                        //     setDeadlockPriority.ExecuteNonQuery();
                        // }

                        using (var transaction = connection.BeginTransaction())
                        {
                            try
                            {
                                Console.WriteLine("Transaction 1 started...");
                                using (var command = connection.CreateCommand())
                                {
                                    command.Transaction = transaction;

                                    command.CommandText = "UPDATE Users SET Username='deadlock1' WHERE Uid=23";
                                    command.ExecuteNonQuery();
                                    
                                    Thread.Sleep(7000); //sleep 7 seconds

                                    command.CommandText = "UPDATE Artists SET Name='deadlock1' WHERE Aid=28";
                                    command.ExecuteNonQuery();
                                }
                                
                                transaction.Commit();
                                Console.WriteLine("Transaction 1 committed successfully!");
                                success = true;
                            }
                            catch (SqlException e)
                            {
                                if (e.Number == 1205) // Deadlock error number
                                {
                                    Console.WriteLine("Deadlock! Retrying...");
                                    transaction.Rollback();
                                    Console.WriteLine("Tran rolled back!");
                                    retryCount++;
                                }
                                else
                                {
                                    Console.WriteLine("Error! " + e.Message);
                                    transaction.Rollback();
                                    Console.WriteLine("Tran rolled back!");
                                }
                            }
                        }

                    }
                });
                
                var thread2 = new Thread(() =>
                {
                    using (var connection = new SqlConnection(connectionString))
                    {
                        connection.Open();

                        using (var transaction = connection.BeginTransaction())
                        {
                            try
                            {
                                using (var command = connection.CreateCommand())
                                {
                                    Console.WriteLine("Transaction 2 started...");
                                    command.Transaction = transaction;

                                    command.CommandText = "UPDATE Artists SET Name='deadlock2' WHERE Aid=28";
                                    command.ExecuteNonQuery();
                                    
                                    Thread.Sleep(7000); //sleep 7 seconds

                                    command.CommandText = "UPDATE Users SET Username='deadlock2' WHERE Uid=23";
                                    command.ExecuteNonQuery();
                                }
                                
                                transaction.Commit();
                                Console.WriteLine("Transaction 2 committed successfully!");
                                success = true;
                            }
                            catch (SqlException e)
                            {
                                if (e.Number == 1205) // Deadlock error number
                                {
                                    Console.WriteLine("Deadlock! Retrying...");
                                    transaction.Rollback();
                                    Console.WriteLine("Tran rolled back!");
                                    retryCount++;
                                }
                                else
                                {
                                    Console.WriteLine("Error! " + e.Message);
                                    transaction.Rollback();
                                    Console.WriteLine("Tran rolled back!");
                                }
                            }
                        }

                    }
                });
                
                thread1.Start();
                thread2.Start();
                thread1.Join();
                thread2.Join();
            }

            Console.WriteLine(retryCount >= 5 ? "Exceeded maximum retry attempts. Aborting..." : "All tran completed!");
        }
    }
}