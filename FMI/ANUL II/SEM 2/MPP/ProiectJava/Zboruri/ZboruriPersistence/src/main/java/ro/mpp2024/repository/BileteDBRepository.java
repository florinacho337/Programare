package ro.mpp2024.repository;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import ro.mpp2024.domain.Bilet;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Properties;

public class BileteDBRepository implements BileteRepository {
    private final JdbcUtils dbUtils;
    private final Logger logger = LogManager.getLogger();

    public BileteDBRepository(Properties props) {
        logger.info("Initializing BileteDBRepository with properties: {} ", props);
        dbUtils = new JdbcUtils(props);
    }

    @Override
    public int size() {
        return 0;
    }

    @Override
    public Bilet findOne(Integer integer) {
        return null;
    }

    @Override
    public Iterable<Bilet> findAll() {
        return null;
    }

    @Override
    public void save(Bilet entity) {
        logger.traceEntry("saving bilet {}", entity);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("insert into bilete (client, oras, tara, nr_locuri, zbor) values (?, ?, ?, ?, ?)")) {
            preparedStatement.setString(1, entity.getClient());
            preparedStatement.setString(2, entity.getOras());
            preparedStatement.setString(3, entity.getTara());
            preparedStatement.setInt(4, entity.getNrLocuri());
            preparedStatement.setInt(5, entity.getZbor().getId());
            int result = preparedStatement.executeUpdate();
            if (result != 0)
                saveTuristi(connection, entity.getTuristi());
            logger.trace("Saved {} instances", result);
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    private void saveTuristi(Connection connection, List<String> turisti) {
        logger.traceEntry("saving turisti");
        try (PreparedStatement preparedStatement = connection.prepareStatement("select max(id) as \"id\" from bilete")) {
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                if (resultSet.next())
                    turisti.forEach(turist -> saveTurist(resultSet, connection, turist));
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    private void saveTurist(ResultSet resultSet, Connection connection, String turist) {
        logger.traceEntry("saving turist {}", turist);
        try (PreparedStatement preparedStatement = connection.prepareStatement("insert into turisti_bilet (id_bilet, turist) values (?, ?)")) {
            preparedStatement.setInt(1, resultSet.getInt("id"));
            preparedStatement.setString(2, turist);
            int result = preparedStatement.executeUpdate();
            logger.trace("Saved {} instances", result);
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit();
    }

    @Override
    public void delete(Integer integer) {
    }

    @Override
    public void update(Integer integer, Bilet entity) {
    }
}
