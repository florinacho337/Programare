using System.Globalization;
using Gtk;
using Model;
using Services;
using Calendar = Gtk.Calendar;

namespace Client;

public class ZboruriWindow : Window
{
    private readonly ClientCtrl _clientCtrl;
    private readonly TreeView _mainTableView = new TreeView();
    private readonly TreeView _secondTableView = new TreeView();
    private readonly Button _searchButton = new Button("Search");
    private readonly Button _buyTicketsButton = new Button("Buy Tickets");
    private readonly Button _logoutButton = new Button("Logout");
    private readonly Entry _destinationEntry = new Entry();
    private readonly Entry _clientEntry = new Entry();
    private readonly Entry _cityEntry = new Entry();
    private readonly Entry _countryEntry = new Entry();
    private readonly Entry _seatsEntry = new Entry();
    private readonly Entry _touristsEntry = new Entry();
    private readonly Calendar _calendar = new Calendar();
    private readonly ListStore _mainListStore =
        new ListStore(typeof(string), typeof(string), typeof(string), typeof(int), typeof(int));
    private readonly ListStore _secondListStore = new ListStore(typeof(string), typeof(string), typeof(string), typeof(int), typeof(int));
    private string _destination;
    private DateTime _date;

    public ZboruriWindow(ClientCtrl ctrl, string title) : base(title)
    {
        this._clientCtrl = ctrl;
        BuildWindow();
    }

    private void BuildWindow()
    {
        SetDefaultSize(1000, 600);
        DeleteEvent += CloseWindow;

        CreateMainTableView();
        ScrolledWindow mainTableScrolled = new ScrolledWindow();
        mainTableScrolled.Add(_mainTableView);

        CreateSecondTableView();
        ScrolledWindow secondTableScrolled = new ScrolledWindow();
        secondTableScrolled.Add(_secondTableView);
        
        _calendar.Date = DateTime.Now;
        _searchButton.Clicked += HandleSearch;

        Entry touristsEntry = new Entry();
        touristsEntry.WidthChars = 40;
        touristsEntry.PlaceholderText = "Introduceti turistii separati prin \";\".";
        
        Entry seatsEntry = new Entry();
        seatsEntry.Changed += SeatsEntryOnChanged;

        _logoutButton.Clicked += HandleLogout;
        _buyTicketsButton.Clicked += HandleBuyTicket;

        HBox searchFields = new HBox(false, 10);
        searchFields.PackStart(new Label("Date: "), false, false, 0);
        searchFields.PackStart(_calendar, false, false, 0);
        searchFields.PackStart(new Label("Destination: "), false, false, 0);
        searchFields.PackStart(_destinationEntry, false, false, 0);

        VBox searchBox = new VBox(false, 10);
        searchBox.PackStart(searchFields, false, false, 0);
        searchBox.PackEnd(_searchButton, false, false, 0);
        
        VBox formBox = new VBox(false, 10);
        formBox.PackStart(searchBox, false, false, 0);
        formBox.PackEnd(_buyTicketsButton, false, false, 0);
        formBox.PackEnd(_touristsEntry, false, false, 0);
        formBox.PackEnd(new Label("Tourists: "), false, false, 0);
        formBox.PackEnd(_seatsEntry, false, false, 0);
        formBox.PackEnd(new Label("Seats: "), false, false, 0);
        formBox.PackEnd(_countryEntry, false, false, 0);
        formBox.PackEnd(new Label("Country: "), false, false, 0);
        formBox.PackEnd(_cityEntry, false, false, 0);
        formBox.PackEnd(new Label("City: "), false, false, 0);
        formBox.PackEnd(_clientEntry, false, false, 0);
        formBox.PackEnd(new Label("Client: "), false, false, 0);

        VBox leftBox = new VBox(false, 10);
        leftBox.PackStart(mainTableScrolled, true, true, 0);
        leftBox.PackStart(secondTableScrolled, true, true, 0);
        leftBox.PackEnd(_logoutButton, false, false, 0);

        HBox mainBox = new HBox(false, 10);
        mainBox.PackStart(leftBox, true, true, 0);
        mainBox.PackEnd(formBox, false, false, 0);

        Add(mainBox);

        _clientCtrl.updateEvent += AngajatUpdate;
    }

    private void HandleBuyTicket(object? sender, EventArgs e)
    {
        if (String.IsNullOrWhiteSpace(_clientEntry.Text) || String.IsNullOrWhiteSpace(_seatsEntry.Text) ||
                String.IsNullOrWhiteSpace(_cityEntry.Text) || String.IsNullOrWhiteSpace(_countryEntry.Text))
            {
                MessageAlert.ShowErrorMessage("Nu ati completat datele clientului si turistii!");
                return;
            }

            string client = _clientEntry.Text;
            string city = _cityEntry.Text;
            string country = _countryEntry.Text;
            if (!int.TryParse(_seatsEntry.Text, out int seats))
            {
                MessageAlert.ShowErrorMessage("Numarul de locuri este invalid!");
                return;
            }
            List<TuristBilet> turisti = _touristsEntry.Text.Split(';')
                .Select(s => s.Trim())
                .Where(s => !string.IsNullOrWhiteSpace(s))
                .Select(t => new TuristBilet {Turist = t})
                .ToList();
            
            turisti.Add(new TuristBilet {Turist = client});
            if (turisti.Count != seats)
            {
                MessageAlert.ShowErrorMessage("Numarul de locuri nu corespunde cu numarul turistilor!");
                return;
            }
            
            if (_secondTableView.Selection.GetSelected(out ITreeModel model, out TreeIter iter))
            {
                Zbor zbor = _clientCtrl.FindZbor((int)model.GetValue(iter, 4));
                if (zbor.NrLocuri < seats)
                {
                    MessageAlert.ShowErrorMessage("Zborul nu are destule locuri disponibile!");
                    return;
                }

                try
                {
                    this._clientCtrl.CumparaBilet(client, city, country, turisti, seats, zbor);
                    MessageAlert.ShowMessage("Bilet cumparat cu succes!");
                    _clientEntry.Text = "";
                    _cityEntry.Text = "";
                    _countryEntry.Text = "";
                    _seatsEntry.Text = "";
                    _touristsEntry.Text = "";
                } catch (ZboruriException ex)
                {
                    MessageAlert.ShowErrorMessage(ex.Message);
                }
            }
            else
                MessageAlert.ShowErrorMessage("Nu ati selectat nici un zbor!");
    }

