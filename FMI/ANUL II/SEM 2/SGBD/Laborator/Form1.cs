using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace Laborator
{
    public partial class Form1 : Form
    {
        private readonly SqlConnection _cs = new SqlConnection("Data Source=DESKTOP-L25SHPO\\SQLEXPRESS;Initial Catalog=Spotify;Integrated Security=True");
        private readonly SqlDataAdapter _daPlaylists = new SqlDataAdapter();
        private readonly SqlDataAdapter _daUsers = new SqlDataAdapter();
        private readonly DataSet _dsUsers = new DataSet();
        private readonly DataSet _dsPlaylists = new DataSet();
        // private readonly BindingSource _bs = new BindingSource();
        public Form1()
        {
            InitializeComponent();
            UpdateParentTable();
        }

        private void UpdateParentTable()
        {
            _daUsers.SelectCommand = new SqlCommand("select * from Users", _cs);
            _dsUsers.Clear();
            _daUsers.Fill(_dsUsers);
            dataGridViewUsers.DataSource = _dsUsers.Tables[0];
        }

        private void UpdateChildTable()
        {
            _dsPlaylists.Clear();
            _daPlaylists.Fill(_dsPlaylists);
        }

        private void dataGridViewUsers_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            _daPlaylists.SelectCommand = new SqlCommand("select * from Playlists where Uid=@uid", _cs);
            _daPlaylists.SelectCommand.Parameters.Add("@uid", SqlDbType.Int).Value = _dsUsers.Tables[0].Rows[dataGridViewUsers.CurrentCell.RowIndex][0];
            _dsPlaylists.Clear();
            _daPlaylists.Fill(_dsPlaylists);
            dataGridViewPlaylists.DataSource = _dsPlaylists.Tables[0];
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            if (txtNrMelodii.Text == "" || txtNumePlaylist.Text == "")
            {
                MessageBox.Show(@"Exista spatii necompletate!");
                return;
            }

            if (!int.TryParse(txtNrMelodii.Text, out _))
            {
                MessageBox.Show(@"Numarul de melodii nu este valid!");
                return;
            }

            _daPlaylists.InsertCommand =
                new SqlCommand("insert into Playlists(Uid, Name, NoOfSongs) values (@uid, @nume, @nrMelodii)",
                    _cs);
            if (dataGridViewUsers.CurrentCell != null)
                _daPlaylists.InsertCommand.Parameters.Add("@uid", SqlDbType.Int).Value =
                    _dsUsers.Tables[0].Rows[dataGridViewUsers.CurrentCell.RowIndex][0];
            else
            {
                MessageBox.Show(@"Nu ati selectat nici un user!");
                return;
            }

            _daPlaylists.InsertCommand.Parameters.Add("@nume", SqlDbType.VarChar).Value = txtNumePlaylist.Text;
            _daPlaylists.InsertCommand.Parameters.Add("@nrMelodii", SqlDbType.Int).Value = txtNrMelodii.Text;

            _cs.Open();
            _daPlaylists.InsertCommand.ExecuteNonQuery();
            _cs.Close();
            UpdateChildTable();
            MessageBox.Show(@"Playlist adaugat cu succes!");
        }

        private void btnDelete_Click(object sender, EventArgs eventArgs)
        {
            if (dataGridViewPlaylists.CurrentCell == null)
            {
                MessageBox.Show(@"Nu ati selectat nici un playlist!");
                return;
            }

            var dr = MessageBox.Show(@"Are you sure?
No undo after delete!", @"Confirm deletion", MessageBoxButtons.YesNo);
            if (dr == DialogResult.Yes)
            {
                _daPlaylists.DeleteCommand = new SqlCommand("""
                                                            delete from PlaylistSongs where Pid=@id1
                                                            delete from Playlists where Pid=@id2
                                                            """, _cs);
                _daPlaylists.DeleteCommand.Parameters.Add("@id1", SqlDbType.Int).Value =
                _daPlaylists.DeleteCommand.Parameters.Add("@id2", SqlDbType.Int).Value =
                    _dsPlaylists.Tables[0].Rows[dataGridViewPlaylists.CurrentCell.RowIndex][0];

                _cs.Open();
                _daPlaylists.DeleteCommand.ExecuteNonQuery();
                _cs.Close();
                
                UpdateChildTable();
            }
            else
            {
                MessageBox.Show(@"Deletion aborted!");
            }
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            if (dataGridViewPlaylists.CurrentCell == null)
            {
                MessageBox.Show(@"Nu ati selectat nici un playlist!");
                return;
            }
            if (txtNrMelodii.Text == "" || txtNumePlaylist.Text == "")
            {
                MessageBox.Show(@"Exista spatii necompletate!");
                return;
            }

            if (!int.TryParse(txtNrMelodii.Text, out _))
            {
                MessageBox.Show(@"Numarul de melodii nu este valid!");
                return;
            }
            
            _daPlaylists.UpdateCommand =
                new SqlCommand("update Playlists set Name=@nume, NoOfSongs=@nrMelodii where Pid=@id", _cs);

            _daPlaylists.UpdateCommand.Parameters.Add("@nume", SqlDbType.VarChar).Value = txtNumePlaylist.Text;
            _daPlaylists.UpdateCommand.Parameters.Add("@nrMelodii", SqlDbType.Int).Value = txtNrMelodii.Text;
            _daPlaylists.UpdateCommand.Parameters.Add("@id", SqlDbType.Int).Value =
                _dsPlaylists.Tables[0].Rows[dataGridViewPlaylists.CurrentCell.RowIndex][0];
            
            _cs.Open();
            var x = _daPlaylists.UpdateCommand.ExecuteNonQuery();
            _cs.Close();

            if (x >= 1)
            {
                UpdateChildTable();
                MessageBox.Show(@"The record has been udpdated!");
            }
        }

        private void dataGridViewPlaylists_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            txtNumePlaylist.Text =
                _dsPlaylists.Tables[0].Rows[dataGridViewPlaylists.CurrentCell.RowIndex][2].ToString();
            txtNrMelodii.Text = _dsPlaylists.Tables[0].Rows[dataGridViewPlaylists.CurrentCell.RowIndex][3].ToString();
        }
    }
}