using Gtk;
using Model;
using Services;

namespace Client;

public class ProgrammerWindow : Window
{
    private readonly ClientCtrl _clientCtrl;
        private readonly Button _exitButton = new("Exit");
        private readonly Button _fixButton = new("Fix bug");
        private readonly TreeView _bugsTable = new();
        private readonly ListStore _modelBugs = new(typeof(string), typeof(string), typeof(string), typeof(string), typeof(int));

        public ProgrammerWindow(ClientCtrl clientCtrl, string title) : base(title)
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
            
            // Add buttons for Exit, Fix bug
            var buttonBox = new HBox(false, 10);
            _exitButton.Clicked += HandleExit;
            _fixButton.Clicked += HandleFix;
            buttonBox.PackStart(_exitButton, true, true, 0);
            buttonBox.PackEnd(_fixButton, true, true, 0);
            vbox.PackEnd(buttonBox, false, false, 0);

            Add(vbox);
            _clientCtrl.UpdateEvent += ProgrammerUpdate;
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
            
            UpdateBugsTable();
        }

        private void HandleExit(object? sender, EventArgs e)
        {
            _clientCtrl.Logout();
            _clientCtrl.UpdateEvent -= ProgrammerUpdate;
            var loginWindow = new LoginWindow(_clientCtrl);
            loginWindow.ShowAll();
            Dispose();
        }

        private void HandleFix(object? sender, EventArgs e)
        {
            
            if (_bugsTable.Selection.GetSelected(out var model, out var iter))
            {
                int id = (int) model.GetValue(iter, 4);
                try
                {
                    _clientCtrl.FixBug(id);
                }
                catch (BmsException exception)
                {
                    MessageAlert.ShowErrorMessage(exception.Message);
                }
            }
        }

        private void ProgrammerUpdate(object? sender, BmsEventArgs e)
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