    private void SeatsEntryOnChanged(object? sender, EventArgs e)
    {
        if (int.TryParse(((Entry)sender).Text, out var newValue))
        {
            UpdateSearch(newValue);
        }
    }
    
    private void UpdateSearch(int min)
    {
        if (_destination == "")
            return;
            
        _secondListStore.Clear();
        foreach (var flight in _clientCtrl.FindZboruriDestDateAndMinSeats(_destination, _date, min))
        {
            _secondListStore.AppendValues(flight.Aeroport, flight.Destinatie,
                flight.Plecare.ToString("HH:mm"), flight.NrLocuri, flight.Id);
        }
    }

    private void HandleSearch(object? sender, EventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_destinationEntry.Text))
        {
            MessageAlert.ShowErrorMessage("Nu ati selectat destinatia sau data!");
            return;
        }

        _destination = _destinationEntry.Text;
        _date = _calendar.GetDate();
        _destinationEntry.Text = "";
        UpdateSearch(1);
    }

    private void HandleLogout(object? sender, EventArgs e)
    {
        Console.WriteLine("S-a apasat logout, se inchide aplicatia");
        _clientCtrl.Logout();
        _clientCtrl.updateEvent -= AngajatUpdate;
        Application.Quit();
    }

    private void CreateMainTableView()
    {
        _mainTableView.Model = _mainListStore;
            
        _mainTableView.AppendColumn("Airport", new CellRendererText(), "text", 0);
        _mainTableView.AppendColumn("Destination", new CellRendererText(), "text", 1);
        _mainTableView.AppendColumn("Departure", new CellRendererText(), "text", 2);
        _mainTableView.AppendColumn("Seats", new CellRendererText(), "text", 3);
        _mainTableView.Selection.Mode = SelectionMode.None;
            
        UpdateMainTable();
    }
    
    private void UpdateMainTable()
    {
        _mainListStore.Clear();
        foreach (var flight in _clientCtrl.FindZboruri())
        {
            _mainListStore.AppendValues(flight.Aeroport, flight.Destinatie,
                flight.Plecare.ToString(CultureInfo.InvariantCulture), flight.NrLocuri, flight.Id);
        }
    }
    
    private void CreateSecondTableView()
    {
        _secondTableView.Model = _secondListStore;
            
        _secondTableView.AppendColumn("Airport", new CellRendererText(), "text", 0);
        _secondTableView.AppendColumn("Destination", new CellRendererText(), "text", 1);
        _secondTableView.AppendColumn("Departure", new CellRendererText(), "text", 2);
        _secondTableView.AppendColumn("Seats", new CellRendererText(), "text", 3);
    }
    
    void CloseWindow(Object o, DeleteEventArgs args)
    {
        _clientCtrl.Logout();
        Console.WriteLine("Application closing");
        _clientCtrl.updateEvent -= AngajatUpdate;
        Application.Quit();
    }

    private void AngajatUpdate(object? sender, ZboruriAngajatEventArgs e)
    {
        if (e.AngajatEventType != ZboruriAngajatEvent.TicketBought) return;
        Zbor zbor = (Zbor)e.Data;
        TreeIter it1;
        _mainListStore.GetIterFirst(out it1);
        for (int i = 0; i < _mainListStore.IterNChildren(); i++)
        {
            int value = (int)_mainListStore.GetValue(it1, 4);
            Console.WriteLine("In for, am obtinut {0}",value);
            if (value == zbor.Id)
            {
                Console.WriteLine("Found zbor cu id {0}",value);
                break;
            }
                
            _mainListStore.IterNext(ref it1);
        }
        TreeIter it2;
        _secondListStore.GetIterFirst(out it2);
        for (var i = 0; i < _secondListStore.IterNChildren(); i++)
        {
            int value = (int)_secondListStore.GetValue(it2, 4);
            Console.WriteLine("In for, am obtinut {0}",value);
            if (value == zbor.Id)
            {
                Console.WriteLine("Found zbor cu id {0}",value);
                break;
            }
                
            _secondListStore.IterNext(ref it2);
        }
        Application.Invoke(delegate
        {
            _mainListStore.Remove(ref it1);
            _secondListStore.Remove(ref it2);
            if (zbor.NrLocuri <= 0) return;
            _mainListStore.AppendValues(zbor.Aeroport, zbor.Destinatie,
                zbor.Plecare.ToString(CultureInfo.InvariantCulture), zbor.NrLocuri, zbor.Id);
            if (_secondListStore.IterNChildren() != 0)
            {
                _secondListStore.AppendValues(zbor.Aeroport, zbor.Destinatie,
                    zbor.Plecare.ToString("HH:mm"), zbor.NrLocuri, zbor.Id);
            }
        });
    }
}