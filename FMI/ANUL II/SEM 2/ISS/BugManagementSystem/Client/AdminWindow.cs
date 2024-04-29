using Gtk;
using Model;
using Services;
using Window = Gtk.Window;

namespace Client
{
    public class AdminWindow : Window
    {
        private readonly ClientCtrl _clientCtrl;
        private readonly Entry _usernameEntry = new Entry { PlaceholderText = "Username" };
        private readonly Entry _nameEntry = new Entry { PlaceholderText = "Name" };
        private readonly Entry _passwordEntry = new Entry { PlaceholderText = "Password" };
        private readonly ComboBoxText _roleComboBox = new ComboBoxText();
        private readonly Button _exitButton = new Button("Exit");
        private readonly Button _addButton = new Button("Add Employee");
        private readonly Button _removeButton = new Button("Remove Employee");
        private readonly TreeView _employeeTable = new TreeView();
        private readonly ListStore _modelEmployees = new ListStore(typeof(string), typeof(string), typeof(string), typeof(string));

        public AdminWindow(ClientCtrl clientCtrl) : base("Administration")
        {
            this._clientCtrl = clientCtrl;
            BuildWindow();
        }

        private void BuildWindow()
        {
            SetDefaultSize(800, 400);
            DeleteEvent += HandleExit;
            VBox vbox = new VBox(false, 10);

            // Add a label at the top
            Label label = new Label("Employees");
            var fontDescription = Pango.FontDescription.FromString("Arial 32");
            label.ModifyFont(fontDescription);
            vbox.PackStart(label, false, false, 0);

            // Add a table with the fields: Username, Name, Password, Role
            vbox.PackStart(_employeeTable, true, true, 0);
            BuildEmployeeTable();

            // Add textfields for Username, Name, Password and a combobox for Role
            HBox entryBox = new HBox(true, 10);
            entryBox.PackStart(_usernameEntry, false, false, 0);
            entryBox.PackStart(_nameEntry, false, false, 0);
            entryBox.PackStart(_passwordEntry, false, false, 0);
            entryBox.PackStart(_roleComboBox, false, false, 0);
            InitComboBox();

            vbox.PackStart(entryBox, false, false, 0);
            // Add buttons for Exit, Add Employee, Remove Employee
            HBox buttonBox = new HBox(false, 10);
            _exitButton.Clicked += HandleExit;
            _addButton.Clicked += HandleAdd;
            _removeButton.Clicked += HandleRemove;
            buttonBox.PackStart(_exitButton, true, true, 0);
            buttonBox.PackStart(_addButton, true, true, 0);
            buttonBox.PackEnd(_removeButton, true, true, 0);
            vbox.PackEnd(buttonBox, false, false, 0);

            Add(vbox);
            _clientCtrl.UpdateEvent += AdminUpdate;
        }

        private void InitComboBox()
        {
            ListStore listStore = new ListStore(typeof(string));
            listStore.AppendValues("Role");
            _roleComboBox.Model = listStore;

            foreach (Role role in Enum.GetValues(typeof(Role)))
            {
                if (role != Model.Role.Admin)
                {
                    listStore.AppendValues(role.ToString());
                }
            }

            _roleComboBox.Active = 0;
        }

        private void UpdateEmployeeTable()
        {
            _modelEmployees.Clear();
            foreach (var emp in _clientCtrl.GetAllEmployees())
            {
                _modelEmployees.AppendValues(emp.Username, emp.Name, emp.Password, emp.Role.ToString());
            }
        }

        private void BuildEmployeeTable()
        {

            _employeeTable.Model = _modelEmployees;

            TreeViewColumn usernameColumn = new TreeViewColumn("Username", new CellRendererText(), "text", 0);
            usernameColumn.Expand = true;
            _employeeTable.AppendColumn(usernameColumn);

            TreeViewColumn nameColumn = new TreeViewColumn("Name", new CellRendererText(), "text", 1);
            nameColumn.Expand = true;
            _employeeTable.AppendColumn(nameColumn);

            TreeViewColumn passwordColumn = new TreeViewColumn("Password", new CellRendererText(), "text", 2);
            passwordColumn.Expand = true;
            _employeeTable.AppendColumn(passwordColumn);

            TreeViewColumn roleColumn = new TreeViewColumn("Role", new CellRendererText(), "text", 3);
            roleColumn.Expand = true;
            _employeeTable.AppendColumn(roleColumn);

            UpdateEmployeeTable();
        }

        private void HandleExit(object? sender, EventArgs e)
        {
            _clientCtrl.UpdateEvent -= AdminUpdate;
            _clientCtrl.Close();
            Application.Quit();
            Dispose();
        }

        private void HandleAdd(object? sender, EventArgs e)
        {
            string username = _usernameEntry.Text;
            string name = _nameEntry.Text;
            string password = _passwordEntry.Text;
            string role = _roleComboBox.ActiveText;
            try
            {
                _clientCtrl.AddEmployee(username, name, password, role);
            }
            catch (BmsException exception)
            {
                MessageAlert.ShowErrorMessage(exception.Message);
            }
        }

        private void HandleRemove(object? sender, EventArgs e)
        {
            
            if (_employeeTable.Selection.GetSelected(out var model, out var iter))
            {
                string username = model.GetValue(iter, 0).ToString();
                try
                {
                    _clientCtrl.RemoveEmployee(username);
                    MessageAlert.ShowMessage("Employee removed successfully!");
                }
                catch (BmsException exception)
                {
                    MessageAlert.ShowErrorMessage(exception.Message);
                }
            }
        }

        private void AdminUpdate(object? sender, BmsEventArgs e)
        {
            switch (e.AngajatEventType)
            {
                case BmsEvent.EmployeeAdded:
                {
                    var employee = (Employee)e.Data;
                    _modelEmployees.AppendValues(employee.Username, employee.Name, employee.Password,
                        employee.Role.ToString());
                    break;
                }
                case BmsEvent.EmployeeRemoved:
                {
                    var username = (string)e.Data;
                    if (!_modelEmployees.GetIterFirst(out var iter)) return;
                    do
                    {
                        if (_modelEmployees.GetValue(iter, 0).ToString() != username) continue;
                        _modelEmployees.Remove(ref iter);
                        break;
                    } while (_modelEmployees.IterNext(ref iter));

                    break;
                }
            }
        }
    }
}