package ro.mpp2024.repository;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import ro.mpp2024.domain.Angajat;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Properties;

public class AngajatiDBRepository implements AngajatiRepository {
    private final JdbcUtils dbUtils;
    private static final Logger logger = LogManager.getLogger();

    public AngajatiDBRepository(Properties props) {
        logger.info("Initializing AngajatiDBRepository with properties: {} ", props);
        dbUtils = new JdbcUtils(props);
    }

    @Override
    public int size() {
        return 0;
    }

    @Override
    public Angajat findOne(String s) {
        return null;
    }

    @Override
    public Iterable<Angajat> findAll() {
        return null;
    }

    @Override
    public void save(Angajat entity) {
    }

    @Override
    public void delete(String s) {
    }

    @Override
    public void update(String id, Angajat entity) {
    }

    @Override
    public Angajat findByUsernameAndPass(String username, String password) {
        logger.traceEntry("finding angajat with username {}", username);
        Connection connection = dbUtils.getConnection();
        try (PreparedStatement preparedStatement = connection.prepareStatement("select * from angajati where username = ? and parola = ?")) {
            preparedStatement.setString(1, username);
            preparedStatement.setString(2, password);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                if (resultSet.next()) {
                    String nume = resultSet.getString("nume");
                    Angajat angajat = new Angajat(username, nume, password);
                    angajat.setId(username);
                    logger.traceExit();
                    return angajat;
                }
            }
        } catch (SQLException e) {
            logger.error(e);
            System.err.println("Error DB: " + e);
        }
        logger.traceExit("No angajat found with username {}", username);
        return null;
    }
}
