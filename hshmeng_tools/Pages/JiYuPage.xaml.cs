using System.Windows.Controls;
using System.Windows;
using System.Diagnostics;
using System.IO;
using hshmeng_tools.ToolsFeatures.JiYu;

namespace hshmeng_tools.Pages
{
    public partial class JiYuPage : Page
    {
        public JiYuPage()
        {
            InitializeComponent();
        }
        
        private void StartJiYuButton_Click(object sender, RoutedEventArgs e)
        {
            string exePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ToolsFeatures", "JiYu", "JiYu.exe");
            if (File.Exists(exePath))
            {
                Process.Start(new ProcessStartInfo(exePath) { UseShellExecute = true });
            }
            else
            {
                MessageBox.Show("未找到JiYu.exe文件。", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        private void HotkeysButton_Click(object sender, RoutedEventArgs e)
        {
            ShowHotkeys.Show();
        }
        private void KillButton_Click(object sender, RoutedEventArgs e)
        {
            KillJiYuProcesses.Kill();
        }
        private void CreateTKBatButton_Click(object sender, RoutedEventArgs e)
        {
            CreateTKBatFile.Create();
        }
    }
}