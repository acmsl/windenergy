If LCase$(Right$(Program, 4)) = ".bat" Or LCase$(Right$(Program, 4)) = ".cmd" Then

    ' Batch files must be run through cmd.exe
    Shell = ShellExecute(0, "open", "cmd.exe", _
                         "/c """ & Program & """ " & LTrim$(Mid$(Program, FirstSpace)), _
                         WorkDir, ShowCmd)

ElseIf LCase$(Right$(Program, 4)) = ".exe" Then

    ' Executables can be launched directly
    Shell = ShellExecute(0, "open", _
                         Left$(Program, FirstSpace - 1), _
                         LTrim$(Mid$(Program, FirstSpace)), _
                         WorkDir, ShowCmd)

Else
    ' Default behavior for other file types
    Shell = ShellExecute(0, "open", _
                         Left$(Program, FirstSpace - 1), _
                         LTrim$(Mid$(Program, FirstSpace)), _
                         WorkDir, ShowCmd)
End If
