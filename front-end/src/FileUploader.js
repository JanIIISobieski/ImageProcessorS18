import React from 'react';
import Dropzone from 'react-dropzone'

class FileUploader extends React.Component {
    constructor() {
        super();
        this.state = {
            accepted: [],
            rejected: [],
            current_image_string: '',
            all_image_array: [],
        }
    }

    onDropWhat = (acceptedImages, rejectedImages) => {
        this.setState({accepted: acceptedImages});
        this.setState({rejected: rejectedImages});
        acceptedImages.forEach(file => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
                //console.log(reader.result);
                var readImage = reader.result;
                this.setState({current_image_string: readImage});
                var joined = this.state.all_image_array.concat([readImage]);
                this.setState({all_image_array: joined});
            };
        });
        console.log({'accepted': this.state.accepted});
        console.log({'rejected': this.state.rejected});
        console.log({'current_image_string': this.state.current_image_string});
        console.log({'all_images': this.state.all_image_array});
    };

    render() {
        return (
            <section>
                <p>Try dropping some files here, or click to select files to upload.</p>
                <p>Only *.jpeg and *.png images will be accepted</p>
                <div className="dropzone">
                    <Dropzone
                        accept="image/jpeg, image/png"
                        onDrop= {this.onDropWhat}
                    >
                    </Dropzone>
                </div>
                <aside>
                    <h2>Accepted files</h2>
                    <ul>
                        {
                            this.state.accepted.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                        }
                    </ul>
                    <h2>Rejected files</h2>
                    <ul>
                        {
                            this.state.rejected.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                        }
                    </ul>
                </aside>
                <img src={this.state.current_image_string} width='500'/>
            </section>
        );
    }
}

export default FileUploader;