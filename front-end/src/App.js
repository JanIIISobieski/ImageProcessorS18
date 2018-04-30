import React from 'react';
import FileUploader from './FileUploader.js';
import AppHeader from './AppHeader.js'
import FunctionSelector from './FunctionSelector';
import Downloader from './Downloader'
import './App.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <AppHeader />
                <FileUploader />
                <div>
                    <FunctionSelector />
                    <Downloader />
                </div>
            </div>
        );
    }
}

export default App;