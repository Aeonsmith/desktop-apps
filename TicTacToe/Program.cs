using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Media;
using System.Threading;
using System.Windows.Forms;

namespace TicTacToeApp
{
    public class TicTacToeForm : Form
    {
        // Game State
        private char[] board = new char[9]; // ' ', 'X', 'O'
        private char currentTurn = 'X';
        private bool gameOver = false;
        private int[] winningCombo = null; // e.g. [0,1,2]
        private string statusMessage = "Player X's Turn";

        // Game Settings & Modes
        private bool isVsAI = true;
        private string aiDifficulty = "Master (Unbeatable)"; // Easy, Medium, Master
        private char humanPlayer = 'X';
        private char aiPlayer = 'O';
        private bool soundEnabled = true;

        // Statistics
        private int scoreX = 0;
        private int scoreO = 0;
        private int scoreDraws = 0;
        private int streakX = 0;
        private int streakO = 0;

        // Move History for Undo
        private Stack<char[]> history = new Stack<char[]>();

        // UI Colors matching app.ico
        private readonly Color BgColor = Color.FromArgb(15, 17, 26);
        private readonly Color CardBg = Color.FromArgb(24, 27, 40);
        private readonly Color GridColor = Color.FromArgb(42, 47, 68);
        private readonly Color CellHoverColor = Color.FromArgb(32, 37, 56);
        private readonly Color CyanX = Color.FromArgb(14, 165, 233);
        private readonly Color CyanGlow = Color.FromArgb(56, 189, 248);
        private readonly Color RoseO = Color.FromArgb(244, 63, 94);
        private readonly Color RoseGlow = Color.FromArgb(251, 113, 133);
        private readonly Color GoldColor = Color.FromArgb(251, 191, 36);
        private readonly Color TextMuted = Color.FromArgb(148, 163, 184);
        private readonly Color WinLineColor = Color.FromArgb(52, 211, 153);

        // UI Controls
        private ComboBox modeCombo;
        private ComboBox diffCombo;
        private Button btnNewRound;
        private Button btnResetScores;
        private Button btnUndo;
        private CheckBox chkSound;

        // Board layout geometry
        private Rectangle boardRect = new Rectangle(50, 190, 420, 420);
        private Rectangle[] cellRects = new Rectangle[9];
        private int hoveredCell = -1;

        public TicTacToeForm()
        {
            this.Text = "Tic Tac Toe — Modern Neon Edition";
            this.ClientSize = new Size(520, 720);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.BackColor = BgColor;
            this.DoubleBuffered = true;

            // Load app icon if available
            string iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "app.ico");
            if (!File.Exists(iconPath))
            {
                iconPath = @"C:\Users\ole_a\Desktop\Apps\TicTacToe\app.ico";
            }
            if (File.Exists(iconPath))
            {
                try
                {
                    this.Icon = new Icon(iconPath);
                }
                catch { }
            }

            InitCellRectangles();
            InitControls();
            ResetGame(false);

            this.MouseMove += OnFormMouseMove;
            this.MouseLeave += (s, e) => { hoveredCell = -1; Invalidate(); };
            this.MouseDown += OnFormMouseDown;
            this.Paint += OnFormPaint;
        }

        private void InitCellRectangles()
        {
            int cellW = boardRect.Width / 3;
            int cellH = boardRect.Height / 3;
            for (int i = 0; i < 9; i++)
            {
                int r = i / 3;
                int c = i % 3;
                cellRects[i] = new Rectangle(boardRect.Left + c * cellW, boardRect.Top + r * cellH, cellW, cellH);
            }
        }

        private void InitControls()
        {
            // Top Options Panel
            Panel topPanel = new Panel
            {
                Location = new Point(20, 10),
                Size = new Size(480, 50),
                BackColor = CardBg
            };

            Label lblMode = new Label
            {
                Text = "Mode:",
                ForeColor = TextMuted,
                Font = new Font("Segoe UI", 9f, FontStyle.Bold),
                Location = new Point(10, 15),
                AutoSize = true
            };

            modeCombo = new ComboBox
            {
                Location = new Point(55, 12),
                Width = 120,
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = Color.FromArgb(30, 34, 52),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9f)
            };
            modeCombo.Items.AddRange(new object[] { "vs AI", "2 Players" });
            modeCombo.SelectedIndex = 0;
            modeCombo.SelectedIndexChanged += (s, e) =>
            {
                isVsAI = (modeCombo.SelectedIndex == 0);
                diffCombo.Enabled = isVsAI;
                ResetGame(false);
            };

