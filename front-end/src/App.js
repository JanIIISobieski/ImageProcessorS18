import React from 'react';
import FileUploader from './FileUploader.js';
import AppHeader from './AppHeader.js'
import FunctionSelector from './FunctionSelector';
import Downloader from './Downloader'
import axios from 'axios'
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
            data_received: {
                email: '',
                functions: '',
                originals: '',
            },
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
        this.setState({data_received:
                {
                    email: '',
                    functions: '',
                    originals: '',
                }
        });
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

    postRequest = (event, func_array) => {
        var address = 'http://67.159.95.29:3000/api/process_images';
        var chosen_func = [0, 0, 0, 0];
        func_array.forEach(element => {
           chosen_func[element] = 1
        });

        var json = {
            'email': this.state.email,
            'originals': this.state.all_image_array,
            'functions': chosen_func
        };
        console.log({'post_request': [address, json]});
        axios.post(address, json)
            .then((response) => {
                console.log({'axios_response': response});
                this.setState({
                    data_received: response.data
                })
            })
    };

    render() {
        return (
            <div className="outer">
                <AppHeader
                    email={this.state.email}
                    bad_email={this.state.bad_email}
                    onChange={this.onEmailFieldChange}
                />
                <FileUploader
                    all_image_array={this.state.all_image_array}
                    onDrop={this.onDropSetter}
                    length={this.state.length_array}
                    processed_data={this.state.data_received}
                />
                <div className="center">
                    <div className="adjacent">
                        <FunctionSelector
                            email={this.state.email}
                            files={this.state.all_image_array}
                            length={this.state.length_array}
                            get_processed={this.postRequest}
                        />
                        <Downloader
                            email={this.state.email}
                        />
                    </div>
                </div>
            </div>
        );
    }
}

export default App;