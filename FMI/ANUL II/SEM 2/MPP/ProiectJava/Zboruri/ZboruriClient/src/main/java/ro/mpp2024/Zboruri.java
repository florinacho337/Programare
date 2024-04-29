package ro.mpp2024;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;
import ro.mpp2024.controllers.LoginController;
import ro.mpp2024.network.jsonprotocol.ZboruriServicesJsonProxy;
import ro.mpp2024.services.ZboruriServices;

import java.io.IOException;
import java.util.Properties;

public class Zboruri extends Application {
    private ZboruriServices server;

    @Override
    public void start(Stage stage) throws IOException {
        System.out.println("In start");
        Properties angajatProps = new Properties();
        try {
            angajatProps.load(Zboruri.class.getResourceAsStream("/zboruriclient.properties"));
            System.out.println("Angajat properties set. ");
            angajatProps.list(System.out);
        } catch (IOException e) {
            System.err.println("Cannot find zboruriclient.properties " + e);
            return;
        }
        String defaultServer = "localhost";
        String serverIP = angajatProps.getProperty("zboruri.server.host", defaultServer);
        int defaultAngajatPort = 55555;
        int serverPort = defaultAngajatPort;

        try {
            serverPort = Integer.parseInt(angajatProps.getProperty("zboruri.server.port"));
        } catch (NumberFormatException ex) {
            System.err.println("Wrong port number " + ex.getMessage());
            System.out.println("Using default port: " + defaultAngajatPort);
        }
        System.out.println("Using server IP " + serverIP);
        System.out.println("Using server port " + serverPort);

        server = new ZboruriServicesJsonProxy(serverIP, serverPort);
        initView(stage);
        stage.show();
    }

    private void initView(Stage primaryStage) throws IOException {

        FXMLLoader loginLoader = new FXMLLoader(Zboruri.class.getResource("login-view.fxml"));
        primaryStage.setScene(new Scene(loginLoader.load()));
        primaryStage.setTitle("Login");

        LoginController loginController = loginLoader.getController();
        loginController.setServer(server, primaryStage);

    }

    public static void main(String[] args) {
        Application.launch();
    }
}