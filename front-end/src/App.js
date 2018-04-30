import React from 'react';
import FileUploader from './FileUploader.js';
import AppHeader from './AppHeader.js'
import FunctionSelector from './FunctionSelector';
import Downloader from './Downloader'
import './App.css';

class App extends React.Component {
    constructor() {
        super();
        this.state = {
            email: '',
            bad_email: true,
            bad_files: false,
            length_array: 0,
            all_image_array: '',
            checked_func: [0],
        };
    }

    validateEmail = (email) => {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var testVal = !re.test(String(email).toLowerCase());
        console.log({'bad_email': testVal});
        return testVal
    };

    onEmailFieldChange = (event) => {
        this.setState(
            {email: event.target.value},
            () => {
                this.setState({bad_email: this.validateEmail(this.state.email)});
                console.log({'email': this.state.email})
            });
    };

    onDropSetter = (acceptedImages, rejectedImages) => {
        if (rejectedImages.length !== 0){
            this.setState({bad_files: true})
        } else {
            this.setState({bad_files: false})
        }
        this.setState({all_image_array: []});
        acceptedImages.forEach(file => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
                var readImage = reader.result;
                var joined = this.state.all_image_array.concat([readImage]);
                this.setState({all_image_array: joined},
                    () => {
                        this.setState({length_array: this.state.all_image_array.length},
                            () => {console.log({'length_array': this.state.length_array})});
                        console.log({'all_images': this.state.all_image_array});
                    });
            };
        });
    };

    render() {
        return (
            <div>
                <AppHeader
                    email={this.state.email}
                    bad_email={this.state.bad_email}
                    onChange={this.onEmailFieldChange}
                />
                <FileUploader
                    all_image_array={this.state.all_image_array}
                    onDrop={this.onDropSetter}
                    length={this.state.length_array}
                />
                <div>
                    <FunctionSelector />
                    <Downloader />
                </div>
            </div>
        );
    }
}

export default App;