            Label lblDiff = new Label
            {
                Text = "AI:",
                ForeColor = TextMuted,
                Font = new Font("Segoe UI", 9f, FontStyle.Bold),
                Location = new Point(185, 15),
                AutoSize = true
            };

            diffCombo = new ComboBox
            {
                Location = new Point(210, 12),
                Width = 140,
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = Color.FromArgb(30, 34, 52),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9f)
            };
            diffCombo.Items.AddRange(new object[] { "Master (Unbeatable)", "Medium", "Easy" });
            diffCombo.SelectedIndex = 0;
            diffCombo.SelectedIndexChanged += (s, e) =>
            {
                aiDifficulty = diffCombo.SelectedItem.ToString();
                ResetGame(false);
            };

            chkSound = new CheckBox
            {
                Text = "🔊 Sound",
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9f),
                Location = new Point(370, 14),
                Checked = true,
                AutoSize = true
            };
            chkSound.CheckedChanged += (s, e) => { soundEnabled = chkSound.Checked; };

            topPanel.Controls.AddRange(new Control[] { lblMode, modeCombo, lblDiff, diffCombo, chkSound });
            this.Controls.Add(topPanel);

            // Bottom Buttons Panel
            Panel bottomPanel = new Panel
            {
                Location = new Point(20, 625),
                Size = new Size(480, 50),
                BackColor = CardBg
            };

            btnNewRound = CreateStyledButton("🔄 New Round", new Point(15, 8), new Size(130, 34), Color.FromArgb(2, 132, 199));
            btnNewRound.Click += (s, e) => ResetGame(false);

            btnUndo = CreateStyledButton("↩️ Undo", new Point(160, 8), new Size(110, 34), Color.FromArgb(51, 65, 85));
            btnUndo.Click += (s, e) => UndoMove();

            btnResetScores = CreateStyledButton("🗑️ Reset Scores", new Point(285, 8), new Size(180, 34), Color.FromArgb(71, 85, 105));
            btnResetScores.Click += (s, e) => ResetScores();

            bottomPanel.Controls.AddRange(new Control[] { btnNewRound, btnUndo, btnResetScores });
            this.Controls.Add(bottomPanel);
        }

        private Button CreateStyledButton(string text, Point loc, Size size, Color bg)
        {
            Button btn = new Button
            {
                Text = text,
                Location = loc,
                Size = size,
                BackColor = bg,
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 9.5f, FontStyle.Bold),
                Cursor = Cursors.Hand
            };
            btn.FlatAppearance.BorderSize = 0;
            return btn;
        }

        private void PlayGameSound(string type)
        {
            if (!soundEnabled) return;
            new Thread(() =>
            {
                try
                {
                    if (type == "click")
                    {
                        Console.Beep(520, 45);
                    }
                    else if (type == "win")
                    {
                        Console.Beep(587, 80);
                        Thread.Sleep(30);
                        Console.Beep(740, 80);
                        Thread.Sleep(30);
                        Console.Beep(880, 150);
                    }
                    else if (type == "draw")
                    {
                        Console.Beep(440, 90);
                        Thread.Sleep(40);
                        Console.Beep(330, 120);
                    }
                    else if (type == "undo")
                    {
                        Console.Beep(380, 60);
                    }
                }
                catch { }
            })
            { IsBackground = true }.Start();
        }

        private void ResetGame(bool keepHistory)
        {
            for (int i = 0; i < 9; i++) board[i] = ' ';
            currentTurn = 'X';
            gameOver = false;
            winningCombo = null;
            statusMessage = "Player X's Turn";
            if (!keepHistory) history.Clear();
            Invalidate();
        }

        private void ResetScores()
        {
            scoreX = 0;
            scoreO = 0;
            scoreDraws = 0;
            streakX = 0;
            streakO = 0;
            ResetGame(false);
        }

        private void SaveState()
        {
            char[] clone = (char[])board.Clone();
            history.Push(clone);
        }

        private void UndoMove()
        {
            if (gameOver || history.Count == 0) return;

            if (isVsAI)
            {
                if (history.Count >= 1)
                {
                    board = history.Pop();
                    currentTurn = humanPlayer;
                    statusMessage = "Move undone. Player X's Turn";
                    PlayGameSound("undo");
                    Invalidate();
                }
            }
            else
            {
                board = history.Pop();
                currentTurn = (currentTurn == 'X') ? 'O' : 'X';
                statusMessage = string.Format("Move undone. Player {0}'s Turn", currentTurn);
                PlayGameSound("undo");
                Invalidate();
            }
        }

        private void OnFormMouseMove(object sender, MouseEventArgs e)
        {
            if (gameOver) return;
            int prev = hoveredCell;
            hoveredCell = -1;
            for (int i = 0; i < 9; i++)
            {
                if (cellRects[i].Contains(e.Location) && board[i] == ' ')
                {
                    hoveredCell = i;
                    break;
                }
            }
            if (prev != hoveredCell) Invalidate();
        }

        private void OnFormMouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button != MouseButtons.Left || gameOver) return;

            for (int i = 0; i < 9; i++)
            {
                if (cellRects[i].Contains(e.Location) && board[i] == ' ')
                {
                    MakePlayerMove(i);
                    break;
                }
            }
        }

        private void MakePlayerMove(int index)
        {
            SaveState();
            board[index] = currentTurn;
            PlayGameSound("click");

            if (CheckWinOrDraw()) return;

            if (isVsAI)
            {
                currentTurn = aiPlayer;
                statusMessage = "AI is thinking...";
                Invalidate();

                // Small delay for natural AI response
                var aiTimer = new System.Windows.Forms.Timer();
                aiTimer.Interval = 220;
                aiTimer.Tick += (s, e) =>
                {
                    aiTimer.Stop();
                    aiTimer.Dispose();
                    MakeAIMove();
                };
                aiTimer.Start();
            }
            else
            {
                currentTurn = (currentTurn == 'X') ? 'O' : 'X';
                statusMessage = string.Format("Player {0}'s Turn", currentTurn);
                Invalidate();
            }
        }

        private void MakeAIMove()
        {
            if (gameOver) return;

            int bestMove = -1;

            if (aiDifficulty == "Easy")
            {
                bestMove = GetRandomMove();
            }
            else if (aiDifficulty == "Medium")
            {
                // Try to win or block, else random
                bestMove = FindWinningMove(aiPlayer);
                if (bestMove == -1) bestMove = FindWinningMove(humanPlayer);
                if (bestMove == -1) bestMove = GetRandomMove();
            }
            else // Master / Unbeatable Minimax
            {
                bestMove = GetBestMinimaxMove();
            }

            if (bestMove >= 0 && bestMove < 9 && board[bestMove] == ' ')
            {
                board[bestMove] = aiPlayer;
                PlayGameSound("click");
                if (CheckWinOrDraw()) return;

                currentTurn = humanPlayer;
                statusMessage = "Player X's Turn";
            }
            Invalidate();
        }

        private int GetRandomMove()
        {
            List<int> available = new List<int>();
            for (int i = 0; i < 9; i++)
            {
                if (board[i] == ' ') available.Add(i);
            }
            if (available.Count == 0) return -1;
            Random rnd = new Random();
            return available[rnd.Next(available.Count)];
        }

        private int FindWinningMove(char player)
        {
            int[][] lines = GetLines();
            foreach (var line in lines)
            {
                int count = 0;
                int emptyIdx = -1;
                foreach (int idx in line)
                {
                    if (board[idx] == player) count++;
                    else if (board[idx] == ' ') emptyIdx = idx;
                }
                if (count == 2 && emptyIdx != -1) return emptyIdx;
            }
            return -1;
        }

        private int GetBestMinimaxMove()
        {
            int bestScore = int.MinValue;
            int bestMove = -1;

            for (int i = 0; i < 9; i++)
            {
                if (board[i] == ' ')
                {
                    board[i] = aiPlayer;
                    int score = Minimax(board, 0, false, int.MinValue, int.MaxValue);
                    board[i] = ' ';
                    if (score > bestScore)
                    {
                        bestScore = score;
                        bestMove = i;
                    }
                }
            }
            return bestMove;
        }

        private int Minimax(char[] b, int depth, bool isMaximizing, int alpha, int beta)
        {
            int[] win = CheckBoardWinner(b);
            if (win != null)
            {
                char winner = b[win[0]];
                if (winner == aiPlayer) return 10 - depth;
                if (winner == humanPlayer) return depth - 10;
            }

            bool isFull = true;
            for (int i = 0; i < 9; i++)
            {
                if (b[i] == ' ') { isFull = false; break; }
            }
            if (isFull) return 0;

            if (isMaximizing)
            {
                int maxEval = int.MinValue;
                for (int i = 0; i < 9; i++)
                {
                    if (b[i] == ' ')
                    {
                        b[i] = aiPlayer;
                        int eval = Minimax(b, depth + 1, false, alpha, beta);
                        b[i] = ' ';
                        maxEval = Math.Max(maxEval, eval);
                        alpha = Math.Max(alpha, eval);
                        if (beta <= alpha) break;
                    }
                }
                return maxEval;
            }
            else
            {
                int minEval = int.MaxValue;
                for (int i = 0; i < 9; i++)
                {
                    if (b[i] == ' ')
                    {
                        b[i] = humanPlayer;
                        int eval = Minimax(b, depth + 1, true, alpha, beta);
                        b[i] = ' ';
                        minEval = Math.Min(minEval, eval);
                        beta = Math.Min(beta, eval);
                        if (beta <= alpha) break;
                    }
                }
                return minEval;
            }
        }

        private int[][] GetLines()
        {
            return new int[][]
            {
                new int[] { 0, 1, 2 },
                new int[] { 3, 4, 5 },
                new int[] { 6, 7, 8 },
                new int[] { 0, 3, 6 },
                new int[] { 1, 4, 7 },
                new int[] { 2, 5, 8 },
                new int[] { 0, 4, 8 },
                new int[] { 2, 4, 6 }
            };
        }

        private int[] CheckBoardWinner(char[] b)
        {
            int[][] lines = GetLines();
            foreach (var line in lines)
            {
                if (b[line[0]] != ' ' && b[line[0]] == b[line[1]] && b[line[1]] == b[line[2]])
                {
                    return line;
                }
            }
            return null;
        }

        private bool CheckWinOrDraw()
        {
            winningCombo = CheckBoardWinner(board);
            if (winningCombo != null)
            {
                gameOver = true;
                char winner = board[winningCombo[0]];
                if (winner == 'X')
                {
                    scoreX++;
                    streakX++;
                    streakO = 0;
                    statusMessage = isVsAI ? "🎉 You Won! (Player X Victory)" : "🎉 Player X Won!";
                }
                else
                {
                    scoreO++;
                    streakO++;
                    streakX = 0;
                    statusMessage = isVsAI ? "🤖 AI Won! (Player O Victory)" : "🎉 Player O Won!";
                }
                PlayGameSound("win");
                Invalidate();
                return true;
            }

            bool isFull = true;
            for (int i = 0; i < 9; i++)
            {
                if (board[i] == ' ') { isFull = false; break; }
            }

            if (isFull)
            {
                gameOver = true;
                scoreDraws++;
                streakX = 0;
                streakO = 0;
                statusMessage = "🤝 It's a Draw!";
                PlayGameSound("draw");
                Invalidate();
                return true;
            }

            return false;
        }

        private void OnFormPaint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            // 1. Draw Scoreboard Cards
            DrawScoreboard(g);

            // 2. Draw Status Message Banner
            DrawStatusBar(g);

            // 3. Draw Game Board Container & Grid
            DrawGameBoard(g);

            // 4. Draw X and O Tokens
            DrawPieces(g);

            // 5. Draw Winning Strike Line
            if (winningCombo != null)
            {
                DrawWinningLine(g);
            }
        }

        private void DrawScoreboard(Graphics g)
        {
            int top = 70;
            int cardW = 145;
            int cardH = 65;
            int gap = 15;

            // X Score Card
            DrawCard(g, new Rectangle(25, top, cardW, cardH), "PLAYER (X)", scoreX.ToString(), CyanX, streakX > 1 ? string.Format("🔥 {0} Streak", streakX) : null);

            // Draws Card
            DrawCard(g, new Rectangle(25 + cardW + gap, top, cardW, cardH), "DRAWS", scoreDraws.ToString(), GoldColor, null);

            // O Score Card
            string oLabel = isVsAI ? "AI (O)" : "PLAYER (O)";
            DrawCard(g, new Rectangle(25 + (cardW + gap) * 2, top, cardW, cardH), oLabel, scoreO.ToString(), RoseO, streakO > 1 ? string.Format("🔥 {0} Streak", streakO) : null);
        }

        private void DrawCard(Graphics g, Rectangle r, string title, string val, Color accent, string subtext)
        {
            using (GraphicsPath path = RoundedRect(r, 12))
            using (SolidBrush brush = new SolidBrush(CardBg))
            using (Pen borderPen = new Pen(GridColor, 1.5f))
            {
                g.FillPath(brush, path);
                g.DrawPath(borderPen, path);
            }

            // Top indicator bar
            using (GraphicsPath topBar = RoundedRect(new Rectangle(r.X + 2, r.Y + 2, r.Width - 4, 3), 2))
            using (SolidBrush topBrush = new SolidBrush(accent))
            {
                g.FillPath(topBrush, topBar);
            }

            using (Font titleFont = new Font("Segoe UI", 8.5f, FontStyle.Bold))
            using (SolidBrush titleBrush = new SolidBrush(TextMuted))
            {
                g.DrawString(title, titleFont, titleBrush, r.X + 12, r.Y + 10);
            }

            using (Font valFont = new Font("Segoe UI", 16f, FontStyle.Bold))
            using (SolidBrush valBrush = new SolidBrush(Color.White))
            {
                g.DrawString(val, valFont, valBrush, r.X + 12, r.Y + 28);
            }

            if (!string.IsNullOrEmpty(subtext))
            {
                using (Font subFont = new Font("Segoe UI", 8f, FontStyle.Bold))
                using (SolidBrush subBrush = new SolidBrush(GoldColor))
                {
                    g.DrawString(subtext, subFont, subBrush, r.Right - 65, r.Y + 34);
                }
            }
        }

        private void DrawStatusBar(Graphics g)
        {
            Rectangle statusRect = new Rectangle(50, 145, 420, 36);
            Color statusBg = gameOver ? ((winningCombo != null) ? Color.FromArgb(40, 20, 35) : Color.FromArgb(30, 35, 45)) : Color.FromArgb(20, 25, 38);
            Color borderColor = gameOver ? ((winningCombo != null) ? RoseO : GoldColor) : (currentTurn == 'X' ? CyanX : RoseO);

            using (GraphicsPath path = RoundedRect(statusRect, 8))
            using (SolidBrush brush = new SolidBrush(statusBg))
            using (Pen pen = new Pen(borderColor, 1.5f))
            {
                g.FillPath(brush, path);
                g.DrawPath(pen, path);
            }

            using (Font statusFont = new Font("Segoe UI", 11f, FontStyle.Bold))
            using (SolidBrush textBrush = new SolidBrush(Color.White))
            using (StringFormat sf = new StringFormat { Alignment = StringAlignment.Center, LineAlignment = StringAlignment.Center })
            {
                g.DrawString(statusMessage, statusFont, textBrush, statusRect, sf);
            }
        }

        private void DrawGameBoard(Graphics g)
        {
            // Outer container
            using (GraphicsPath path = RoundedRect(new Rectangle(boardRect.X - 8, boardRect.Y - 8, boardRect.Width + 16, boardRect.Height + 16), 18))
            using (SolidBrush brush = new SolidBrush(CardBg))
            using (Pen borderPen = new Pen(GridColor, 2f))
            {
                g.FillPath(brush, path);
                g.DrawPath(borderPen, path);
            }

            // Hover cell highlight
            if (hoveredCell >= 0 && hoveredCell < 9 && board[hoveredCell] == ' ' && !gameOver)
            {
                Rectangle hr = cellRects[hoveredCell];
                hr.Inflate(-4, -4);
                using (GraphicsPath hpath = RoundedRect(hr, 10))
                using (SolidBrush hbrush = new SolidBrush(CellHoverColor))
                {
                    g.FillPath(hbrush, hpath);
                }
            }

            // Grid Lines
            int cellW = boardRect.Width / 3;
            int cellH = boardRect.Height / 3;
            using (Pen gridPen = new Pen(GridColor, 4f))
            {
                gridPen.StartCap = LineCap.Round;
                gridPen.EndCap = LineCap.Round;

                // Vertical lines
                g.DrawLine(gridPen, boardRect.Left + cellW, boardRect.Top + 15, boardRect.Left + cellW, boardRect.Bottom - 15);
                g.DrawLine(gridPen, boardRect.Left + cellW * 2, boardRect.Top + 15, boardRect.Left + cellW * 2, boardRect.Bottom - 15);

                // Horizontal lines
                g.DrawLine(gridPen, boardRect.Left + 15, boardRect.Top + cellH, boardRect.Right - 15, boardRect.Top + cellH);
                g.DrawLine(gridPen, boardRect.Left + 15, boardRect.Top + cellH * 2, boardRect.Right - 15, boardRect.Top + cellH * 2);
            }
        }

        private void DrawPieces(Graphics g)
        {
            for (int i = 0; i < 9; i++)
            {
                char p = board[i];
                if (p == ' ') continue;

                Rectangle r = cellRects[i];
                int cx = r.X + r.Width / 2;
                int cy = r.Y + r.Height / 2;
                int size = 42;

                if (p == 'X')
                {
                    // Draw glowing Cyan X
                    using (Pen glowPen = new Pen(Color.FromArgb(40, CyanGlow), 14f) { StartCap = LineCap.Round, EndCap = LineCap.Round })
                    using (Pen xPen = new Pen(CyanX, 8f) { StartCap = LineCap.Round, EndCap = LineCap.Round })
                    {
                        g.DrawLine(glowPen, cx - size, cy - size, cx + size, cy + size);
                        g.DrawLine(glowPen, cx + size, cy - size, cx - size, cy + size);

                        g.DrawLine(xPen, cx - size, cy - size, cx + size, cy + size);
                        g.DrawLine(xPen, cx + size, cy - size, cx - size, cy + size);
                    }
                }
                else if (p == 'O')
                {
                    // Draw glowing Rose O
                    using (Pen glowPen = new Pen(Color.FromArgb(40, RoseGlow), 14f))
                    using (Pen oPen = new Pen(RoseO, 8f))
                    {
                        Rectangle oRect = new Rectangle(cx - size, cy - size, size * 2, size * 2);
                        g.DrawEllipse(glowPen, oRect);
                        g.DrawEllipse(oPen, oRect);
                    }
                }
            }
        }

        private void DrawWinningLine(Graphics g)
        {
            if (winningCombo == null || winningCombo.Length < 3) return;

            Rectangle r1 = cellRects[winningCombo[0]];
            Rectangle r3 = cellRects[winningCombo[2]];

            Point p1 = new Point(r1.X + r1.Width / 2, r1.Y + r1.Height / 2);
            Point p2 = new Point(r3.X + r3.Width / 2, r3.Y + r3.Height / 2);

            using (Pen glowPen = new Pen(Color.FromArgb(80, WinLineColor), 18f) { StartCap = LineCap.Round, EndCap = LineCap.Round })
            using (Pen linePen = new Pen(WinLineColor, 8f) { StartCap = LineCap.Round, EndCap = LineCap.Round })
            {
                g.DrawLine(glowPen, p1, p2);
                g.DrawLine(linePen, p1, p2);
            }
        }

        private GraphicsPath RoundedRect(Rectangle bounds, int radius)
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

    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new TicTacToeForm());
        }
    }
}
