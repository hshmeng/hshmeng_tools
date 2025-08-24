using System.Net.Sockets;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Threading;
using System.Collections.Generic;

namespace hshmeng_tools.ToolsFeatures.SaoHuo
{
    public static class PortScanner
    {
        public static void Scan(string ip, TextBox outputBox)
        {
            outputBox.Clear();
            outputBox.AppendText($"开始扫描 {ip} 的所有端口...\n");

            int maxConcurrent = 200;   // 并发数
            int batchSize = 1000;      // 每批端口数量

            Task.Run(async () =>
            {
                for (int batchStart = 1; batchStart <= 65535; batchStart += batchSize)
                {
                    int batchEnd = batchStart + batchSize - 1;
                    if (batchEnd > 65535) batchEnd = 65535;

                    SemaphoreSlim sem = new SemaphoreSlim(maxConcurrent);
                    List<Task> tasks = new List<Task>();

                    for (int port = batchStart; port <= batchEnd; port++)
                    {
                        await sem.WaitAsync();
                        tasks.Add(Task.Run(async () =>
                        {
                            try
                            {
                                using TcpClient client = new TcpClient();
                                var connectTask = client.ConnectAsync(ip, port);
                                if (await Task.WhenAny(connectTask, Task.Delay(500)) == connectTask && client.Connected)
                                {
                                    outputBox.Dispatcher.Invoke(() =>
                                    {
                                        outputBox.AppendText($"端口 {port} 开放\n");
                                    });
                                }
                            }
                            catch { } // 可以记录失败端口
                            finally
                            {
                                sem.Release();
                            }
                        }));
                    }

                    await Task.WhenAll(tasks); // 等待当前批次完成
                }

                outputBox.Dispatcher.Invoke(() =>
                {
                    outputBox.AppendText("端口扫描完成！");
                });
            });
        }
    }
}
