using System;
using System.Collections.Generic;
using System.Net.NetworkInformation;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;

namespace hshmeng_tools.ToolsFeatures.SaoHuo
{
    // 局域网扫描辅助类
    public static class LanScanner
    {
        public static void Scan(string startIp, int subnetMaskLength, TextBox outputBox)
        {
            outputBox.Clear();
            outputBox.AppendText($"开始扫描 {startIp}/{subnetMaskLength} ...\n");

            string[] parts = startIp.Split('.');
            if (parts.Length != 4)
            {
                outputBox.AppendText("IP 格式错误\n");
                return;
            }

            // 将 IP 转成 uint
            uint ipUint = (uint)(int.Parse(parts[0]) << 24 |
                                 int.Parse(parts[1]) << 16 |
                                 int.Parse(parts[2]) << 8 |
                                 int.Parse(parts[3]));

            // 子网掩码
            uint mask = subnetMaskLength == 0 ? 0 : 0xFFFFFFFF << (32 - subnetMaskLength);

            // 网络地址
            uint network = ipUint & mask;
            int hostBits = 32 - subnetMaskLength;
            uint maxHosts = hostBits == 0 ? 1u : (uint)Math.Pow(2, hostBits) - 2;
            if (maxHosts > 65534) maxHosts = 65534;

            List<uint> ipList = new List<uint>();
            for (uint i = 1; i <= maxHosts; i++)
            {
                ipList.Add(network + i);
            }

            SemaphoreSlim semaphore = new SemaphoreSlim(200);

            Task.Run(async () =>
            {
                List<Task> tasks = new List<Task>();

                foreach (var ipNum in ipList)
                {
                    await semaphore.WaitAsync();

                    tasks.Add(Task.Run(async () =>
                    {
                        try
                        {
                            string ipStr = $"{(ipNum >> 24) & 0xFF}.{(ipNum >> 16) & 0xFF}.{(ipNum >> 8) & 0xFF}.{ipNum & 0xFF}";
                            using Ping ping = new Ping();
                            bool alive = false;

                            for (int attempt = 0; attempt < 2; attempt++)
                            {
                                try
                                {
                                    PingReply reply = await ping.SendPingAsync(ipStr, 300);
                                    if (reply.Status == IPStatus.Success)
                                    {
                                        alive = true;
                                        break;
                                    }
                                }
                                catch { }
                            }

                            if (alive)
                            {
                                outputBox.Dispatcher.Invoke(() =>
                                {
                                    outputBox.AppendText($"{ipStr} 存活\n");
                                });
                            }
                        }
                        finally
                        {
                            semaphore.Release();
                        }
                    }));
                }

                await Task.WhenAll(tasks);

                outputBox.Dispatcher.Invoke(() =>
                {
                    outputBox.AppendText("扫描完成！");
                });
            });
        }
    }
}
