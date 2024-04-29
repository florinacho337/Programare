package ro.mpp2024.repository;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.utils.Constants;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class ZboruriDBRepository implements ZboruriRepository {
    private final JdbcUtils dbUtils;
    private static final Logger logger = LogManager.getLogger();

    public ZboruriDBRepository(Properties props) {
        logger.info("Initializing ZboruriDBRepository with properties: {} ", props);
        dbUtils = new JdbcUtils(props);
    }

    @Override
    public int size() {
        return 0;
    }

    @Override
    public Zbor findOne(Integer integer) {
        logger.traceEntry("finding zbor with id {}", integer);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from zboruri where id = ?")) {
            preparedStatement.setInt(1, integer);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                if (resultSet.next()) {
                    Zbor zbor = createZbor(resultSet);
                    logger.traceExit();
                    return zbor;
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit("No zbor found with id {}", integer);
        return null;
    }

    private Zbor createZbor(ResultSet resultSet) throws SQLException {
        Integer id = resultSet.getInt("id");
        String destinatie = resultSet.getString("destinatie");
        LocalDateTime plecare = LocalDateTime.parse(resultSet.getString("plecare"), Constants.DATE_TIME_FORMATTER);
        String aeroport = resultSet.getString("aeroport");
        int nrLocuri = resultSet.getInt("nr_locuri");
        Zbor zbor = new Zbor(aeroport, destinatie, plecare, nrLocuri);
        zbor.setId(id);
        return zbor;
    }

    @Override
    public Iterable<Zbor> findAll() {
        logger.traceEntry();
        List<Zbor> zboruri = new ArrayList<>();
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from zboruri where nr_locuri > 0")) {
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    Zbor zbor = createZbor(resultSet);
                    zboruri.add(zbor);
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
        return zboruri;
    }

    @Override
    public void save(Zbor entity) {
    }

    @Override
    public void delete(Integer integer) {
    }

    @Override
    public void update(Integer integer, Zbor entity) {
        logger.traceEntry("updating zbor with id {}", integer);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("update zboruri set destinatie=?, plecare=?, aeroport=?, nr_locuri=? where id=?")) {
            preparedStatement.setString(1, entity.getDestinatie());
            preparedStatement.setString(2, entity.getPlecare().format(Constants.DATE_TIME_FORMATTER));
            preparedStatement.setString(3, entity.getAeroport());
            preparedStatement.setInt(4, entity.getNrLocuri());
            preparedStatement.setInt(5, integer);
            int result = preparedStatement.executeUpdate();
            logger.trace("Updated {} instances", result);
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    @Override
    public List<Zbor> findAllByDestDateAndMinimumSeats(String destination, LocalDateTime date, int min) {
        logger.traceEntry();
        List<Zbor> zboruri = new ArrayList<>();
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from zboruri where destinatie = ? and plecare like ? || '%' and nr_locuri >= ?")) {
            preparedStatement.setString(1, destination);
            preparedStatement.setString(2, date.format(Constants.DATE_FORMATTER));
            preparedStatement.setInt(3, min);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    Zbor zbor = createZbor(resultSet);
                    zboruri.add(zbor);
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
        return zboruri;
    }
}
