package ro.mpp2024;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import ro.mpp2024.Car;
import ro.mpp2024.CarRepository;
import ro.mpp2024.JdbcUtils;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class CarsDBRepository implements CarRepository {

    private JdbcUtils dbUtils;



    private static final Logger logger= LogManager.getLogger();

    public CarsDBRepository(Properties props) {
        logger.info("Initializing CarsDBRepository with properties: {} ",props);
        dbUtils=new JdbcUtils(props);
    }

    @Override
    public List<Car> findByManufacturer(String manufacturerN) {
        logger.traceEntry();
        List<Car> cars = new ArrayList<>();
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from cars where manufacturer = ?"))
        {
            preparedStatement.setString(1, manufacturerN);
            try (ResultSet resultSet = preparedStatement.executeQuery())
            {
                while (resultSet.next()){
                    int id = resultSet.getInt("id");
                    String manufacturer = resultSet.getString("manufacturer");
                    String model = resultSet.getString("model");
                    int year = resultSet.getInt("year");
                    Car car = new Car(manufacturer, model, year);
                    car.setId(id);
                    cars.add(car);
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
        return cars;
    }

    @Override
    public List<Car> findBetweenYears(int min, int max) {
        logger.traceEntry();
        List<Car> cars = new ArrayList<>();
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from cars where year > ? and year < ?"))
        {
            preparedStatement.setInt(1, min);
            preparedStatement.setInt(2, max);
            try (ResultSet resultSet = preparedStatement.executeQuery())
            {
                while (resultSet.next()){
                    int id = resultSet.getInt("id");
                    String manufacturer = resultSet.getString("manufacturer");
                    String model = resultSet.getString("model");
                    int year = resultSet.getInt("year");
                    Car car = new Car(manufacturer, model, year);
                    car.setId(id);
                    cars.add(car);
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
        return cars;
    }

    @Override
    public void add(Car elem) {
        logger.traceEntry("saving task {}", elem);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("insert into cars (manufacturer, model, year)  values (?, ?, ?)"))
        {
            preparedStatement.setString(1, elem.getManufacturer());
            preparedStatement.setString(2, elem.getModel());
            preparedStatement.setInt(3, elem.getYear());
            int result = preparedStatement.executeUpdate();
            logger.trace("Saved {} instances", result);
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    @Override
    public void update(Integer integer, Car elem) {
        logger.traceEntry("update task {}", elem);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("update cars set manufacturer=?, model=?, year=? where id=?"))
        {
            preparedStatement.setString(1, elem.getManufacturer());
            preparedStatement.setString(2, elem.getModel());
            preparedStatement.setInt(3, elem.getYear());
            preparedStatement.setInt(4, integer);
            int result = preparedStatement.executeUpdate();
            logger.trace("Updated {} instances", result);
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    @Override
    public Iterable<Car> findAll() {
        logger.traceEntry();
        List<Car> cars = new ArrayList<>();
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from cars"))
        {
            try (ResultSet resultSet = preparedStatement.executeQuery())
            {
                while (resultSet.next()){
                    int id = resultSet.getInt("id");
                    String manufacturer = resultSet.getString("manufacturer");
                    String model = resultSet.getString("model");
                    int year = resultSet.getInt("year");
                    Car car = new Car(manufacturer, model, year);
                    car.setId(id);
                    cars.add(car);
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
        return cars;
    }
}
