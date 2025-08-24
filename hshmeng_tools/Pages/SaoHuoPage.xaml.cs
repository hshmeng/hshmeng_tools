using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using hshmeng_tools.ToolsFeatures.SaoHuo;

namespace hshmeng_tools.Pages;

// 输入框占位符辅助类
public static class InputHelper
{
    public static void SetupPlaceholder(TextBox tb, string placeholder)
    {
        tb.Text = placeholder;
        tb.Foreground = Brushes.Gray;

        tb.GotFocus += (s, e) =>
        {
            if (tb.Text == placeholder)
            {
                tb.Text = "";
                tb.Foreground = Brushes.Black;
            }
        };

        tb.LostFocus += (s, e) =>
        {
            if (string.IsNullOrWhiteSpace(tb.Text))
            {
                tb.Text = placeholder;
                tb.Foreground = Brushes.Gray;
            }
        };
    }
}

public partial class SaoHuoPage : Page
{
    public SaoHuoPage()
    {
        InitializeComponent(); 
        InputHelper.SetupPlaceholder(IpTextBox, "填写IP地址");
        InputHelper.SetupPlaceholder(SubnetTextBox, "填写网段长度");
        InputHelper.SetupPlaceholder(PortIpTextBox, "填写IP地址");
    }

    // 折叠面板展开/收起
    private void LanScanButton_Click(object sender, RoutedEventArgs e)
    {
        LanScanPanel.Visibility = LanScanPanel.Visibility == Visibility.Visible
            ? Visibility.Collapsed
            : Visibility.Visible;
    }
    private void PortScanButton_Click(object sender, RoutedEventArgs e)
    {
        PortScanPanel.Visibility = PortScanPanel.Visibility == Visibility.Visible
            ? Visibility.Collapsed
            : Visibility.Visible;
    }

    // 开始扫描按钮
    private void StartLanScan_Click(object sender, RoutedEventArgs e)
    {
        string ip = IpTextBox.Text.Trim();
        string subnetStr = SubnetTextBox.Text.Trim();
        if (ip == "填写起始IP") ip = "";
        if (subnetStr == "填写网段长度") subnetStr = "";
        if (string.IsNullOrEmpty(ip) || string.IsNullOrEmpty(subnetStr))
        {
            MessageBox.Show("请填写起始IP和网段长度！");
            return;
        }
        if (!int.TryParse(subnetStr, out int length) || length < 1 || length > 32)
        {
            MessageBox.Show("网段长度必须是1~32之间的数字！");
            return;
        }
        LanScanner.Scan(ip, length, LanOutputTextBox);
    }
    // 开始端口扫描按钮
    private void StartPortScan_Click(object sender, RoutedEventArgs e)
    {
        string ip = PortIpTextBox.Text.Trim();
        if (ip == "填写IP地址") ip = "";

        if (string.IsNullOrEmpty(ip))
        {
            MessageBox.Show("请填写IP地址！");
            return;
        }
        PortScanner.Scan(ip, PortOutputTextBox);
    }
    
    private void CommonPortsButton_Click(object sender, RoutedEventArgs e)
    {
        var window = new CommonPortsWindow();
        window.Show();
    }
}