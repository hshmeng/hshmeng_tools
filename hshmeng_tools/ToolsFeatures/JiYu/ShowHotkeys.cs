using System.Windows;

namespace hshmeng_tools.ToolsFeatures.JiYu
{
    public static class ShowHotkeys
    {
        public static void Show()
        {
            string message = "Ctrl + Alt + F: 紧急全屏快捷键\nCtrl + Alt + D: 快速显示/隐藏窗口快捷键";
            MessageBox.Show(message, "极域电子教室工具快捷键教学", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}