global count := 1000
newHeight := Floor(A_ScreenHeight / 2.5)
WinMove, Minecraft,,1920,0,%A_ScreenWidth%,%newHeight%
Loop {
  getSeed()
  sleep, 100
  createWorld()
  sleep, 10000
  newSS()
  sleep, 100
  exitWorld()
  sleep, 1000
  count -= 1
  if (count = 0) {
    break
  }
}


newSS() {
  Send, {F2}
}

exitWorld() {
  Send, {esc}
  Send, {Shift down}
  Send, {tab}
  Send, {Shift up}
  Send, {enter}
}

getSeed() {
  WinActivate, C0R0B0
  Send, {Ctrl Down}
  Send, c
  Send, {Ctrl Up}
  Send, {Down}
  WinActivate, Minecraft
  
}

createWorld() {
  Send, `t
  Send, {enter}
  Send, `t
  Send, `t
  Send, `t
  Send, {enter}
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, {enter}
  Send, `t
  Send, `t
  Send, `t
  Send, {Ctrl down}
  Send, v
  Send, {Ctrl up}
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, `t
  Send, {enter}
}
#IfWinActive, Minecraft
  {
    *B:: 
      newSS()
    return

    *N:: 
      exitWorld()
    return

    *M:: 
      createWorld()
    return

    *G:: 
      getSeed()
    return
  } 