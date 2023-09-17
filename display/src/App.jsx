import { useState } from "react";
import "./App.css";
import {
  Button,
  Typography,
  Table,
  TableBody,
  TableContainer,
  TableRow,
  TableCell,
  TableHead
} from "@mui/material";
import octocat from "../assets/animated_octocat.gif";
import frieza from "../assets/dbz-dragon-ball-z.gif";
import orochimaru from "../assets/orochimaru.gif";
import narutoorochimaru from "../assets/naruto-orochimaru.gif";
import kabuto from "../assets/snake-sage-mode-kabuto.gif";
import dataset from "../../data/2023 09 17 - 11 46 29 movie_data.json"

function Filters() {
  
}

function FilteredList() {

}

function App() {
  const [count, setCount] = useState(8999);
  const increaseClick = () => setCount(count + 1);
  let test_movie_list = "";
  if (count > 9000) {
    try {
      test_movie_list = (
        <>
          <p>This is a temporary test list</p>
          <TableContainer>
            <Table>
              <TableRow>
                <TableCell>Movie Name</TableCell>
                <TableCell>Director</TableCell>
                <TableCell>Year</TableCell>
              </TableRow>
              <TableRow>
              <TableCell>Alien</TableCell>
              <TableCell>Cameron</TableCell>
              <TableCell>2001</TableCell>
              </TableRow>
            </Table>
          </TableContainer>
        </>
      );
    } catch (error) {
      console.log("This shouldn't be happening");
      console.log(error);
    }
  }

  let raw_movie_list = "";
  if (count > 9010) {
    try {
      raw_movie_list = (
        <>
          <TableContainer>
            <Table>
              <TableHead>
                <TableCell>Movie</TableCell>
                <TableCell>Directors</TableCell>
                <TableCell>Genres</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Public Score</TableCell>
                <TableCell>Press Score</TableCell>
              </TableHead>
              <TableRow>
                <TableCell>{dataset[0].title}</TableCell>
                <TableCell>{dataset[0].directors}</TableCell>
                <TableCell>{dataset[0].genre}</TableCell>
                <TableCell>{dataset[0].date}</TableCell>
                <TableCell>{dataset[0]["public note"]}</TableCell>
                <TableCell>{dataset[0]["critic note"]}</TableCell>
              </TableRow>
            </Table>
          </TableContainer>
        </>
      )
    }
    catch {}
  }

  let complete_movie_list = "";
  if (count > 9020) {
    try {
      complete_movie_list = (
        <>
          <TableContainer>
            <Table>
              <TableHead>
                <TableCell>Movie</TableCell>
                <TableCell>Directors</TableCell>
                <TableCell>Genres</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Public Score</TableCell>
                <TableCell>Press Score</TableCell>
              </TableHead>
              {dataset.map( (movie) => <TableRow>
                <TableCell>{movie.title}</TableCell>
                <TableCell>{movie.directors}</TableCell>
                <TableCell>{movie.genre}</TableCell>
                <TableCell>{movie.date}</TableCell>
                <TableCell>{movie["public note"]}</TableCell>
                <TableCell>{movie["critic note"]}</TableCell>
              </TableRow>)}
            </Table>
          </TableContainer>
        
        </>
      )
    }
    catch {}
  }

  return (
    <>
      <main>
        <header>
          <img
            src={octocat}
            alt="Octocat from GITHUB"
            title="Octocat from GITHUB"
          />
          <img
            src={frieza}
            alt="Frieza from Dragon Ball"
            title="Frieza from Dragon Ball"
          />
          <img
            src={orochimaru}
            alt="Orochimaru from Naruto"
            title="Orochimaru from Naruto"
          />
          <img
            src={narutoorochimaru}
            alt="Orochimaru from Naruto"
            title="Orochimaru from Naruto"
          />
          <img
            src={kabuto}
            alt="Kabuto from Naruto"
            title="Kabuto from Naruto"
          />
        </header>
        <Typography variant="h4">THIS IS THE WORLD NOW!</Typography>
        <Button variant="contained" onClick={increaseClick}>
          Click me to active super Sayajin mode! {count} clicks!
        </Button>
      </main>
      {test_movie_list}
      {raw_movie_list}
      {complete_movie_list}
    </>
  );
}

export default App;
