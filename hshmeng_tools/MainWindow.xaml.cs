using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace hshmeng_tools
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            NavListBox.SelectedIndex = 0; // 默认选中第一个
        }

        private void NavListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (NavListBox.SelectedItem is ListBoxItem item)
            {
                switch (item.Content.ToString())
                {
                    case "极域工具":
                        MainFrame.Navigate(new Pages.JiYuPage());
                        break;
                    case "扫活工具":
                        MainFrame.Navigate(new Pages.SaoHuoPage());
                        break;
                    case "帮助":
                        MainFrame.Navigate(new Pages.HelpPage());
                        break;
                    case "设置":
                        MainFrame.Navigate(new Pages.SettingsPage());
                        break;
                }
            }
        }

        // ---------------- 自定义标题栏事件 ----------------
        private void Minimize_Click(object sender, RoutedEventArgs e)
        {
            this.WindowState = WindowState.Minimized;
        }

        private void MaximizeRestore_Click(object sender, RoutedEventArgs e)
        {
            if (this.WindowState == WindowState.Normal)
                this.WindowState = WindowState.Maximized;
            else
                this.WindowState = WindowState.Normal;
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ButtonState == MouseButtonState.Pressed)
                this.DragMove();
        }
    }
}
