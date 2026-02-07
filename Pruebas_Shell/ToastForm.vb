Option Explicit

Private Declare Function SetWindowPos Lib "user32" _
    (ByVal hwnd As Long, ByVal hWndInsertAfter As Long, _
     ByVal X As Long, ByVal Y As Long, ByVal cx As Long, _
     ByVal cy As Long, ByVal wFlags As Long) As Long

Private Const HWND_TOPMOST = -1
Private Const SWP_NOMOVE = &H2
Private Const SWP_NOSIZE = &H1
Private Const SWP_SHOWWINDOW = &H40

Public Sub ShowToast(ByVal Message As String, Optional ByVal DurationMS As Long = 2000)

    lblMsg.Caption = Message

    ' Add padding around the label
    Me.Width = lblMsg.Width + 300
    Me.Height = lblMsg.Height + 300

    ' Position bottom-right of screen
    Me.Left = Screen.Width - Me.Width - 200
    Me.Top = Screen.Height - Me.Height - 600

    Me.Show vbModeless

    ' Make it topmost
    SetWindowPos Me.hwnd, HWND_TOPMOST, 0, 0, 0, 0, _
                 SWP_NOMOVE Or SWP_NOSIZE Or SWP_SHOWWINDOW

    ' Auto-close timer
    tmrClose.Interval = DurationMS
    tmrClose.Enabled = True
End Sub

Private Sub tmrClose_Timer()
    tmrClose.Enabled = False
    Unload Me
End Sub


'====================
Ejemplos:

frmToast.ShowToast "Opening PDF...", 3000   ' 3 seconds

'------
frmToast.ShowToast "Running script..."
Call RunProgram("""C:\Scripts\deploy.bat"" staging")

'----------------------
frmToast.ShowToast "Launching process..."
Call RunProgram("""C:\Tools\Updater.exe"" -silent")

