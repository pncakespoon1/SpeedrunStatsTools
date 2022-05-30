global count := 1
*A::
  Loop {
    Send, %count%
    sleep, 100
    Send, {tab}
    sleep, 100
    count += 1
  }