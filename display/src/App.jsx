import { useState } from 'react'
import './App.css'
import { Button } from "@mui/material"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <p>THIS IS MY WORLD NOW!</p>
      <Button>Click me to active super Sayajin mode!</Button>
    </>
  )
}

export default App
