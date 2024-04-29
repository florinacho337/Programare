using Gtk;

namespace Client
{
    public class MessageAlert
    {
        public static void ShowErrorMessage(string message)
        {
            MessageDialog dialog = new MessageDialog(null, DialogFlags.Modal, MessageType.Error, ButtonsType.Ok, message);
            dialog.Title = "Error";
            dialog.Run();
            dialog.Destroy();
        }

        public static void ShowMessage(string message)
        {
            MessageDialog dialog = new MessageDialog(null, DialogFlags.Modal, MessageType.Info, ButtonsType.Ok, message);
            dialog.Title = "Confirmation";
            dialog.Run();
            dialog.Destroy();
        }
    }
}