package ro.mpp2024.controllers;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.stage.Stage;
import ro.mpp2024.Zboruri;
import ro.mpp2024.domain.Angajat;
import ro.mpp2024.services.ZboruriException;
import ro.mpp2024.services.ZboruriServices;

import java.io.IOException;

public class LoginController {

    @FXML
    private PasswordField passwordFieldLogin;
    @FXML
    private TextField usernameFieldLogin;
    private ZboruriServices server;
    private Stage stage;

    public void setServer(ZboruriServices server, Stage stage) {
        this.server = server;
        this.stage = stage;
    }

    @FXML
    private void handleLogin() throws IOException {
        String password = passwordFieldLogin.getText();
        String username = usernameFieldLogin.getText();
        Angajat angajat = new Angajat(username, password);

        try {
            showAngajatDialog(angajat);
        } catch (ZboruriException e) {
            MessageAlert.showMessage(null, Alert.AlertType.ERROR, "Error", e.getMessage());
            passwordFieldLogin.clear();
        }
    }

    private void showAngajatDialog(Angajat angajat) throws IOException, ZboruriException {
        FXMLLoader loader = new FXMLLoader(Zboruri.class.getResource("angajat-view.fxml"));
        Stage newStage = new Stage();
        newStage.setScene(new Scene(loader.load()));
        newStage.setTitle("Zboruri");

        AngajatController controller = loader.getController();
        server.login(angajat, controller);
        controller.setServer(server, angajat, newStage);

        newStage.setOnCloseRequest(event -> {
            controller.logout();
            System.exit(0);
        });

        newStage.show();
        this.stage.close();
    }

    @FXML
    private void setOnKeyPressedPasswordLogin(KeyEvent keyEvent) throws IOException {
        if (keyEvent.getCode().equals(KeyCode.ENTER)) {
            handleLogin();
        } else if(keyEvent.getCode().equals(KeyCode.UP)){
            usernameFieldLogin.requestFocus();
        }
    }

    @FXML
    private void setOnKeyPressedUsernameLogin(KeyEvent keyEvent) throws IOException {
        if(keyEvent.getCode().equals(KeyCode.DOWN)){
            passwordFieldLogin.requestFocus();
        } else if (keyEvent.getCode().equals(KeyCode.ENTER)) {
            handleLogin();
        }
    }

    @FXML
    private void handleExit() {
        this.stage.close();
    }
}
