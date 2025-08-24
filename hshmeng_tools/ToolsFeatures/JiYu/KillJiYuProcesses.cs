using System.Diagnostics;
using System.Text;
using System.Windows;

namespace hshmeng_tools.ToolsFeatures.JiYu
{
    public static class KillJiYuProcesses
    {
        public static void Kill()
        {
            var sb = new StringBuilder();
            string[] processes = {
                "ProcHelper64.exe",
                "tvnserver32.exe",
                "DesktopCheck.exe",
                "DeploymentAgent.exe",
                "StudentMain.exe",
                "GATESRV.exe",
                "MasterHelper.exe",
                "InstHelpApp.exe",
                "InstHelpApp64.exe",
                "TDChalk.exe",
                "DispcapHelper.exe"
            };

            foreach (var proc in processes)
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "taskkill",
                        Arguments = $"/f /im {proc}",
                        CreateNoWindow = true,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true
                    };
                    using (var p = Process.Start(psi)!)
                    {
                        string output = p.StandardOutput.ReadToEnd();
                        string error = p.StandardError.ReadToEnd();
                        p.WaitForExit();
                        if (p.ExitCode == 0)
                            sb.AppendLine($"{proc}：成功终止");
                        else
                            sb.AppendLine($"{proc}：未找到或终止失败");
                    }
                }
                catch
                {
                    sb.AppendLine($"{proc}：执行出错");
                }
            }

            string[] services = { "TDNetFilter", "TDFileFilter" };
            foreach (var svc in services)
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "sc",
                        Arguments = $"stop {svc}",
                        CreateNoWindow = true,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true
                    };
                    using (var p = Process.Start(psi)!)
                    {
                        string output = p.StandardOutput.ReadToEnd();
                        string error = p.StandardError.ReadToEnd();
                        p.WaitForExit();
                        if (output.Contains("STOP_PENDING") || output.Contains("已停止") || output.Contains("STOPPED"))
                            sb.AppendLine($"{svc} 服务：停止成功");
                        else
                            sb.AppendLine($"{svc} 服务：停止失败或未运行");
                    }
                }
                catch
                {
                    sb.AppendLine($"{svc} 服务：执行出错");
                }
            }

            MessageBox.Show(sb.ToString(), "一键杀死结果", MessageBoxButton.OK, MessageBoxImage.Information);
        }
    }
}