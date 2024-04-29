package ro.mpp2024.controllers;

import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;
import ro.mpp2024.Zboruri;
import ro.mpp2024.domain.Angajat;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.network.dto.DTOUtils;
import ro.mpp2024.services.ZboruriException;
import ro.mpp2024.services.ZboruriObserver;
import ro.mpp2024.services.ZboruriServices;
import ro.mpp2024.network.dto.ZborDTO;
import ro.mpp2024.utils.Constants;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.*;

public class AngajatController implements ZboruriObserver {
    @FXML
    private TextField txtClient;
    @FXML
    private TextField txtOras;
    @FXML
    private TextField txtTara;
    @FXML
    private TextField txtLocuri;
    @FXML
    private TextArea txtTuristi;
    @FXML
    private TableView<ZborDTO> tableMain;
    @FXML
    private TableView<ZborDTO> tableCumpara;
    @FXML
    private TableColumn<ZborDTO, String> colAeroportMain;
    @FXML
    private TableColumn<ZborDTO, String> colDestMain;
    @FXML
    private TableColumn<ZborDTO, String> colDataMain;
    @FXML
    private TableColumn<ZborDTO, Integer> colLocuriMain;
    @FXML
    private TextField txtDest;
    @FXML
    private DatePicker datePickerData;
    @FXML
    private TableColumn<ZborDTO, String> colAeroport2;
    @FXML
    private TableColumn<ZborDTO, String> colDest2;
    @FXML
    private TableColumn<ZborDTO, String> colData2;
    @FXML
    private TableColumn<ZborDTO, Integer> colLocuri2;

    private final ObservableList<ZborDTO> modelMain = FXCollections.observableArrayList();
    private final ObservableList<ZborDTO> modelCauta = FXCollections.observableArrayList();
    private ZboruriServices server;
    private Angajat angajat;
    private Stage stage;
    private String destinatie;
    private LocalDateTime data;

    public void setServer(ZboruriServices service, Angajat angajat, Stage stage) {
        this.server = service;
        this.stage = stage;
        this.angajat = angajat;
        initModels();
    }

    private void initModels() {
        List<ZborDTO> zborDTOS;
        try {
            zborDTOS = server.findZboruri()
                    .stream()
                    .map(zbor -> new ZborDTO(zbor.getAeroport(), zbor.getDestinatie(), zbor.getPlecare().format(Constants.DATE_TIME_FORMATTER), zbor.getNrLocuri(), zbor.getPlecare().toLocalTime().toString(), zbor.getId())).toList();
        } catch (ZboruriException e) {
            MessageAlert.showErrorMessage(null, e.getMessage());
            return;
        }
        modelMain.setAll(zborDTOS);
    }

    @FXML
    private void initialize() {
        colAeroportMain.setCellValueFactory(new PropertyValueFactory<>("aeroport"));
        colDataMain.setCellValueFactory(new PropertyValueFactory<>("plecare"));
        colDestMain.setCellValueFactory(new PropertyValueFactory<>("destinatie"));
        colLocuriMain.setCellValueFactory(new PropertyValueFactory<>("nrLocuri"));
        tableMain.setItems(modelMain);
        colAeroport2.setCellValueFactory(new PropertyValueFactory<>("aeroport"));
        colData2.setCellValueFactory(new PropertyValueFactory<>("oraPlecare"));
        colDest2.setCellValueFactory(new PropertyValueFactory<>("destinatie"));
        colLocuri2.setCellValueFactory(new PropertyValueFactory<>("nrLocuri"));
        tableCumpara.setItems(modelCauta);
        txtLocuri.textProperty().addListener((observableValue, oldValue, newValue) -> {
            try {
                updateCautare(Integer.parseInt(newValue));
            } catch (NumberFormatException ignored) {
            }
        });
    }

    @FXML
    private void handleCauta() {
        if (txtDest.getText().isBlank() || datePickerData.getValue() == null) {
            MessageAlert.showErrorMessage(null, "Nu ati selectat destinatia sau data!");
            return;
        }

        destinatie = txtDest.getText();
        data = datePickerData.getValue().atTime(0, 0);
        txtDest.clear();
        datePickerData.setValue(null);
        updateCautare(1);
    }

