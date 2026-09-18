using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;

class IconGenerator
{
    static void Main()
    {
        string baseDir = @"C:\Users\ole_a\Desktop\Apps";
        GenerateRecursiveEngineIcon(Path.Combine(baseDir, @"RecursiveEngine\app.ico"));
        GenerateTicTacToeIcon(Path.Combine(baseDir, @"TicTacToe\app.ico"));
    }

    static void SaveAsIco(Bitmap bmp, string path)
    {
        using (MemoryStream pngStream = new MemoryStream())
        {
            bmp.Save(pngStream, ImageFormat.Png);
            byte[] pngBytes = pngStream.ToArray();

            using (FileStream fs = new FileStream(path, FileMode.Create))
            using (BinaryWriter bw = new BinaryWriter(fs))
            {
                // ICONDIR header
                bw.Write((short)0); // Reserved
                bw.Write((short)1); // Type: 1 = ICO
                bw.Write((short)1); // Image count = 1

                // ICONDIRENTRY
                bw.Write((byte)bmp.Width);
                bw.Write((byte)bmp.Height);
                bw.Write((byte)0); // Color palette count
                bw.Write((byte)0); // Reserved
                bw.Write((short)1); // Color planes
                bw.Write((short)32); // Bits per pixel
                bw.Write(pngBytes.Length); // Image size in bytes
                bw.Write(6 + 16); // Offset of image data

                // Image Data (PNG payload supported in modern Windows ICO)
                bw.Write(pngBytes);
            }
        }
    }

    static void GenerateRecursiveEngineIcon(string outPath)
    {
        using (Bitmap bmp = new Bitmap(256, 256))
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.Clear(Color.Transparent);

            // Dark rounded background
            using (GraphicsPath path = RoundedRect(new Rectangle(8, 8, 240, 240), 40))
            using (LinearGradientBrush bgBrush = new LinearGradientBrush(new Point(0, 0), new Point(256, 256), Color.FromArgb(20, 24, 38), Color.FromArgb(10, 12, 20)))
            {
                g.FillPath(bgBrush, path);
                using (Pen borderPen = new Pen(Color.FromArgb(80, 130, 255), 4))
                {
                    g.DrawPath(borderPen, path);
                }
            }

            // Draw recursive nesting squares/fractal vortex
            Color[] colors = new Color[] {
                Color.FromArgb(0, 229, 255),
                Color.FromArgb(99, 102, 241),
                Color.FromArgb(168, 85, 247),
                Color.FromArgb(236, 72, 153),
                Color.FromArgb(245, 158, 11)
            };

            for (int i = 0; i < 5; i++)
            {
                float size = 160f - (i * 28f);
                float offset = (256f - size) / 2f;
                using (Pen pen = new Pen(colors[i % colors.Length], 4f - (i * 0.4f)))
                {
                    g.TranslateTransform(128, 128);
                    g.RotateTransform(i * 18f);
                    g.DrawRectangle(pen, -size / 2f, -size / 2f, size, size);
                    g.ResetTransform();
                }
            }

            // Core center glowing circle
            using (SolidBrush coreBrush = new SolidBrush(Color.FromArgb(240, 255, 255)))
            {
                g.FillEllipse(coreBrush, 128 - 10, 128 - 10, 20, 20);
            }

            SaveAsIco(bmp, outPath);
        }
    }

    static void GenerateTicTacToeIcon(string outPath)
    {
        using (Bitmap bmp = new Bitmap(256, 256))
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.Clear(Color.Transparent);

            // Dark rounded background
            using (GraphicsPath path = RoundedRect(new Rectangle(8, 8, 240, 240), 40))
            using (LinearGradientBrush bgBrush = new LinearGradientBrush(new Point(0, 0), new Point(256, 256), Color.FromArgb(24, 24, 32), Color.FromArgb(12, 12, 18)))
            {
                g.FillPath(bgBrush, path);
                using (Pen borderPen = new Pen(Color.FromArgb(244, 63, 94), 4))
                {
                    g.DrawPath(borderPen, path);
                }
            }

            // Grid lines
            using (Pen gridPen = new Pen(Color.FromArgb(90, 100, 130), 6))
            {
                gridPen.StartCap = LineCap.Round;
                gridPen.EndCap = LineCap.Round;
                g.DrawLine(gridPen, 95, 45, 95, 211);
                g.DrawLine(gridPen, 161, 45, 161, 211);
                g.DrawLine(gridPen, 45, 95, 211, 95);
                g.DrawLine(gridPen, 45, 161, 211, 161);
            }

            // Draw X (Cyan/Blue)
            using (Pen xPen = new Pen(Color.FromArgb(14, 165, 233), 8))
            {
                xPen.StartCap = LineCap.Round;
                xPen.EndCap = LineCap.Round;
                g.DrawLine(xPen, 55, 55, 85, 85);
                g.DrawLine(xPen, 85, 55, 55, 85);
            }

            // Draw O (Rose/Pink)
            using (Pen oPen = new Pen(Color.FromArgb(244, 63, 94), 8))
            {
                g.DrawEllipse(oPen, 113, 113, 30, 30);
            }

            // Draw X in bottom right
            using (Pen xPen2 = new Pen(Color.FromArgb(14, 165, 233), 8))
            {
                xPen2.StartCap = LineCap.Round;
                xPen2.EndCap = LineCap.Round;
                g.DrawLine(xPen2, 171, 171, 201, 201);
                g.DrawLine(xPen2, 201, 171, 171, 201);
            }

            SaveAsIco(bmp, outPath);
        }
    }

    static GraphicsPath RoundedRect(Rectangle bounds, int radius)
    {
        int diameter = radius * 2;
        Size size = new Size(diameter, diameter);
        Rectangle arc = new Rectangle(bounds.Location, size);
        GraphicsPath path = new GraphicsPath();

        if (radius == 0)
        {
            path.AddRectangle(bounds);
            return path;
        }

        path.AddArc(arc, 180, 90);
        arc.X = bounds.Right - diameter;
        path.AddArc(arc, 270, 90);
        arc.Y = bounds.Bottom - diameter;
        path.AddArc(arc, 0, 90);
        arc.X = bounds.Left;
        path.AddArc(arc, 90, 90);
        path.CloseFigure();
        return path;
    }
}
