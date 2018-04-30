import React from 'react';
import FileUploader from './FileUploader.js';
import AppHeader from './AppHeader.js'
import FunctionSelector from "./FunctionSelector";
import './App.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <AppHeader />
                <FileUploader />
                <FunctionSelector />
            </div>
        );
    }
}

export default App;