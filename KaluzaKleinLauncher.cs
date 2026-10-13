using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace KaluzaKleinStudio
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            try
            {
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string htmlPath = Path.Combine(baseDir, "kaluza_klein_app.html");

                // Check default locations if moved
                if (!File.Exists(htmlPath))
                {
                    string homeDir = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                    string altPath = Path.Combine(homeDir, "kaluza_klein_app.html");
                    if (File.Exists(altPath))
                    {
                        htmlPath = altPath;
                    }
                }

                if (!File.Exists(htmlPath))
                {
                    MessageBox.Show("Could not locate kaluza_klein_app.html", "Kaluza-Klein Studio", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Try launching in standalone browser window mode (Edge/Chrome app mode) for clean app experience
                string edgePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), @"Microsoft\Edge\Application\msedge.exe");
                if (!File.Exists(edgePath))
                {
                    edgePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), @"Microsoft\Edge\Application\msedge.exe");
                }

                if (File.Exists(edgePath))
                {
                    ProcessStartInfo psi = new ProcessStartInfo
                    {
                        FileName = edgePath,
                        Arguments = string.Format("--app=\"file:///{0}\" --window-size=1400,900", htmlPath.Replace('\\', '/')),
                        UseShellExecute = true
                    };
                    Process.Start(psi);
                }
                else
                {
                    // Fallback to default browser
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = htmlPath,
                        UseShellExecute = true
                    });
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to launch application: " + ex.Message, "Kaluza-Klein Studio", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
