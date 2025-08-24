using System;
using System.IO;
using System.Windows;

namespace hshmeng_tools.ToolsFeatures.JiYu
{
    public static class CreateTKBatFile
    {
        public static void Create()
        {
            string fileName = "TK.bat";
            string content = @"@ECHO OFF
taskkill /f /im ProcHelper64.exe
taskkill /f /im tvnserver32.exe
taskkill /f /im DesktopCheck.exe
taskkill /f /im DeploymentAgent.exe
taskkill /f /im StudentMain.exe
taskkill /f /im GATESRV.exe
taskkill /f /im MasterHelper.exe
taskkill /f /im InstHelpApp.exe
taskkill /f /im InstHelpApp64.exe
taskkill /f /im TDChalk.exe
taskkill /f /im DispcapHelper.exe
SC STOP TDNetFilter
SC STOP TDFileFilter
";
            string[] roots = { @"C:\", @"D:\" };
            foreach (var root in roots)
            {
                try
                {
                    string path = Path.Combine(root, fileName);
                    File.WriteAllText(path, content);
                    MessageBox.Show($"已成功创建：{path}", "创建TK.bat", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }
                catch (Exception ex)
                {
                    _ = ex; // 显式使用变量，防止警告
                    // 继续尝试下一个盘符
                }
            }
            MessageBox.Show("C盘和D盘根目录均创建失败，请检查权限。", "创建TK.bat", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }
}