'===================================================================
' LaunchWebLauncher.vbs
' Lanzador de ACMSLWebServer + WebLauncher
'
' 1) Si ACMSLServerClaude.exe no esta corriendo, lo lanza minimizado
' 2) Espera a que el servidor responda en puerto 60080
' 3) Abre Edge en modo --app (sin pestanas, sin barra de URL)
'    con un user-data-dir propio para poder rastrear el proceso
' 4) Monitoriza Edge: cuando el usuario cierra la ventana,
'    termina automaticamente el servidor
'===================================================================

Option Explicit

Const SERVER_EXE = "ACMSLServerClaude.exe"
Const SERVER_URL = "http://localhost:60080/"
Const MAX_WAIT_SECONDS = 10
Const EDGE_PROFILE_NAME = "ACMSLWebLauncher"
Const POLL_INTERVAL_MS = 2000

Dim objShell, objWMI, objFSO
Set objShell = CreateObject("WScript.Shell")
Set objWMI = GetObject("winmgmts:\\.\root\cimv2")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Directorio del script (donde estan el .exe y WebLauncher.html)
Dim scriptDir
scriptDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

' Perfil temporal de Edge para aislar el proceso
Dim edgeProfileDir
edgeProfileDir = objShell.ExpandEnvironmentStrings("%TEMP%") & "\" & EDGE_PROFILE_NAME

' ===================================================================
' PASO 1: Lanzar el servidor si no esta corriendo
' ===================================================================
Dim colProcesses
Set colProcesses = objWMI.ExecQuery( _
    "SELECT Name FROM Win32_Process WHERE Name='" & SERVER_EXE & "'")

Dim serverYaCorria
serverYaCorria = (colProcesses.Count > 0)

If Not serverYaCorria Then
    Dim serverPath
    serverPath = scriptDir & SERVER_EXE

    If Not objFSO.FileExists(serverPath) Then
        MsgBox "No se encuentra " & serverPath, vbCritical, "Error"
        WScript.Quit 1
    End If

    ' Lanzar minimizado (7 = minimized, False = no esperar)
    objShell.Run """" & serverPath & """", 7, False
End If

' ===================================================================
' PASO 2: Esperar a que el servidor responda
' ===================================================================
Dim ready, elapsed
ready = False
elapsed = 0

Do While Not ready And elapsed < MAX_WAIT_SECONDS
    ready = ServerResponde()
    If Not ready Then
        WScript.Sleep 500
        elapsed = elapsed + 0.5
    End If
Loop

If Not ready Then
    MsgBox "El servidor no responde despues de " & MAX_WAIT_SECONDS & " segundos.", _
           vbExclamation, "ACMSLWebServer"
    WScript.Quit 1
End If

' ===================================================================
' PASO 3: Abrir Edge en modo app con perfil aislado
' ===================================================================
Dim edgePath
edgePath = FindEdge()

If edgePath = "" Then
    ' Fallback: navegador por defecto (sin monitorizacion)
    objShell.Run SERVER_URL
Else
    ' Comprobar si Edge con nuestro perfil ya esta corriendo
    Dim colEdgeCheck
    Set colEdgeCheck = objWMI.ExecQuery( _
        "SELECT ProcessId FROM Win32_Process WHERE Name='msedge.exe'" & _
        " AND CommandLine LIKE '%" & EDGE_PROFILE_NAME & "%'")

    If colEdgeCheck.Count > 0 Then
        ' Ya hay una instancia abierta: no lanzar otra, solo salir
        Set colEdgeCheck = Nothing
        Set colProcesses = Nothing
        Set objFSO = Nothing
        Set objWMI = Nothing
        Set objShell = Nothing
        WScript.Quit 0
    End If
    Set colEdgeCheck = Nothing

    ' Crear directorio de perfil si no existe
    If Not objFSO.FolderExists(edgeProfileDir) Then
        objFSO.CreateFolder edgeProfileDir
    End If

    ' Lanzar Edge con perfil aislado
    Dim edgeCmd
    edgeCmd = """" & edgePath & """ --app=" & SERVER_URL & _
              " --user-data-dir=""" & edgeProfileDir & """"
    objShell.Run edgeCmd, 1, False

    ' Esperar a que Edge arranque
    WScript.Sleep 3000

    ' ==============================================================
    ' PASO 4: Monitorizar Edge - cuando se cierre, parar el servidor
    ' ==============================================================
    Dim colEdge

    Do
        WScript.Sleep POLL_INTERVAL_MS

        ' Buscar procesos msedge.exe que usen nuestro perfil
        Set colEdge = objWMI.ExecQuery( _
            "SELECT ProcessId FROM Win32_Process WHERE Name='msedge.exe'" & _
            " AND CommandLine LIKE '%" & EDGE_PROFILE_NAME & "%'")

        ' Si ya no hay ninguno, el usuario cerro la ventana
        If colEdge.Count = 0 Then Exit Do
    Loop

    ' Edge cerrado: terminar el servidor (solo si lo lanzamos nosotros)
    If Not serverYaCorria Then
        Dim colServer, proc
        Set colServer = objWMI.ExecQuery( _
            "SELECT * FROM Win32_Process WHERE Name='" & SERVER_EXE & "'")
        For Each proc In colServer
            proc.Terminate
        Next
        Set colServer = Nothing
    End If
End If

' ===================================================================
' LIMPIEZA
' ===================================================================
Set colProcesses = Nothing
Set objFSO = Nothing
Set objWMI = Nothing
Set objShell = Nothing
WScript.Quit 0

'===================================================================
' Funcion: comprueba si el servidor responde
'===================================================================
Function ServerResponde()
    On Error Resume Next
    Dim http
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    http.setTimeouts 1000, 1000, 1000, 1000
    http.Open "GET", SERVER_URL, False
    http.Send

    If Err.Number = 0 And http.Status = 200 Then
        ServerResponde = True
    Else
        ServerResponde = False
    End If

    Set http = Nothing
    On Error GoTo 0
End Function

'===================================================================
' Funcion: localiza msedge.exe
'===================================================================
Function FindEdge()
    Dim paths, p

    paths = Array( _
        objShell.ExpandEnvironmentStrings("%ProgramFiles(x86)%") & "\Microsoft\Edge\Application\msedge.exe", _
        objShell.ExpandEnvironmentStrings("%ProgramFiles%") & "\Microsoft\Edge\Application\msedge.exe", _
        objShell.ExpandEnvironmentStrings("%LocalAppData%") & "\Microsoft\Edge\Application\msedge.exe" _
    )

    FindEdge = ""
    For Each p In paths
        If objFSO.FileExists(p) Then
            FindEdge = p
            Exit For
        End If
    Next
End Function
