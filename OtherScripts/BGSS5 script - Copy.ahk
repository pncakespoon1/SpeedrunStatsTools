numberCount := 1
*A::
  Loop, 1000
  {
    WinActivate, BGSS
    sleep, 300
    Send, ^c
    sleep, 300
    entryType := Clipboard
    sleep, 300
    if(entryType = "n/a")
    {
      entryType := "none"
    }
    fileName := entryType numberCount
    sleep, 300
    Clipboard := fileName
    sleep, 300
    Send {Down}
    sleep, 300
    WinActivate, new
    sleep, 300
    Send, {F2}
    sleep, 300
    Send, ^v
    sleep, 300
    Send, {tab}
    sleep, 300
    numberCount += 1
  }
*B::
  WinActivate, BGSS
  sleep, 50
  Send, ^c
  sleep, 50
  entryType := Clipboard
  sleep, 50
  if(entryType = n/a)
  {
    entryType := "none"
  }
  fileName := entryType numberCount
  sleep, 50
  Clipboard := fileName