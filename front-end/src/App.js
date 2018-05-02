import React from 'react';
import FileUploader from './FileUploader.js';
import AppHeader from './AppHeader.js'
import FunctionSelector from './FunctionSelector';
import Downloader from './Downloader'
import UserMetrics from './UserMetrics'
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
                functions: '',
                o_hist: '',
                original: '',
                processed: '',
                p_hist: '',
                ret_time: 'No info yet',
                size: [['', '']],
                up_time: 'No info yet',
                user_metrics: [['0', '0', '0', '0'], ''],
            },
        };
    }

    validateEmail = (email) => {
        var testVal = email == '';
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
                            () => {console.log({'length_array': this.state.length_array});
                        });
                        console.log({'all_images': this.state.all_image_array});
                    });
            };
        });
    };

    postRequest = (event, func_array) => {
        var address = 'http://67.159.95.29:5000/api/process_images';
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
                console.log({'axios': response});
                console.log({'state_data': this.state.data_received});
                this.setState({data_received: response.data},
                    () => console.log(this.state.data_received)
                )
            })
    };

    render() {
        return (
            <div>
                <AppHeader
                    email={this.state.email}
                    bad_email={this.state.bad_email}
                    onChange={this.onEmailFieldChange}
                />
                <div>
                    <p>
                        Directions: Drag files into the box. Provide a valid email in the bar above. Select wanted
                        processing functions (at least one must be selected).
                        If no email given and no images uploaded, the process button will be disabled.
                        Press the process button to get images back. Use the Next Image and Previous Images to cycle
                        through the uploaded files. To download the image set in a given format, select the wanted
                        download format and press download. Image set will automatically download as a .zip if multiple
                        images, or as the wanted image type if a single image.
                    </p>
                </div>
                <div>
                    <FileUploader
                        all_image_array={this.state.all_image_array}
                        onDrop={this.onDropSetter}
                        length={this.state.length_array}
                        processed_data={this.state.data_received}
                    />
                </div>
                <div>
                    <div className="functions_adjacent">
                        <FunctionSelector
                            email={this.state.email}
                            bad_email_flag={this.state.bad_email}
                            files={this.state.all_image_array}
                            length={this.state.length_array}
                            get_processed={this.postRequest}
                        />
                        <Downloader
                            email={this.state.email}
                            recieved={this.state.data_received}
                            length={this.state.length_array}
                        />
                    </div>
                </div>
                <UserMetrics
                    data={this.state.data_received}
                />
            </div>
        );
    }
}

export default App;