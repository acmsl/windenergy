Set objFSO = CreateObject("Scripting.FileSystemObject")
strFile = "c:\Proyectos\LdP\v1r12\Web_Launcher\trabajo-1-feb-2026.html"
Set objFile = objFSO.OpenTextFile(strFile, 1)
strContent = objFile.ReadAll
objFile.Close
strContent = Replace(strContent, "[00-ff]", "[\u0300-\u036f]")
Set objFile = objFSO.OpenTextFile(strFile, 2)
objFile.Write strContent
objFile.Close
WScript.Echo "Done"
