using Gtk;
using Model;
using Services;
using Window = Gtk.Window;

namespace Client
{
    public class ValidatorWindow : Window
    {
        private readonly ClientCtrl _clientCtrl;
        private readonly Entry _nameEntry = new() { PlaceholderText = "Name" };
        private readonly Entry _descriptionEntry = new() {PlaceholderText = "Description"};
        private readonly ComboBoxText _severityComboBox = new();
        private readonly Button _exitButton = new("Exit");
        private readonly Button _reportButton = new("Report a bug");
        private readonly Button _modifyButton = new("Modify bug");
        private readonly TreeView _bugsTable = new();
        private readonly ListStore _modelBugs = new(typeof(string), typeof(string), typeof(string), typeof(string), typeof(int));

        public ValidatorWindow(ClientCtrl clientCtrl, string title) : base(title)
        {
            this._clientCtrl = clientCtrl;
            BuildWindow();
        }

        private void BuildWindow()
        {
            SetDefaultSize(800, 400);
            DeleteEvent += HandleExit;
            var vbox = new VBox(false, 10);

            // Add a label at the top
            var label = new Label("Bugs");
            var fontDescription = Pango.FontDescription.FromString("Arial 32");
            label.ModifyFont(fontDescription);
            vbox.PackStart(label, false, false, 0);

            // Add a table with the fields: Name, Description, Severity, Status
            vbox.PackStart(_bugsTable, true, true, 0);
            BuildBugsTable();

            // Add textfields for Name, Description and a combobox for Severity
            var entryBox = new HBox(true, 10);
            entryBox.PackStart(_nameEntry, false, false, 0);
            entryBox.PackStart(_descriptionEntry, false, false, 0);
            entryBox.PackStart(_severityComboBox, false, false, 0);
            InitComboBox();

            vbox.PackStart(entryBox, false, false, 0);
            // Add buttons for Exit, Report a bug, Modify a bug
            var buttonBox = new HBox(false, 10);
            _exitButton.Clicked += HandleExit;
            _reportButton.Clicked += HandleReport;
            _modifyButton.Clicked += HandleModify;
            buttonBox.PackStart(_exitButton, true, true, 0);
            buttonBox.PackStart(_reportButton, true, true, 0);
            buttonBox.PackEnd(_modifyButton, true, true, 0);
            vbox.PackEnd(buttonBox, false, false, 0);

            Add(vbox);
            _clientCtrl.UpdateEvent += ValidatorUpdate;
        }

        private void InitComboBox()
        {
            var listStore = new ListStore(typeof(string));
            listStore.AppendValues("Severity");
            _severityComboBox.Model = listStore;

            foreach (var severity in Enum.GetValues(typeof(Severity)))
            { 
                listStore.AppendValues(severity.ToString());
            }

            _severityComboBox.Active = 0;
        }

        private void UpdateBugsTable()
        {
            _modelBugs.Clear();
            foreach (var bug in _clientCtrl.GetAllBugs())
            {
                _modelBugs.AppendValues(bug.Name, bug.Description, bug.Severity.ToString(), bug.Status, bug.Id);
            }
        }

        private void BuildBugsTable()
        {

            _bugsTable.Model = _modelBugs;

            var nameColumn = new TreeViewColumn("Name", new CellRendererText(), "text", 0);
            nameColumn.Expand = true;
            _bugsTable.AppendColumn(nameColumn);
            
            var descriptionColumn = new TreeViewColumn("Description", new CellRendererText(), "text", 1);
            descriptionColumn.Expand = true;
            _bugsTable.AppendColumn(descriptionColumn);

            var severityColumn = new TreeViewColumn("Severity", new CellRendererText(), "text", 2);
            severityColumn.Expand = true;
            _bugsTable.AppendColumn(severityColumn);
            
            var statusColumn = new TreeViewColumn("Status", new CellRendererText(), "text", 3);
            statusColumn.Expand = true;
            _bugsTable.AppendColumn(statusColumn);

            _bugsTable.RowActivated += OnRowActivated;
            UpdateBugsTable();
        }
        
        private void OnRowActivated(object o, RowActivatedArgs args)
        {
            if (!_bugsTable.Selection.GetSelected(out var model, out var iter)) return;
            string name = model.GetValue(iter, 0).ToString();
            string description = model.GetValue(iter, 1).ToString();
            string severity = model.GetValue(iter, 2).ToString();
                
            _nameEntry.Text = name;
            _descriptionEntry.Text = description;
            _severityComboBox.Active = _severityComboBox.Model.IterNChildren() > 0 ? Array.IndexOf(Enum.GetValues(typeof(Severity)), Enum.Parse(typeof(Severity), severity)) + 1 : 0;
        }

        private void HandleExit(object? sender, EventArgs e)
        {
            _clientCtrl.Logout();
            _clientCtrl.UpdateEvent -= ValidatorUpdate;
            var loginWindow = new LoginWindow(_clientCtrl);
            loginWindow.ShowAll();
            Dispose();
        }

        private void HandleReport(object? sender, EventArgs e)
        {
            string name = _nameEntry.Text;
            string description = _descriptionEntry.Text;
            string severity = _severityComboBox.ActiveText;
            try
            {
                _clientCtrl.ReportBug(name, description, severity);
                _nameEntry.Text = "";
                _descriptionEntry.Text = "";
                _severityComboBox.Active = 0;
            }
            catch (BmsException exception)
            {
                MessageAlert.ShowErrorMessage(exception.Message);
            }
        }

        private void HandleModify(object? sender, EventArgs e)
        {
            
            if (_bugsTable.Selection.GetSelected(out var model, out var iter))
            {
                string name = _nameEntry.Text;
                string description = _descriptionEntry.Text;
                string severity = _severityComboBox.ActiveText;
                string status = model.GetValue(iter, 3).ToString();
                int id = (int) model.GetValue(iter, 4);
                try
                {
                    _clientCtrl.ModifyBug(id, name, description, severity, status);
                }
                catch (BmsException exception)
                {
                    MessageAlert.ShowErrorMessage(exception.Message);
                }
            }
        }

        private void ValidatorUpdate(object? sender, BmsEventArgs e)
        {
            switch (e.AngajatEventType)
            {
                case BmsEvent.BugReported:
                    var bug = (Bug)e.Data;
                    Application.Invoke(delegate
                    {
                        _modelBugs.AppendValues(bug.Name, bug.Description, bug.Severity.ToString(), bug.Status, bug.Id);
                    });
                    break;
                case BmsEvent.BugUpdated:
                    bug = (Bug)e.Data;
                    _modelBugs.GetIterFirst(out var it);
                    for (int i = 0; i < _modelBugs.IterNChildren(); i++)
                    {
                        int value = (int)_modelBugs.GetValue(it, 4);
                        if (value == bug.Id)
                            break;
                        _modelBugs.IterNext(ref it);
                    }
                    Application.Invoke(delegate
                    {
                        _modelBugs.Remove(ref it);
                        _modelBugs.AppendValues(bug.Name, bug.Description, bug.Severity.ToString(), bug.Status, bug.Id);
                    });
                    break;
                case BmsEvent.BugFixed:
                    bug = (Bug)e.Data;
                    _modelBugs.GetIterFirst(out it);
                    for (int i = 0; i < _modelBugs.IterNChildren(); i++)
                    {
                        int value = (int)_modelBugs.GetValue(it, 4);
                        if (value == bug.Id)
                            break;
                        _modelBugs.IterNext(ref it);
                    }
                    Application.Invoke(delegate { _modelBugs.Remove(ref it); });
                    break;
            }
        }
    }
}