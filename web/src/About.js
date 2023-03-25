import React from 'react'
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import { Link } from "react-router-dom";


const AboutPage = () => {
  return (

    <>
      <Box
        sx={{
          pt: 4,
          pb: 3,
        }}
      >
      <Container maxWidth="lg">
      <Typography
      component="h1"
      variant="h5"
      align="left"
      color="text.primary"
      gutterBottom
    >
      About
        </Typography>
        
        <Typography display="block" variant="h6" align="left" color="text.secondary" paragraph="true">
        Russian Error-Annotated Learner of English Corpus (<Link to="https://realec.org/">REALEC</Link>) is a corpus of essays written by university students with Russian as L1 in answer to examinations questions of two types. The essays are annotated for errors and have POS tags.
        </Typography>

        <Typography display="block" variant="h6" align="left" color="text.secondary" paragraph="true">
        Realec Search is a tool that allows to execute different types of search on REALEC essays. This tool might be useful for L2 research, including Bachelor and Master theses.
        </Typography>

        <Typography display="block" variant="h6" align="left" color="text.secondary" paragraph="true">
        <Link to="/general-search">General search</Link> allows to search for a token or a sequence of tokens. It also offers functionality of filtering search results by POS tags.
        </Typography>
        
        <Typography display="block" variant="h6" align="left" color="text.secondary" paragraph="true">
        <Link to="/mistakes-search">Mistakes search</Link> returns annotated mistakes in the corpus.It is possible to pick the type and the cause of the queried mistake.
        </Typography>
          
        <Typography
        component="h1"
        variant="h5"
        align="left"
        color="text.primary"
        gutterBottom
      >
      Labeling
        </Typography>

        <Typography display="block" variant="h6" align="left" color="text.secondary" paragraph="true">    
        Follow <Link to="//localhost:8082">this link</Link> to open the data labeling platform for the project on text coherence.
        </Typography>
            
        </Container>

        </Box>
    </>
    
    )
}

export const Head = () => <title>About</title>

export default AboutPage