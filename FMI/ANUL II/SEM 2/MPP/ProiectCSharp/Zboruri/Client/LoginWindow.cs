using Gtk;
using Services;

namespace Client;

public class LoginWindow : Window
{
    private readonly ClientCtrl _clientCtrl;
    readonly Entry _usernameEntry = new Entry();
    readonly Entry _passwordEntry = new Entry();
    readonly Button _exitButton = new Button("Exit");
    readonly Button _loginButton = new Button("Login");

    public LoginWindow(ClientCtrl clientCtrl) : base("Login")
    {
        this._clientCtrl = clientCtrl;
        BuildWindow();
    }

    private void BuildWindow()
    {
        SetDefaultSize(300, 200);
        DeleteEvent += HandleExit;

        VBox vbox = new VBox(false, 10);

        HBox usernameBox = new HBox(false, 5);
        usernameBox.PackStart(new Label("Username: "), false, false, 0);
        usernameBox.PackStart(_usernameEntry, true, true, 0);
        vbox.PackStart(usernameBox, false, false, 0);

        HBox passwordBox = new HBox(false, 5);
        passwordBox.PackStart(new Label("Password: "), false, false, 0);
        _passwordEntry.Visibility = false;
        passwordBox.PackStart(_passwordEntry, true, true, 0);
        vbox.PackStart(passwordBox, false, false, 0);

        HBox buttonBox = new HBox(false, 10);
        _exitButton.Clicked += HandleExit;
        buttonBox.PackStart(_exitButton, true, true, 0);
        _loginButton.Clicked += HandleLogin;
        buttonBox.PackEnd(_loginButton, true, true, 0);
        vbox.PackEnd(buttonBox, false, false, 0);

        Add(vbox);
    }

    private void HandleLogin(object? sender, EventArgs e)
    {
        Console.WriteLine("S-a apasat login");
        Console.WriteLine("Username {0} - Password - {1}", _usernameEntry.Text, _passwordEntry.Text);
        string username = _usernameEntry.Text;
        string password = _passwordEntry.Text;
        try
        {
            _clientCtrl.Login(username, password);
            ZboruriWindow angajatView = new ZboruriWindow(_clientCtrl, "Zboruri");
            angajatView.ShowAll();
            Dispose();
        }
        catch (ZboruriException ex)
        {
            MessageAlert.ShowErrorMessage(ex.Message);
            _passwordEntry.Text = "";
        }
    }

    private void HandleExit(object? sender, EventArgs e)
    {
        Application.Quit();
    }
}