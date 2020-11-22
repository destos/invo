import React from 'react';
import './App.css'
import { ApolloProvider } from '@apollo/client'
import client from './client'
import {Container } from "@material-ui/core"
import Situations from './views/Situations';

function App() {
  return (
    <ApolloProvider client={client}>
      <Container>
        <Situations/>
      </Container>
    </ApolloProvider>
  );
}

export default App;
