using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace RecursiveEngineApp
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            try
            {
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string htmlPath = Path.Combine(baseDir, "index.html");
                string profileDir = Path.Combine(baseDir, "profile");

                if (!File.Exists(htmlPath))
                {
                    htmlPath = @"C:\Users\ole_a\Desktop\Apps\RecursiveEngine\index.html";
                }

                string htmlUri = new Uri(htmlPath).AbsoluteUri;

                // Candidate browser executables for standalone app-mode
                string[] candidates = new string[]
                {
                    @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    @"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    @"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                };

                string browserExe = null;
                foreach (string path in candidates)
                {
                    if (File.Exists(path))
                    {
                        browserExe = path;
                        break;
                    }
                }

                if (browserExe != null)
                {
                    string args = string.Format("--app=\"{0}\" --window-size=1000,880 --user-data-dir=\"{1}\" --app-id=RecursiveEngine", htmlUri, profileDir);
                    ProcessStartInfo psi = new ProcessStartInfo(browserExe, args);
                    psi.UseShellExecute = true;
                    Process.Start(psi);
                }
                else
                {
                    // Fallback to default handler
                    Process.Start(new ProcessStartInfo(htmlUri) { UseShellExecute = true });
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error launching Recursive Engine: " + ex.Message, "Recursive Engine", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