    private void updateCautare(int min) {
        if (Objects.equals(destinatie, "") || data == null)
            return;
        List<ZborDTO> zborDTOS;
        try {
            zborDTOS = server.findZboruriDestDateAndMinSeats(destinatie, data, min)
                    .stream()
                    .map(zbor -> new ZborDTO(zbor.getAeroport(), zbor.getDestinatie(), zbor.getPlecare().format(Constants.DATE_TIME_FORMATTER), zbor.getNrLocuri(), zbor.getPlecare().toLocalTime().toString(), zbor.getId())).toList();
        } catch (ZboruriException e) {
            MessageAlert.showErrorMessage(null, e.getMessage());
            return;
        }
        modelCauta.setAll(zborDTOS);
    }

    @FXML
    private void handleCumpara() {
        if (txtClient.getText().isBlank() || txtLocuri.getText().isBlank() || txtOras.getText().isBlank() || txtTara.getText().isBlank()) {
            MessageAlert.showErrorMessage(null, "Nu ati completat datele clientului si turistii!");
            return;
        }
        String client = txtClient.getText();
        String oras = txtOras.getText();
        String tara = txtTara.getText();
        int nrLocuri;
        try {
            nrLocuri = Integer.parseInt(txtLocuri.getText());
        } catch (NumberFormatException e) {
            MessageAlert.showErrorMessage(null, "Numarul de locuri este invalid!");
            return;
        }
        List<String> turisti = new ArrayList<>(Arrays.asList(txtTuristi.getText().strip().split(";")));
        turisti.add(client);
        turisti.remove("");
        if (turisti.size() != nrLocuri) {
            MessageAlert.showErrorMessage(null, "Numarul de locuri nu corespunde cu numarul turistilor!");
            return;
        }
        ZborDTO zborDTO = tableCumpara.getSelectionModel().getSelectedItem();
        if (zborDTO != null) {
            if (zborDTO.getNrLocuri() < nrLocuri) {
                MessageAlert.showErrorMessage(null, "Zborul nu are destule locuri disponibile!");
                return;
            }
            Zbor zbor = DTOUtils.getFromDTO(zborDTO);
            try {
                this.server.cumparaBilet(client, oras, tara, turisti, nrLocuri, zbor);
                MessageAlert.showMessage(null, Alert.AlertType.INFORMATION, "Confirmare", "Bilet cumparat cu succes!");
                txtClient.clear();
                txtOras.clear();
                txtTara.clear();
                txtLocuri.clear();
                txtTuristi.clear();
            } catch (ZboruriException e) {
                MessageAlert.showErrorMessage(null, e.getMessage());
            }
        } else
            MessageAlert.showErrorMessage(null, "Nu ati selectat nici un zbor!");
    }

    @FXML
    public void handleLogOut() throws IOException {
        logout();
        showLogInDialog();
    }

    protected void logout() {
        try {
            server.logout(angajat, this);
        } catch (ZboruriException e) {
            System.out.println("Logout error " + e);
        }

    }

    private void showLogInDialog() throws IOException {
        FXMLLoader loader = new FXMLLoader(Zboruri.class.getResource("login-view.fxml"));
        Stage newStage = new Stage();
        newStage.setScene(new Scene(loader.load()));
        newStage.setTitle("Login");

        LoginController controller = loader.getController();
        controller.setServer(server, newStage);

        this.stage.hide();
        newStage.show();
    }

    @Override
    public void ticketBought(Zbor oldZbor, Zbor zbor) {
        Platform.runLater(() -> {
            modelMain.remove(DTOUtils.getDTO(oldZbor));
            modelMain.add(DTOUtils.getDTO(zbor));
            if (!modelCauta.isEmpty()) {
                modelCauta.remove(DTOUtils.getDTO(oldZbor));
                modelCauta.add(DTOUtils.getDTO(zbor));
            }
            tableMain.refresh();
            tableCumpara.refresh();
        });
    }
}
